import argparse
import os
import json
import time
import logging
import requests
from urllib.parse import urljoin, unquote, urlsplit
from pathvalidate import sanitize_filename
from bs4 import BeautifulSoup
from requests import HTTPError

logger = logging.getLogger(__name__)


def check_redirect(response):
    if response.history:
        raise HTTPError(f"A redirect has occurred.")


def get_response(url, params=None):
    res = requests.get(url, params=params)
    res.raise_for_status()
    check_redirect(res)
    return res


def download_book_text(book_text, book_title, folder):
    save_book_path = os.path.join(folder, book_title)

    with open(save_book_path, "w", encoding="UTF-8") as f:
        f.write(book_text)


def download_content(url, folder):
    res = get_response(url)

    filename = os.path.basename(unquote(urlsplit(url).path))
    file_path = os.path.join(folder, filename).replace("\\", "/")

    with open(file_path, "wb") as f:
        f.write(res.content)

    return file_path


def parse_page_book(page_content, book_url):
    soup = BeautifulSoup(page_content, 'lxml')

    book_content = soup.select_one("div#content h1").text.split(" :: ")
    book_image_path = soup.select_one("div.bookimage img")['src']
    genres_elements = soup.select("span.d_book a")
    comments_elements = soup.select("div.texts")

    title = book_content[0].strip()
    author = book_content[1].strip()
    genres = [genre.text for genre in genres_elements]
    cover_url = urljoin(book_url, book_image_path)
    text_comments = [comment.select_one("span").text for comment in comments_elements]

    book = {
        "title": title,
        "author": author,
        "genres": genres,
        "cover_url": cover_url,
        "text_comments": text_comments
    }

    return book


def create_folders(dest_folder):
    os.makedirs(dest_folder, exist_ok=True)
    images_folder = f"{dest_folder}/covers"
    books_folder = f"{dest_folder}/books_txt"

    for folder in (images_folder, books_folder):
        os.makedirs(folder, exist_ok=True)

    return images_folder, books_folder


def get_book_urls(page_url):
    res = get_response(page_url)
    soup = BeautifulSoup(res.text, 'lxml')
    page_books = soup.select("table.d_book")

    books_urls = []
    for page_book in page_books:
        book_id = page_book.select_one("a")['href']
        books_urls.append(urljoin(page_url, book_id))

    return books_urls


def parse_book(parsing_details):
    skip_images = parsing_details.get("skip_images")
    skip_books = parsing_details.get("skip_books")
    book_url = parsing_details.get("book_url")
    book_counter = parsing_details.get("book_counter")
    images_folder = parsing_details.get("images_folder")
    books_folder = parsing_details.get("books_folder")
    book_id = parsing_details.get("book_id")

    book_text_url = "https://tululu.org/txt.php"
    params = {"id": book_id}

    res = get_response(book_url)
    book_text = get_response(book_text_url, params).text
    book_details = parse_page_book(res.text, book_url)

    book_cover_url = book_details.get("cover_url")
    book_title = book_details.get("title")

    sanitize_book_name = sanitize_filename(f"{book_title}.txt")
    book_filename = f"{book_counter}. {sanitize_book_name}"
    cover_path = ""
    book_path = ""

    if not skip_images:
        cover_path = download_content(book_cover_url, images_folder)

    if not skip_books:
        book_path = os.path.join(books_folder, book_filename).replace("\\", "/")
        download_book_text(book_text, book_filename, books_folder)

    if skip_images and skip_books:
        return logging.info("The process is complete because there is nothing to download.")

    return {
        "title": book_title,
        "author": book_details.get("author"),
        "cover_path": cover_path,
        "book_path": book_path,
        "genres": book_details.get("genres", []),
        "text_comments": book_details.get("text_comments", [])
    }


def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s %(message)s")

    parser = argparse.ArgumentParser(
        prog="LibraryParsing",
        description="Downloads books and their covers from the online library tululu.org",
    )

    parser.add_argument(
        '-s', '--start_id',
        help='The ID of the page from which to start downloading books.',
        type=int,
        default=1
    )

    parser.add_argument(
        '-e', '--end_id',
        help='ID of the page until which the books need to be downloaded books',
        type=int,
        default=10
    )

    parser.add_argument(
        '-df', '--dest_folder',
        help='Path to the directory with analysis results: pictures, books, JSON',
        type=str,
        default="books"
    )

    parser.add_argument(
        '-si', '--skip_imgs',
        help='Ignore covers downloading',
        action="store_true"
    )

    parser.add_argument(
        '-st', '--skip_txt',
        help='Ignore book downloading',
        action="store_true"
    )

    args = parser.parse_args()

    start_page_number = args.start_id
    end_page_number = args.end_id
    dest_folder = args.dest_folder
    skip_images = args.skip_imgs
    skip_books = args.skip_txt

    images_folder, books_folder = create_folders(dest_folder)
    json_path = f"{dest_folder}/books.json"

    book_counter = len(os.listdir(books_folder)) + 1
    books = []

    for page_number in range(start_page_number, end_page_number + 1):
        while True:
            try:
                page_url = f"https://tululu.org/l55/{page_number}/"
                books_urls = get_book_urls(page_url)
                break

            except requests.exceptions.ConnectionError:
                logger.info(f"Connection error, trying to reconnect...")
                time.sleep(3.5)

            except HTTPError:
                logger.info(f"Page with ID {page_number} not found.")
                break

        for book_url in books_urls:
            book_id = book_url.split("/")[-2].strip("b")
            while True:
                try:
                    parsing_details = {
                        "book_url": book_url,
                        "skip_images": skip_images,
                        "skip_books": skip_books,
                        "book_counter": book_counter,
                        "dest_folder": dest_folder,
                        "images_folder": images_folder,
                        "books_folder": books_folder,
                        "book_id": book_id
                    }

                    book_details = parse_book(parsing_details)

                    books.append(book_details)
                    book_counter += 1
                    logger.info(f"Book with ID {book_id} was successfully downloaded.")
                    break

                except requests.exceptions.ConnectionError:
                    logger.info(f"Connection error, trying to reconnect...")
                    time.sleep(3.5)

                except HTTPError:
                    logger.info(f"Book with ID {book_id} not found.")
                    break

    with open(json_path, "w", encoding="UTF-8") as f:
        json.dump(books, f, indent=3, ensure_ascii=False)


if __name__ == "__main__":
    main()
