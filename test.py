from SPARQLWrapper import SPARQLWrapper
import json

queryString = "SELECT * WHERE { ?s ?p ?o. }"
sparql = SPARQLWrapper("http://example.org/sparql")

sparql.setQuery(queryString)

# try:
# ret = sparql.query()
# ret is a stream with the results in XML, see <http://www.w3.org/TR/rdf-sparql-XMLres/>
# except:
#     print('hei')


KBPATH = SPARQLWrapper(
    'file:///E:/WDPS/assignment-no-elasticsearch-splitted2/assignment-no-elasticsearch-splitted/assignment/assets/wikidata-20200203-truthy-uri-tridentdb/')
query = "PREFIX wde: <http://www.wikidata.org/entity/> "\
    "PREFIX wdp: <http://www.wikidata.org/prop/direct/> "\
    "PREFIX wdpn: <http://www.wikidata.org/prop/direct-normalized/> "\
    "select ?s where { ?s wdp:P31 wde:Q515 . } LIMIT 10"
KBPATH.setQuery(query)

res = KBPATH.query().convert()
json_results = json.loads(res)


print("*** VARIABLES ***")
variables = json_results["head"]["vars"]
print(variables)

print("\n*** BINDINGS ***")
results = json_results["results"]
for b in results["bindings"]:
    line = ""
    for var in variables:
        line += var + ": " + b[var]["value"] + " "
    print(line)

print("\n*** STATISTICS ***")
print(json_results['stats'])
