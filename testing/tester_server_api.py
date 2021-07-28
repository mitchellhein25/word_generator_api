#Source of inspiration: https://www.codementor.io/@sagaragarwal94/building-a-basic-restful-api-in-python-58k02xsiq
import re

import requests
from flask import Flask, request
from flask_restful import Resource, Api
import random

app = Flask(__name__)
api = Api(app)

def create_result_dict(search_phrase, related_words, status):
    return {"search_phrase": search_phrase, "related_words": related_words, "status": status}

def get_request_args(request):
    request_word_param = 'word'
    no_valid_word = "No valid search word was entered. Enter a search word in the format of word=SEARCH_PHRASE. Separate spaces in your phrase with a '+'"
    request_number_of_words_param = 'number_of_words'
    no_valid_number = "No valid number of words was entered. Enter a number of words in the format of number_of_words=NUMBER_OF_WORDS"
    invalid = 'invalid'

    try:
        word = request.args.get(request_word_param)
    except:
        return invalid, create_result_dict("", "", no_valid_word)

    try:
        number_of_words = int(request.args.get(request_number_of_words_param))
    except:
        return invalid, create_result_dict("", "", no_valid_number)

    return word, number_of_words

def get_related_words_from_api(word):
    response = requests.get(f'https://api.datamuse.com/words?ml={word}&md=fr')
    return response.json()

def get_status(response_length, number_of_words):
    status = ""
    if response_length == 0:
        status = "No search matches"
    elif response_length < number_of_words:
        status = "The number of available words was less than requested"
    elif response_length >= number_of_words:
        status = "Successful"
    return status

def get_number_of_words(response_length, number_of_words):
    if response_length < number_of_words:
        number_of_words = response_length
    return number_of_words

def get_random_num(response_length):
    return random.randint(0, response_length - 1)

def get_frequency_random_num(response_length, parsed_response):
    frequency_index = 2
    random_num = get_random_num(response_length)
    try:
        frequency = re.search(r'f:([\d\.]*)', parsed_response[random_num]['tags'][frequency_index])
    except:
        frequency = 0
    if frequency:
        frequency = float(frequency.group(1))
    else:
        frequency = 0
    return frequency, parsed_response[random_num]['word']

class WordGenerator(Resource):

    def get(self):
        word, number_of_words = get_request_args(request)

        if word == 'invalid':
            return number_of_words

        parsed_response = get_related_words_from_api(word)
        response_length = len(parsed_response)

        status = get_status(response_length, number_of_words)
        number_of_words = get_number_of_words(response_length, number_of_words)

        list_of_related_words = []
        if parsed_response != []:

            #Continue picking random words from the list of responses until list is full with number_of_words
            while len(list_of_related_words) < number_of_words:
                frequency, random_word = get_frequency_random_num(response_length, parsed_response)

                #If the returned phrase has a space or the frequency is less than 1 in a million
                while " " in random_word or frequency < 1:
                    frequency, random_word = get_frequency_random_num(response_length, parsed_response)

                #See if word is in the list already
                if random_word not in list_of_related_words:
                    for curr_word in list_of_related_words:

                        #Also check if the word is contained in an already chosen word (i.e. hair, haircut)
                        if random_word in curr_word:
                            continue

                    list_of_related_words.append(random_word)

        return {"search_phrase": word, "related_words": list_of_related_words, "status": status}

api.add_resource(WordGenerator, '/word_generator')

if __name__ == '__main__':
    app.run(port=5000, ssl_context='adhoc')