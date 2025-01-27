import hashlib
import json
import os
import urllib.parse
from typing import Type

import requests
import tiktoken
from dotenv import load_dotenv
from lxml import html as lxml_html
from lxml.etree import XPathEvalError
from openai import OpenAI
from pydantic import BaseModel, create_model

from emmetify import emmetify_compact_html
from emmetify.converters.html_converter import HtmlConverterMaps
from emmetify.utils.xpath import restore_xpath_from_converter_maps

load_dotenv()


class ExtractionError(Exception):
    pass


client = OpenAI(
    api_key=os.environ.get(
        "OPENAI_API_KEY", "<set your OpenAI API key if you didn't set as an env var>"
    )
)


def fill_schema(schema: dict, completion_schema: dict) -> dict:
    for key, value in completion_schema.items():
        if key in schema:
            schema[key] = value
    return schema


with open("./prompt.txt", "r") as f:
    system_prompt = f.read()


class WebExtractionAgent:
    extracted_data: dict[str, list[str]] = {}
    extracted_data_hash: list[str] = []

    requests_queue: list[str] = []
    requests_count = 0
    requests_history: list[str] = []
    requests_queries: dict[str, list[str]] = {}

    tokens = {
        "html": {
            "raw": 0,
            "compressed": 0,
            "compression_ratio": 0,
        },
        "llm": {
            "input": 0,
            "output": 0,
        },
    }

    def __init__(self, start_url: str, queries: list[str], max_count: int, model: str):
        self.model = model
        self.tokenizer = tiktoken.encoding_for_model(model)
        self.max_count = max_count
        self.requests_queue = [start_url]

        self.requests_queries = {q.lower().replace(" ", "_"): [] for q in queries}
        field_names = {q.lower().replace(" ", "_"): (list[str] | None, None) for q in queries}
        self.ExtractedData = create_model("ExtractedData", **field_names)

        # Create ExtractionResult model (OpenAI response_format requires all fields to be present)
        class ExtractionResult(BaseModel):
            thinking: str
            extracted: self.ExtractedData
            status: str
            action_type: str
            action_xpath: str

        self.ExtractionResultType = ExtractionResult

    def count_tokens(self, html: str, compact_html: str):
        html_tokens = len(self.tokenizer.encode(html))
        compact_tokens = len(self.tokenizer.encode(compact_html))
        ratio = round((html_tokens - compact_tokens) / html_tokens * 100, 2)
        print(f"HTML tokens: {html_tokens}")
        print(f"HTML compact tokens: {compact_tokens}")
        print(f"HTML compression ratio: {ratio}%\n")

        self.tokens["html"]["raw"] += html_tokens
        self.tokens["html"]["compressed"] += compact_tokens
        self.tokens["html"]["compression_ratio"] = round(
            (self.tokens["html"]["raw"] - self.tokens["html"]["compressed"])
            / self.tokens["html"]["raw"]
            * 100,
            2,
        )

    def extract_data_by_xpath(
        self, compressed_xpath: str, html: str, converter_maps: HtmlConverterMaps
    ) -> str:
        """
        Get the data from the HTML using the XPath
        @param compressed_xpath: The compressed XPath to use (from the LLM)
        @param html: The HTML content
        @param converter_maps: The converter maps from the emmetified HTML
        @return: The data from the HTML
        """
        full_xpath = restore_xpath_from_converter_maps(compressed_xpath, converter_maps)
        if full_xpath is None:
            print("Invalid XPath expression")
            return
        if full_xpath == "":
            print("Empty XPath expression")
            return ""

        try:
            tree = lxml_html.fromstring(html)
            results = list(set(tree.xpath(full_xpath)))
        except XPathEvalError as e:
            print(f"Invalid XPath expression: {e}")
            return None
        except ValueError as e:
            print(f"Invalid HTML content: {e}")
            return None

        if len(results) == 0:
            print("No data found")
            raise ExtractionError("No data found")

        return results[0]

    def get_url_from_xpath(
        self, current_url: str, compressed_xpath: str, html: str, converter_maps: HtmlConverterMaps
    ) -> str:
        url = self.extract_data_by_xpath(compressed_xpath, html, converter_maps)
        if url is None:
            print("Empty URL")
            return

        if url.startswith("/"):
            url = urllib.parse.urljoin(current_url, url)

        return url

    def run_llm(
        self, url: str, queries: dict[str, list[str]], emmetified_html: str
    ) -> Type[BaseModel]:
        completion = client.beta.chat.completions.parse(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": "\n".join(
                        [
                            f"Research count: {self.requests_count}/{self.max_count}",
                            f"Current URL: {url}",
                            f"Research history: {json.dumps(self.requests_history, indent=2, ensure_ascii=False)}",
                            f"Queries: {json.dumps(queries, indent=2, ensure_ascii=False)}",
                            f"HTML: {emmetified_html}",
                        ]
                    ),
                },
            ],
            response_format=self.ExtractionResultType,
        )
        self.tokens["llm"]["input"] += completion.usage.prompt_tokens
        self.tokens["llm"]["output"] += completion.usage.completion_tokens

        completion_result = completion.choices[0].message.parsed
        print(f"LLM response:\n{completion_result.model_dump_json(indent=2)}\n")
        return completion_result

    def update_extracted_data(self, extracted_data: dict[str, list[str]]) -> dict:
        for query_key, query_values in extracted_data.model_dump().items():
            if query_values is None or len(query_values) == 0:
                continue

            for index, value in enumerate(query_values):
                hash = hashlib.sha256(f"{query_key}_{index}_{value}".encode()).hexdigest()
                if hash in self.extracted_data_hash:
                    continue

                self.extracted_data_hash.append(hash)
                # save extracted data
                values: list[str] = self.extracted_data.get(query_key, [])
                values.append(value)
                self.extracted_data[query_key] = values
                # save query values
                self.requests_queries[query_key].append(value)

    def run_research(self) -> dict:
        if self.requests_count > self.max_count:
            print("Research limit reached")
            return

        current_url = self.requests_queue.pop(0)
        current_queries = self.requests_queries

        self.requests_count += 1
        print(f"--- Research {self.requests_count}/{self.max_count} ---")

        # Fetch the website
        try:
            req = requests.get(current_url)
            req.encoding = req.apparent_encoding
            current_html = req.text
        except Exception as e:
            print(f"Error fetching website: {e}")
            return

        # Compress the HTML
        emmetified = emmetify_compact_html(current_html)
        self.count_tokens(current_html, emmetified.result)

        llm_result = self.run_llm(current_url, current_queries, emmetified.result)

        # Handle stop action
        if llm_result.action_type == "stop":
            self.update_extracted_data(llm_result.extracted)
            print("Research completed")
            return self.extracted_data

        if llm_result.action_type == "terminate":
            self.update_extracted_data(llm_result.extracted)
            print("Research terminated")
            return self.extracted_data

        # Handle redirect action
        if llm_result.action_type == "redirect":
            redirect_url = self.get_url_from_xpath(
                current_url, llm_result.action_xpath, current_html, emmetified.maps
            )
            if redirect_url is None:
                print("Invalid redirect URL")
                return
            self.update_extracted_data(llm_result.extracted)
            print(f"Redirecting to: {redirect_url}")
            self.requests_queue.append(redirect_url)
            self.requests_history.append(current_url)
            self.run_research()


if __name__ == "__main__":
    ##############################################
    # Change the website and queries to your needs
    ##############################################
    website = "https://ycombinator.com"
    queries = ["What are the goals of the Y Combinator", "How to apply to Y Combinator"]

    print("----- STARTING RESEARCH -----")
    print("Website: ", website)
    print(f"Queries: {json.dumps(queries, indent=2)}\n")

    agent = WebExtractionAgent(max_count=5, start_url=website, queries=queries, model="gpt-4o")
    agent.run_research()

    print("----- RESEARCH COMPLETED -----")
    print(
        f"--- Extracted schema ---\n{json.dumps(agent.extracted_data, indent=2, ensure_ascii=False)}"
    )
    print(f"--- Tokens count ---\n{json.dumps(agent.tokens, indent=2, ensure_ascii=False)}")
