import gzip
import requests
import json
from elasticsearch import Elasticsearch, ElasticsearchException
from bs4 import BeautifulSoup
import spacy
import urllib
import math



HOST = "http://fs0.das5.cs.vu.nl:10011/sparql"

def sparqlQuery(query, format="application/json"):
    resp = requests.get(HOST + "?" + urllib.parse.urlencode({
        "default-graph": "",
        "should-sponge": "soft",
        "query": query,
        "debug": "on",
        "timeout": "",
        "format": format,
        "save": "display",
        "fname": ""
    }))

    return json.loads(resp.content.decode("utf-8"))





a=1
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

    namedEntity_list = {}
    extractedText = BeautifulSoup(payload, 'html.parser')
    
    extractedText = extractedText.get_text().replace("\n", " ")
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(extractedText)
    false_entities = ("DATE", "TIME", "PERCENT", "MONEY", "QUANTITY", "ORDINAL", "CARDINAL")
    false_labels = ("WARC-Type","WARC-Date","clueweb12","WARC-IP-Address","WARC-Target-URI","Content-Type","GMT Cache-Control","§","ORG","OpenSSL/0.9.8e","ACCEPT",\
        "WARC Format 1.0 specification","WARC Format 1.1 specification","WARC 1.1","WARC","WARC 1.0","WARC-Payload-Digest:","Content-Length","GMT Server",\
        "Apache X-Powered-By","sha1","Accept-Encoding","WARC-Filename","WARC-File-Length","WARC-Data-Type","WARC-Record-ID","WARC File Format","WARC","WARC bands","WARC Format 1.0 specification")
    
    for i in doc.ents:
            if i.label_ not in false_entities and i.text not in false_labels:
                namedEntity_list[i.text] = i.label_
    
    result = {}
    print(namedEntity_list)
    for keyent in namedEntity_list:
            es_results=search(keyent)
            print(es_results)
            if es_results:
                for hit in es_results['hits']['hits']:
                    if 'schema_name' in hit['_source']:
                        label = hit['_source']['schema_name']
                        id = hit['_id']
                        score = hit['_score']

                        if result.get(label):
                            change_score = max(result[label]['score'], score)
                            result[label]['score'] = change_score

                        result[label]= ({
                                'id': id,
                                'score':score,
                                'rank': 0
                            })

                        query = "select distinct * where {"+id+" ?pred ?obj.}"
                        sparqlQuerydata = sparqlQuery(query)
                        if sparqlQuerydata['results']:
                            bindings = sparqlQuerydata['bindings']
                            result[label]['rank'] = math.log(len(bindings)) * result[label]['score']

            if result.items is not None:
                result = sorted(result.items(), key=lambda i: (i[1]['rank']), reverse=True)

                        # if sparqlQuerydata:
                        #     n = int()
    
                     

        # response = requests.get(dbapi + "candidates?text="+extractedText)
        # print('candidate text', response.content)
        # es_results = search("Cola")
        # print(es_results)
    
    for label, id in result.items():
                yield key, label, wikidata_id

def search(query):
    e = Elasticsearch(['http://fs0.das5.cs.vu.nl:10010'])
    p = { "query" : { "query_string" : { "query" : query }}}
    try:
        response = e.search(index="wikidata_en", body=json.dumps(p))
        return response
    except ElasticsearchException as e:
        pass

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
