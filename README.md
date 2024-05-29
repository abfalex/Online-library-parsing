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

## Launch
To run, you need to enter the following command into the terminal:

```bash
python3 main.py -jp <json_path>
```

Instead of `json_path`, you need to specify the path to the json file with book details.

After launch, all you have to do is go to the address [127.0.0.1:5500](http://127.0.0.1:5500) and that’s it.