# Parsing online library tululu.org

This project offers an online library based on books taken from the online library [tululu.org](https://tululu.org/).

## Demo

To demonstrate the website, please follow the following link:
https://abfalex.github.io/Online-library-parsing/pages/index1.html

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

## Launching a website offline

To launch a website offline you need:

- In the project repository, find the code button

- Download a copy of the project, through the archive or via the link

- Open the downloaded project

Go to the pages folder and:

- Run file index1.html

Also in the media folder you can find downloaded book covers and the books themselves in text format.

## Launch via code

To run, you need to enter the following command into the terminal:

```bash
python3 render_website.py -jp <json_path>
```

Instead of `json_path`, you need to specify the path to the json file with book details. All data is stored along the path: `media/books.json`.

Example:

```bash
python render_website.py -jp media/books.json
```

Since the current path to the parts file is the default, the argument is optional. It exists so that you can specify the desired path yourself, if necessary.

After launch, all you have to do is go to the address [127.0.0.1:5500](http://127.0.0.1:5500) and that’s it.