# UKPOL

## Python Instillation

Python 3 should be installed. Check with:
`python --version`

If python3 is installed but "python" command is pointing to a native python 2 installation, you can alias python3 to python by appending the following to ~/.bashrc
`alias python=python3`

## Initialise Git Repo (personal account)

## Setup up virtual environment with venv

It can be useful to use a virtual environment to keep project dependancies separate from your systems python installation. Once setup - any third party python libraries installed will be kept locally in the environment.

https://docs.python.org/3/library/venv.html

Read the docs. I set this up with the following
`python -m venv venv`

To activate virtual environment
`source venv/bin/activate`

## (Option 1)

Install required packages (there will be more to come). We’ll be using bs4 to scrape content from the web.
https://www.crummy.com/software/BeautifulSoup/bs4/doc/
`pip install requests`
`pip install beautifulsoup4`

Keep track of projects requirements in a requirements.txt file. Here’s a useful article to explain why
https://blog.usejournal.com/why-and-how-to-make-a-requirements-txt-f329c685181e
`pip freeze > requirements.txt`

## (Option 2)

Clone my repo and install requirements with

`pip install -r requirements.txt`
