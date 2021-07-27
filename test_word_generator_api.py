import requests

BASE = "http://127.0.0.1:5555/"

response = requests.get(BASE + "word_generator?word=dog&number_of_words=3")
print(response)
print(response.json())