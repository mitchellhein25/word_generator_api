import requests

response = requests.get('https://api.datamuse.com/words?rel_trg=dog')

print(response.json())