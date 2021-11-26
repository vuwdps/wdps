from bs4 import BeautifulSoup
import requests
import spacy

# html_doc = """<html><head><title>The Dormouse's story</title></head>
# <body>
# <p class="title"><b>The Dormouse's story</b></p>

# <p class="story">Once upon a time there were three little sisters; and their names were
# <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
# <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
# <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
# and they lived at the bottom of a well.</p>

# <p class="story">...</p>
# """

# soup = BeautifulSoup(html_doc, 'html.parser')


testfile = open('data\sample-labels-cheat.txt', 'r')
testfile = testfile.readline().split('\t')
url = testfile[1]
url = url[1:-2]
site = requests.get(url).text
soup = BeautifulSoup(site, 'html.parser')

print(soup.get_text())

nlp = spacy.load("en_core_web_sm")
doc = nlp("This is a sentence.")
print([(w.text, w.pos_) for w in doc])
