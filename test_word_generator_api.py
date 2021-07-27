import requests

BASE = "https://peaceful-harbor-63265.herokuapp.com/"

response = requests.get(BASE + "word_generator?word=dog&number_of_words=3")
print(response)
print(response.json())