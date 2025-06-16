from groq import AsyncGroq
from utils.web_search import search_news
import json
import asyncio
import logging

logger = logging.getLogger(__name__)

class NewscasterAgent:
    def __init__(self, client: AsyncGroq):
        self.client = client

    def _prepare_query(self, query: str) -> str:
        """Prepare the query for better news search results."""
        # Remove common filler words
        filler_words = ['please', 'can you', 'tell me', 'show me', 'give me', 'i want', 'i need']
        query = query.lower()
        for word in filler_words:
            query = query.replace(word, '')
        
        # Add 'news' if not present and query is too short
        if len(query.split()) < 3 and 'news' not in query:
            query = f"{query} news"
            
        return query.strip()

    async def handle(self, query: str):
        system_prompt = """You are a helpful assistant that summarizes news articles. Your task is to:
1. Provide a concise summary of the key points from the news articles
2. Focus on the most important and recent information
3. Include relevant details like dates, locations, and key figures
4. If there are multiple articles, synthesize them into a coherent summary
5. Do not include any pre-amble or conversational filler
6. If the articles seem irrelevant to the query, mention this

Format your response in clear paragraphs with proper spacing."""
        
        # Prepare the query for better search results
        search_query = self._prepare_query(query)
        logger.info(f"Original query: {query}")
        logger.info(f"Prepared search query: {search_query}")
        
        # Run search_news in a thread pool since it's synchronous
        search_results = await asyncio.to_thread(search_news, search_query)
        if not search_results:
            yield "I couldn't find any relevant news articles for your query. Please try rephrasing your question or asking about a different topic."
            return

        # Format articles with dates and sources
        news_text = "\n\n".join([
            f"Article {i+1}:\nTitle: {a['title']}\nDescription: {a['description']}\nPublished: {a['publishedAt']}\nURL: {a['url']}"
            for i, a in enumerate(search_results)
        ])
        
        user_prompt = f"Please summarize the following news articles related to '{query}':\n\n{news_text}"
        
        try:
            response = await self.client.chat.completions.create(
                model="meta-llama/llama-4-scout-17b-16e-instruct",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                stream=True,
                temperature=0.7  # Add some creativity to the summaries
            )
            
            async for chunk in response:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
                
        except Exception as e:
            logger.error(f"Error in newscaster agent: {e}")
            yield f"I encountered an error while trying to summarize the news. Please try again later."
