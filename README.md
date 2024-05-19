# Parsing online library tululu.org
This project will help the user to download books with covers from the online library [tululu.org](https://tululu.org/).

The code loads the text of books with their covers from pages in the specified range. You can choose the range of pages yourself, and also skip downloading covers or texts of books (all optional).

## Installation
Before installation, make sure you have [Python](https://www.python.org/) 3.x installed

To work with a project, you need to install or clone it.

Use the following command in terminal to clone:

```bash
git clone https://github.com/abfalex/Online-library-parsing.git
```

Next, you need to create a virtual environment for easy use (recommended):

   ```bash
   python -m venv <venv_name>
   ```

After installing the virtual environment, you need to activate it:

  - On Windows:

     ```bash
     <venv_name>\Scripts\activate
     ```

- On macOS and Linux:

     ```bash
     source <venv_name>/bin/activate
     ```

After, you need to install the necessary libraries. Enter this command into the terminal:

```bash
pip install -r requirements.txt
```

## Launch
To run, you need to enter the following command into the terminal:

```bash
python3 main.py
```

### Arguments
By default, the book page ID range is from 1 to 10. This means that only the first 10 pages of the book will be loaded.

`--start_id` - ID of the page from which the download of books will begin (default 1).

 `--end_id` is the identifier of the page where you want to download books (default 10).

`--dest_folder` - the folder in which the parsing result will be saved (text of books, their covers and the main json file) (default "books").

`--skip_imgs` - specify this argument if you want to skip downloading book covers.

`--skip_txt` - specify this argument if you want to skip downloading books.

Usage example:

```bash
python3 main.py --start_id 2 --end_id 10
```

In the example above, we specified a range from 2 to 10. It turns out that books and their covers will be downloaded from pages in the specified range into the book and images folders.

Another example:

```bash
python3 main.py --start_id 1 --end_id 3 --skip_imgs
```

In this example, books WITHOUT COVERS will be downloaded (because we used the `--skip_imgs` arg) from pages in the range from 1 to 3.

It is worth remembering that some books are missing or hidden. Books will be numbered as they are downloaded, so the number of books will vary from the range shown.