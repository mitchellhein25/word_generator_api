import requests

# BASE = "https://related-word-generator.herokuapp.com/"
BASE = "https://127.0.0.1:5000/"

response = requests.get(BASE + "word_generator?word=happy&number_of_words=10", verify=False)
print(response)
print(response.json())