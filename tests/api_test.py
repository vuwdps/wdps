import requests

api = "https://api.dbpedia-spotlight.org/en/"

response = requests.get(
    api + "candidates?text=apple+company+macintosh+computer")
# print('res', response)
print('candidate text', response.content)
# print('headers', response.headers['date'])
# print('content', response.content)
# print('json', response.json)

print('===================')
res = requests.get(api+'candidates?text=Rosa+rubiginosa')
print('candidates:', res.text)

print('===================')

res = requests.get(api+'annotate?text=Rosa+rubiginosa')
print('annotate text', res.headers)

print('===================')

# blacklist - select all entities that are not the same type
res = requests.get(
    api+"annotate?text=cake&url=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FCake&policy=blacklist")
print('blacklist', res.text)
