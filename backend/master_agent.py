import os
import time
from threading import Thread
from .agents import SearchAgent, WriterAgent, CuratorAgent, DesignerAgent, EditorAgent

class MasterAgent:
    def __init__(self):
        self.search_agent = SearchAgent()
        self.curator_agent = CuratorAgent()
        self.writer_agent = WriterAgent()
        self.designer_agent = DesignerAgent()
        self.output_dir = f"outputs/run_{int(time.time())}"
        self.editor_agent = EditorAgent(self.output_dir)
        os.makedirs(self.output_dir, exist_ok=True)

    def save_article_html(self, article, query):
        filename = f"{query.replace(' ', '_')}.html"
        path = os.path.join(self.output_dir, filename)
        with open(path, 'w') as file:
            file.write(article['html'])
        return filename

    def produce_report(self, query: str, results: list):
        sources, image = self.search_agent.run(query)
        context = self.curator_agent.run(query, sources)
        article = self.writer_agent.run(query, context)
        article["image"] = image
        article["html"] = self.designer_agent.run(article)
        article["path"] = self.save_article_html(article, query)
        results.append(article)

    def run(self, queries: list):
        results = []
        threads = []

        for query in queries:
            thread = Thread(target=self.produce_report, args=(query, results))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        newspaper_path = self.editor_agent.run(results)
        return newspaper_path
