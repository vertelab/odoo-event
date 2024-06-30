# tools.py
import os
from crawl4ai import WebCrawler
from crawl4ai.extraction_strategy import LLMExtractionStrategy
from pydantic import BaseModel, Field
from praisonai_tools import BaseTool

class ModelFee(BaseModel):
    llm_model_name: str = Field(..., description="Name of the model.")
    input_fee: str = Field(..., description="Fee for input token for the model.")
    output_fee: str = Field(..., description="Fee for output token for the model.")

class ModelFeeTool(BaseTool):
    name: str = "ModelFeeTool"
    description: str = "Extracts model fees for input and output tokens from the given pricing page."

    def _run(self, url: str):
        crawler = WebCrawler()
        crawler.warmup()

        result = crawler.run(
            url=url,
            word_count_threshold=1,
            extraction_strategy= LLMExtractionStrategy(
                provider="openai/gpt-4o",
                api_token=os.getenv('OPENAI_API_KEY'), 
                schema=ModelFee.schema(),
                extraction_type="schema",
                instruction="""From the crawled content, extract all mentioned model names along with their fees for input and output tokens. 
                Do not miss any models in the entire content. One extracted model JSON format should look like this: 
                {"model_name": "GPT-4", "input_fee": "US$10.00 / 1M tokens", "output_fee": "US$30.00 / 1M tokens"}."""
            ),            
            bypass_cache=True,
        )
        return result.extracted_content

if __name__ == "__main__":
    # Test the ModelFeeTool
    tool = ModelFeeTool()
    url = "https://www.openai.com/pricing"
    result = tool.run(url)
    print(result)
