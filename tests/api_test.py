import requests

api = "https://api.dbpedia-spotlight.org/en/"

response = requests.get(
    api + "candidates?text=apple+company+macintosh+computer")
# print('res', response)
# print('candidate text', response.content)
# print('headers', response.headers['date'])
# print('content', response.content)
# print('json', response.json)

print('===================')
res = requests.get(api+'candidates?text=Rosa+rubiginosa')
# print('candidates:', res.text)

print('===================')

res = requests.get('https://api.dbpedia-spotlight.org/en/candidates?text=Modern-day%20Jordan%20has%20been%20inhabited%20by%20humans%20since%20the%20Paleolithic%20period.%20Three%20stable%20kingdoms%20emerged%20there%20at%20the%20end%20of%20the%20Bronze%20Age%3A%20Ammon%2C%20Moab%20and%20Edom.%20Later%20rulers%20include%20the%20Nabataean%20Kingdom%2C%20the%20Persian%20Empire%2C%20the%20Roman%20Empire%2C%20the%20Rashidun%2C%20Umayyad%2C%20and%20Abbasid%20Caliphates%2C%20and%20the%20Ottoman%20Empire.%20Af')
# print('annotate text', res.text)

print('===================')

# blacklist - select all entities that are not the same type
res = requests.get(
    api+"spot?text=cake&url=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FCake&policy=whitelist")
# print('blacklist', res.text)

res = requests.get(api + 'candidates?text=Georgia&types=country')
print(res.text)
print(res.content)
print(res.history)

res = requests.get(api + 'candidates?text=Georgia&types=place&confidence=0.2')
print(res.text)
print(res.content)
print(res.history)
