import os
import json
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked


env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

def on_reload():
    page_directory = "pages"

    os.makedirs(page_directory, exist_ok=True)

    page_template = env.get_template('page_template.html')
    json_path = "assets/books/books.json"

    with open(json_path, "r", encoding="UTF-8") as f:
        json_file = f.read()

    books_details = json.loads(json_file)
    books_per_column = 8
    book_groups = list(chunked(books_details, 2))
    pages_groups = list(chunked(book_groups, books_per_column))

    for page_number, pages_group in enumerate(pages_groups, start=1):
        page_output_path = os.path.join(page_directory, f"index{page_number}.html")

        rendered_page_template = page_template.render(
            pages_group=pages_group,
            page_number=page_number,
            total_pages=len(pages_groups)
        )

        with open(page_output_path, "w", encoding="UTF-8") as f:
            f.write(rendered_page_template)


if __name__ == "__main__":
    on_reload()
    
    server = Server()
    server.watch("page_template.html", on_reload)
    server.serve(root='.')