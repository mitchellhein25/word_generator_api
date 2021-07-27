#Source of inspiration: https://www.codementor.io/@sagaragarwal94/building-a-basic-restful-api-in-python-58k02xsiq
import requests
from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class WordGenerator(Resource):
    def get(self):
        print(type(request.args))
        args = request.args
        word = args.get('word')
        number_of_words = args.get('number_of_words')

        response = requests.get(f'https://api.datamuse.com/words?rel_trg={word}')
        print(response)

        list_of_related_words = []

        for x in range(int(number_of_words)):
            list_of_related_words.append(response.json()[x]['word'])
            print(list_of_related_words)
        return list_of_related_words

api.add_resource(WordGenerator, '/word_generator')

if __name__ == '__main__':
    app.run()