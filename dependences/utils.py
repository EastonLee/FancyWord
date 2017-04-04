import json
from urllib.request import Request
from urllib.request import urlopen
from urllib.error import HTTPError
url = "http://127.0.0.1:5000/word2vec/most_similar?positive=test&topn=10"
req = Request(url, None)
try:
    page = urlopen(req)
    html = page.read()
    page.close()
    print(json.loads(html))
except Exception as e:
    print(e)
    print([])

from subprocess import Popen
Popen(['python', '~/Downloads/word2vec-api/word2vec-api.py', '--model', '~/Downloads/deps.words.bin', '--binary', 'true'])
from pkgutil import extend_path

from nltk.corpus import wordnet as wn
definitions = [(w.name(), w.definition()) for w in wn.synsets('dog')]
print(definitions)
syns = {i.name() for i in {w for w in wn.synsets('course')}}
print(syns)
