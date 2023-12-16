import os

class EditorAgent:
    def __init__(self, output_dir):
        self.output_dir = output_dir

    def load_html_template(self):
        with open("/Users/rotemweiss/Desktop/gpt-newspaper/backend/templates/newspaper/index.html") as f:
            html_template = f.read()
        return html_template

    def save_newspaper_html(self, newspaper_html):
        path = os.path.join(self.output_dir, "newspaper.html")
        with open(path, 'w') as file:
            file.write(newspaper_html)
        return path


    def editor(self, articles):
        html_template = self.load_html_template()
        article_template = """
        <div class="article">
            <a href="{{path}}" target="_blank"><h2>{{title}}</h2></a>
            <img src="{{image}}" alt="Article Image">
            <p class="date">{{date}}</p>
            <p>{{summary}}</p>
        </div>
        """
        articles_html = ""
        for article in articles:
            article_html = article_template.replace("{{title}}", article["title"])
            article_html = article_html.replace("{{image}}", article["image"])
            article_html = article_html.replace("{{date}}", article["date"])
            article_html = article_html.replace("{{summary}}", article["summary"])
            article_html = article_html.replace("{{path}}", article["path"])
            articles_html += article_html

        newspaper_html = html_template.replace("{{articles}}", articles_html)
        return self.save_newspaper_html(newspaper_html)

    def run(self, articles):
        return self.editor(articles)
