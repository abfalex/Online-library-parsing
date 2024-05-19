from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import json

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

def render_website():
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
    render_website()

    server = HTTPServer(('0.0.0.0', 8004), SimpleHTTPRequestHandler)
    server.serve_forever()