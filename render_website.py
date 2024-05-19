from jinja2 import Environment, FileSystemLoader, select_autoescape
import json
from livereload import Server


env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

def on_reload():
    template = env.get_template('template.html')
    json_path = "assets/books/books.json"

    with open(json_path, "r", encoding="UTF-8") as f:
        json_file = f.read()

    books_details = json.loads(json_file)

    rendered_page = template.render(
        books=books_details
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)


if __name__ == "__main__":
    on_reload()
    
    server = Server()
    server.watch("template.html", on_reload)
    server.serve(root='.')