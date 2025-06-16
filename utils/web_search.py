from newsapi import NewsApiClient
from typing import List, Dict
import logging
from datetime import datetime, timedelta
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def search_news(query: str, max_results: int = 5) -> List[Dict]:
    """
    Search for news articles using NewsAPI.
    
    Args:
        query (str): The search query
        max_results (int): Maximum number of results to return
        
    Returns:
        List[Dict]: List of news articles with title, description, and url
    """
    try:
        logger.info(f"Searching news for query: {query}")
        
        # Initialize NewsAPI client
        api_key = os.getenv('NEWS_API_KEY')
        if not api_key:
            logger.error("NEWS_API_KEY environment variable not set")
            raise ValueError("NEWS_API_KEY environment variable not set")
            
        newsapi = NewsApiClient(api_key=api_key)
        
        # Calculate date range (last 30 days for historical news)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        # Search for news
        response = newsapi.get_everything(
            q=query,
            from_param=start_date.strftime('%Y-%m-%d'),
            to=end_date.strftime('%Y-%m-%d'),
            language='en',
            sort_by='relevancy',
            page_size=max_results
        )
        
        articles = response.get('articles', [])
        logger.info(f"Found {len(articles)} articles")
        
        # Format the results
        formatted_articles = []
        for article in articles:
            if article.get('title') and article.get('url'):
                formatted_articles.append({
                    'title': article['title'],
                    'description': article.get('description', ''),
                    'url': article['url'],
                    'publishedAt': article.get('publishedAt', '')
                })
        
        logger.info(f"Processed {len(formatted_articles)} valid articles")
        return formatted_articles
        
    except Exception as e:
        logger.error(f"Error fetching news: {e}")
        return []
