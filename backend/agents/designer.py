
class DesignerAgent:
    def __init__(self):
        pass

    def load_html_template(self):
        with open("/Users/rotemweiss/Desktop/gpt-newspaper/backend/templates/article/index.html") as f:
            html_template = f.read()
        return html_template

    def designer(self, article):
        html_template = self.load_html_template()
        title = article["title"]
        date = article["date"]
        image = article["image"]
        paragraphs = article["paragraphs"]
        html_template = html_template.replace("{{title}}", title)
        html_template = html_template.replace("{{image}}", image)
        html_template = html_template.replace("{{date}}", date)
        for i in range(5):
            html_template = html_template.replace(f"{{paragraph{i+1}}}", paragraphs[i])
        return html_template

    def run(self, article):
        return self.designer(article)


