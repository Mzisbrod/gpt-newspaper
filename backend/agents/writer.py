from datetime import datetime
from langchain.adapters.openai import convert_openai_messages
from langchain_openai import ChatOpenAI
import json5 as json

sample_json = """
{
  "title": title of the article,
  "date": today's date,
  "paragraphs": [
    "paragraph 1",
    "paragraph 2",
    "paragraph 3",
    "paragraph 4",
    "paragraph 5",
    ],
    "summary": "2 sentences summary of the article"
}
"""


class WriterAgent:
    def __init__(self):
        pass

    def writer(self, query: str, sources: list):

        prompt = [{
            "role": "system",
            "content": "You are a newspaper writer. Your sole purpose is to write a well-written article about a "
                       "topic using a list of articles.\n "
        }, {
            "role": "user",
            "content": f"Today's date is {datetime.now().strftime('%d/%m/%Y')}\n."
                       f"Query or Topic: {query}"
                       f"{sources}\n"
                       f"Your task is to write a critically acclaimed article for me about the provided query or "
                       f"topic based on the sources.\n "
                       f"Please return nothing but a JSON in the following format:\n"
                       f"{sample_json}\n "

        }]

        lc_messages = convert_openai_messages(prompt)
        response = ChatOpenAI(model='gpt-4', max_retries=1).invoke(lc_messages).content
        return json.loads(response)

    def revise(self, article: dict):
        prompt = [{
            "role": "system",
            "content": "You are a newspaper editor. Your sole purpose is to edit a well-written article about a "
                       "topic based on given critique\n "
        }, {
            "role": "user",
            "content": f"{str(article)}\n"
                        f"Your task is to edit the article based on the critique given.\n "
                        f"Please return json format of the 'paragraphs' and a new 'message' field"
                        f"to the critique that explain your changes"
                       f"or why you didn't change anything.\n"

        }]

        lc_messages = convert_openai_messages(prompt)
        response = ChatOpenAI(model='gpt-4', max_retries=1).invoke(lc_messages).content
        print(response)
        return json.loads(response)

    def run(self, article: dict):
        critique = article.get("critique")
        if critique is not None:
            article.update(self.revise(article))
        else:
            article.update(self.writer(article["query"], article["sources"]))
        return article
