from groq import AsyncGroq
from .calculator_agent import ShaitaniCalculatorAgent
from .newscaster_agent import NewscasterAgent
from utils.query_classifier import classify_query

class AgentOrchestrator:
    def __init__(self, client: AsyncGroq):
        self.client = client
        self.calculator_agent = ShaitaniCalculatorAgent(client)
        self.newscaster_agent = NewscasterAgent(client)

    async def route_query(self, query: str):
        classification = await classify_query(query, self.client)

        if classification == "calculation":
            async for chunk in self.calculator_agent.handle(query):
                yield chunk

        elif classification == "news":
            async for chunk in self.newscaster_agent.handle(query):
                yield chunk

        else:
            # Unknown queries: try calculator then newscaster
            async for chunk in self.calculator_agent.handle(query):
                yield chunk

            yield "\n\n-- Trying news agent as well --\n\n"

            async for chunk in self.newscaster_agent.handle(query):
                yield chunk
