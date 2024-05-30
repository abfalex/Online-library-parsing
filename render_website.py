import os
import json
import argparse

from more_itertools import chunked
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server


def on_reload():
    parser = argparse.ArgumentParser(
        description="The program receives data about books that will be displayed on the web pages"
    )
    parser.add_argument(
        "-jp",
        "--json_path",
        type=str,
        help="Path to the json file with book details",
        default="media/books.json"
    )
    args = parser.parse_args()
    json_path = args.json_path

    env = Environment(
        loader=FileSystemLoader("."),
        autoescape=select_autoescape(["html", "xml"])
    )
    template = env.get_template("template.html")

    pages_directory = "pages"
    os.makedirs(pages_directory, exist_ok=True)
    
    with open(json_path, "r", encoding="UTF-8") as f:
        books_details = json.load(f)

    book_number_columns = 8
    row_books_number = 2
    book_groups = list(chunked(books_details, row_books_number))
    pages_groups = list(chunked(book_groups, book_number_columns))

    for page_number, pages_group in enumerate(pages_groups, start=1):
        page_output_path = os.path.join(pages_directory, f"index{page_number}.html")
        rendered_page_template = template.render(
            pages_group=pages_group,
            page_number=page_number,
            total_pages=len(pages_groups)
        )
        with open(page_output_path, "w", encoding="UTF-8") as f:
            f.write(rendered_page_template)

if __name__ == "__main__":
    on_reload()
    server = Server()
    server.watch("template.html", on_reload)
    server.serve(root=".", default_filename="pages/index1.html")