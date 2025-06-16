from groq import AsyncGroq
import os
from typing import Literal

async def classify_query(query: str, client: AsyncGroq) -> Literal["calculation", "news", "unknown"]:
    """
    Classify a query using Groq's API to understand its intent.
    
    Args:
        query (str): The user's query
        client (AsyncGroq): Groq client instance
        
    Returns:
        Literal["calculation", "news", "unknown"]: The classification of the query
    """
    system_prompt = """You are a query classifier. Your task is to determine if a query is asking for:
1. A calculation or mathematical operation
2. News or current events information
3. Something else (unknown)

Respond with *ONLY* one word: "calculation", "news", or "unknown". Do not include any other text or punctuation.

Infer the intent even if explicit keywords are not present. For example, a query like "south africa test championship win against australia" should be classified as "news" because it refers to a current event or recent happening. Similarly, "what is 2 + 3" should be "calculation".

**Hint for news queries: News queries typically do not involve direct numerical calculations.**

For calculations, look for mathematical operations, numbers, or requests for computation.
For news, look for queries about current events, recent happenings, or requests for information about ongoing situations.
"""

    try:
        response = await client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct", # Using a suitable Groq model for classification
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ],
            temperature=0.1,  # Low temperature for more consistent classification
            max_tokens=10
        )
        
        classification = response.choices[0].message.content.strip().lower()
        print(f"DEBUG: Raw classification from Groq: '{classification}'") # Debug line
        
        # Ensure we only return valid classifications
        if classification in ["calculation", "news", "unknown"]:
            return classification
        return "unknown"
        
    except Exception as e:
        print(f"Error in query classification: {e}")
        return "unknown" 