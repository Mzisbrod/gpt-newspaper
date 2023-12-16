# libraries

css = """
body {
    font-family: 'Times New Roman', serif;
    font-size: 18px;
    line-height: 1.6;
    color: #333;
    background-color: #fff;
    margin: 0;
    padding: 0;
}

.container {
    width: 80%;
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
}

.header {
    font-family: 'Georgia', serif;
    text-align: center;
    margin-bottom: 30px;
}

.header .title {
    font-size: 28px;
    font-weight: bold;
}

.header .subtitle {
    font-size: 20px;
    font-style: italic;
    color: #666;
}

.main-image {
    width: 100%;
    height: auto;
    display: block;
    margin: 0 auto 20px;
}

.article {
    margin-bottom: 20px;
}

.article .paragraph {
    margin-bottom: 15px;
}

.footer {
    text-align: center;
    font-size: 14px;
    color: #666;
    border-top: 1px solid #ddd;
    padding-top: 10px;
    margin-top: 30px;
}

@media screen and (max-width: 600px) {
    .container {
        width: 95%;
    }

    .header .title {
        font-size: 24px;
    }

    .header .subtitle {
        font-size: 18px;
    }
}

"""

import json
import os
from datetime import datetime

from tavily import TavilyClient
from langchain.adapters.openai import convert_openai_messages
from langchain.chat_models import ChatOpenAI

# Constants
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


# Search
def search(query: str):
    """
    Search for a query
    :param query:
    :return:
    """
    results = tavily_client.search(query=query, topic="news", max_results=10, include_images=True)
    return results


# Curate Relevant Sources
def curate_sources(query: str, sources: list, personal_details: str):
    """
    Curate relevant sources for a query
    :param query:
    :param sources:
    :return:
    """

    prompt = [{
        "role": "system",
        "content": "You are a personal newspaper editor. Your sole purpose is to choose 5 most relevant article for me to read from a list of articles.\n"
    }, {
        "role": "user",
        "content": f"Today's date is {datetime.now().strftime('%d/%m/%Y')}\n."
                   f"{personal_details}"
                   f"Your task is to return the 5 most relevant articles for me to read.\n"
                   f"Here is a list of articles:\n"
                   f"{sources}\n"
                   f"Please return nothing but a list of the strings of the URLs in this structure: ['url1','url2','url3','url4','url5'].\n"
    }]

    lc_messages = convert_openai_messages(prompt)
    response = ChatOpenAI(model='gpt-4', max_retries=1).invoke(lc_messages).content
    chosen_sources = response
    for i in sources:
        if i["url"] not in chosen_sources:
            sources.remove(i)
    return sources


def writer(query: str, sources: list, personal_details: str):
    """
    Curate relevant sources for a query
    :param query:
    :param sources:
    :return:
    """

    prompt = [{
        "role": "system",
        "content": "You are a newspaper writer. Your sole purpose is to write a well-written article about a topic using a list of articles.\n"
    }, {
        "role": "user",
        "content": f"Today's date is {datetime.now().strftime('%d/%m/%Y')}\n."
                   f"{personal_details}"
                   f"{sources}\n"
                   f"Your task is to write a critically acclaimed article for me based on the sources.\n"
                   f"Please return nothing but a string of the article.\n"
    }]

    lc_messages = convert_openai_messages(prompt)
    response = ChatOpenAI(model='gpt-4', max_retries=1).invoke(lc_messages).content
    return response


# designer
def designer(article: str, images: list):
    """
    Curate relevant sources for a query
    :param query:
    :param sources:
    :return:
    """

    prompt = [{
        "role": "system",
        "content": "You are a newspaper designer. Your sole purpose is to design a well-designed html to look like a New York Time Op-Ed.\n"
    }, {
        "role": "user",
        "content": f"Today's date is {datetime.now().strftime('%d/%m/%Y')}\n."
                   f"{article}\n"
                   f"Your task is to design an html for the article to look like a New York Times Op-Ed.\n"
                   f"please use one of these images you find most relevant based on the url:\n"
                   f"{images}\n"
                   f"Please return nothing but a FULL working html with the entire article so I can copy paste.\n"
                   f"use this css: {css}\n"
                   f"Your response:\n"

    }]

    lc_messages = convert_openai_messages(prompt)
    response = ChatOpenAI(model='gpt-4', max_retries=1).invoke(lc_messages).content
    return response


if __name__ == '__main__':

    query = "Latest updates on Harvard University president"

    personal_details = """
    I am a 20 year-old jewish Harvard student.
    I study economics and I am a member of the Harvard Republican Club.
    I love to play tennis and play the piano.
    """

    print(f"Step 1: Search for {query}\n")
    sources = search(query)["results"]
    images = search(query)["images"]
    print(f"Sources:")
    for i in sources:
        print(i["url"])
    print(f"\nImages:")
    for i in images:
        print(i)

    print(f"\nStep 2: Curate sources for {query}\n")
    context = curate_sources(query, sources, personal_details)
    for i in context:
        print(i["url"])

    print(f"\nStep 3: Write article for {query}\n")
    article = writer(query, context, personal_details)
    print(article)

    print(f"\n\nStep 4: Design article for {query}\n")
    html = designer(article, images)
    print(html)
