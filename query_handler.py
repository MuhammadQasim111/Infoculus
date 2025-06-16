import asyncio
from enum import Enum
from typing import Optional, List, Dict
from newsapi import NewsApiClient
from groq import AsyncGroq
import os

class QueryType(Enum):
    NEWS = "news"
    MATH = "math"
    UNKNOWN = "unknown"

class QueryHandler:
    def __init__(self, newsapi: NewsApiClient, groq_client: AsyncGroq):
        self.newsapi = newsapi
        self.groq_client = groq_client

    def classify_query(self, query: str) -> QueryType:
        # Simple classification based on presence of numbers or news keywords.
        # A more sophisticated approach would involve Groq for intent classification.

        # Check for numbers for math
        if any(char.isdigit() for char in query):
            return QueryType.MATH
            
        # Check for news keywords if no numbers are found
        news_keywords = ["news", "headlines", "report", "latest", "update", 
                        "sport", "weather", "politics", "breaking", "event"]
        if any(keyword in query.lower() for keyword in news_keywords):
            return QueryType.NEWS
            
        return QueryType.UNKNOWN

    async def process_query(self, query: str) -> str:
        query_type = self.classify_query(query)
        
        if query_type == QueryType.UNKNOWN:
            return "Please enter a more clear query (math or news related)."
            
        if query_type == QueryType.MATH:
            return await self.process_math_query(query)
            
        return await self.process_news_query(query)

    async def process_news_query(self, query: str) -> str:
        try:
            # NewsAPI is synchronous, so run it in a thread pool executor
            top_headlines = await asyncio.to_thread(self.newsapi.get_everything, q=query, language='en', sort_by='relevancy', page_size=5)
            articles = top_headlines.get('articles', [])

            if not articles:
                return "Could not find any news related to your query."

            news_text = "\n\n".join([f"Title: {a['title']}\nDescription: {a['description']}\nURL: {a['url']}" for a in articles])
            
            system_prompt = "You are a helpful assistant that summarizes news articles. Your responses should be concise and informative, focusing on the key details of the news. Do not include any pre-amble like 'Here is the news summary:'. Just provide the summary. If you cannot summarize, state that the news could not be summarized."
            
            full_response = []
            async with self.groq_client.chat.completions.with_streaming_response.create(
                model="mixtral-8x7b-32768",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Summarize the following news articles:\n\n{news_text}"}
                ],
            ) as response:
                async for chunk in response.iter_text():
                    full_response.append(chunk)
            return "".join(full_response)

        except Exception as e:
            return f"Error fetching or summarizing news: {e}"

    async def process_math_query(self, query: str) -> str:
        system_prompt = "You are a helpful calculator. Solve mathematical problems with complete calculation steps. Do not include any conversational filler."
        
        try:
            full_response = []
            async with self.groq_client.chat.completions.with_streaming_response.create(
                model="mixtral-8x7b-32768",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query}
                ],
            ) as response:
                async for chunk in response.iter_text():
                    full_response.append(chunk)
            return "".join(full_response)
                
        except Exception as e:
            return f"Error calculating: {e}"