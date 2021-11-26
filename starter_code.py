import gzip
import requests
import json
from elasticsearch import Elasticsearch
from bs4 import BeautifulSoup
import spacy

dbapi = "https://api.dbpedia-spotlight.org/en/"
KEYNAME = "WARC-TREC-ID"

# The goal of this function process the webpage and returns a list of labels -> entity ID
def find_labels(payload):
    if payload == '':
        return

    #soup parser
    
    # The variable payload contains the source code of a webpage and some additional meta-data.
    # We firt retrieve the ID of the webpage, which is indicated in a line that starts with KEYNAME.
    # The ID is contained in the variable 'key'
    key = None
    for line in payload.splitlines():
        if line.startswith(KEYNAME):
            key = line.split(': ')[1]
            break

    print(key)
    namedEntity_list = {}
    extractedText = BeautifulSoup(payload, 'html.parser')
    extractedText = extractedText.get_text().replace("\n", " ")
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(extractedText)
    
    false_entities = ("DATE", "TIME", "PERCENT", "MONEY", "QUANTITY", "ORDINAL", "CARDINAL")
    for i in doc.ents:
        if i.label_ not in false_entities:
            namedEntity_list[i.text] = i.label_
    print(namedEntity_list)
    # response = requests.get(dbapi + "candidates?text="+extractedText)
    # print('candidate text', response.content)
    # es_results = search("Cola")
    # print(es_results)
    cheats = dict((line.split('\t', 2) for line in open('data/sample-labels-cheat.txt').read().splitlines()))
    for label, wikidata_id in cheats.items():
        if key and (label in payload):
            yield key, label, wikidata_id

def search(query):
    e = Elasticsearch(['http://fs0.das5.cs.vu.nl:10010'])
    p = { "query" : { "query_string" : { "query" : query }}}
    response = e.search(index="wikidata_en", body=json.dumps(p))
    id_labels = {}
    if response:
        for hit in response['hits']['hits']:
            label = hit['_source']['schema_name']
            id = hit['_id']
            id_labels.setdefault(id, set()).add(label)
    return id_labels

def split_records(stream):
    payload = ''
    for line in stream:
        if line.strip() == "WARC/1.0":
            yield payload
            payload = ''
        else:
            payload += line
    yield payload

if __name__ == '__main__':
    import sys
    try:
        _, INPUT = sys.argv
    except Exception as e:
        print('Usage: python starter-code.py INPUT')
        sys.exit(0)

    with gzip.open(INPUT, 'rt', errors='ignore') as fo:
        for record in split_records(fo):
            for key, label, wikidata_id in find_labels(record):
                # print(key + '\t' + label + '\t' + wikidata_id)
                pass
