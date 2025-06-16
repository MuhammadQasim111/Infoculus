from groq import AsyncGroq

class ShaitaniCalculatorAgent:
    def __init__(self, client: AsyncGroq):
        self.client = client

    async def handle(self, query: str):
        # Use Groq API to perform the calculation intelligently.
        prompt = f"Calculate the following mathematical expression or solve the problem precisely:\n{query}"

        # Streaming response from Groq chat completion
        response = await self.client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",  # Using a suitable Groq model for calculations
            messages=[{"role": "user", "content": prompt}],
            stream=True
        )
        async for chunk in response:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
