import os

import requests
from dotenv import load_dotenv

load_dotenv()


def download():
    session = os.environ['COOKIE_SESSION']
    day = int(input("Day: "))
    url = f'https://adventofcode.com/2022/day/{day}/input'
    response = requests.get(url, cookies={'session': session})
    response.raise_for_status()
    with open('input.txt', 'wb') as file:
        file.write(response.content)


if __name__ == '__main__':
    download()
