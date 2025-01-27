# Website Extraction Agent with OpenAI using Emmetify as a HTML compressor

This is a simple example of how to use Emmetify as a HTML compressor to extract data from websites using LLMs with up to 90% HTML compression ratio.

In this example we will use:
- Requests to fetch the HTML of a website
- Emmetify to compress the HTML
- OpenAI model to ask questions and do research about the website
- Make redirects to different pages using XPath selectors

Emmetify itself is only a HTML compressor, so it's up to you how to provide the HTML to it.
You can use requests to fetch the HTML from a website, or you can use a headless browsers like Playwright or Selenium to fetch the HTML.

## Run the code

Install the dependencies:

```bash
pip install emmetify requests openai python-dotenv tiktoken lxml
```

Run the code:

```bash
python openai-web-extraction-agent.py
```

If you want to use it on a different website or with different queries, you can change the `website ` and `queries` variables in the code at the end of the file.

