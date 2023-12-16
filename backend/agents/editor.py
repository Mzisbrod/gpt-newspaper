

class EditorAgent:
    def __init__(self):
        pass

    def load_html_template(self):
        with open("/Users/rotemweiss/Desktop/gpt-newspaper/backend/templates/newspaper/index.html") as f:
            html_template = f.read()
        return html_template

    def editor(self, articles):
        html_template = self.load_html_template()
        for i in range(5):
            html_template = html_template.replace(f"{{title{i+1}}}", articles[i]["title"])
            html_template = html_template.replace(f"{{image{i+1}}}", articles[i]["image"])
            html_template = html_template.replace(f"{{date{i+1}}}", articles[i]["date"])
            html_template = html_template.replace(f"{{summary{i+1}}}", articles[i]["summary"])
        return html_template

    def run(self, articles):
        return self.editor(articles)


