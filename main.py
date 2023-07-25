#!/usr/bin/env python3

import json
import requests

from bs4 import BeautifulSoup
from datetime import datetime


def get_response(url: str):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Unknown Error: {err}")
    else:
        return response


def parse_date(date_str: str):
    dt = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%fZ')
    return dt.strftime('%B %d, %Y')


def find_answers():
    url = 'https://www.dailydozentrivia.com'
    response = get_response(url)

    if response:
        soup = BeautifulSoup(response.text, 'html.parser')
        script_tag = soup.find('script', {'id': '__NEXT_DATA__'})

        data = json.loads(script_tag.string)

        game_date = parse_date(data["props"]["pageProps"]["dailyGame"]["gameDate"])
        daily_questions = data["props"]["pageProps"]["dailyQuestions"]

        print(f"Today's game date is {game_date} and the answers are:\n")
        for question in daily_questions:
            cat = question["questionCategory"]["name"]
            answers = [answer["answerText"] for answer in question["answers"]]

            print(f"Category : {cat}")
            for ans in answers:
                print(f"    Answer : {ans}")


if __name__ == "__main__":
    find_answers()
