import csv
from bisect import bisect_left

from requests import Session

GUESS_URL = "https://ordgissel.se/gissa"
RESULT_URL = "https://ordgissel.se/resultat"
NAME = "Erik Berglund Jr."
WORDLIST = "saol2018.csv"


def read_word_list_file():
    with open(WORDLIST) as file:
        csv_reader = csv.reader(file)
        return [row[1] for row in csv_reader if not row[1].startswith("-")]


class WordSearch:
    def __init__(self, session):
        self.session = session
        self.done = False
        self.guesses = 0

    def __gt__(self, other):
        if self.done:
            return False
        response = self.session.post(GUESS_URL, {"word": other}).json()
        self.guesses += 1
        self.session_id = response["session_id"]
        result = response["result"]
        if result == "correct":
            self.done = True
            self.found = other
        return result != "after"


if __name__ == '__main__':
    guess_session = Session()
    word_search = WordSearch(guess_session)
    word_list = read_word_list_file()
    bisect_left(word_list, word_search)
    r = guess_session.post(RESULT_URL, {
        "name": NAME,
        "session_id": word_search.session_id
    })

    print(f"Found today's word '{word_search.found}'"
          f" after {word_search.guesses} guesses!")
    print("See result on: " + RESULT_URL)
