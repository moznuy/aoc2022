import argparse
import os
import sys

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv


load_dotenv()

SESSION = os.environ["COOKIE_SESSION"]
YEAR = os.environ["YEAR"]
DAY = os.environ["DAY"]
LEVEL = os.environ["LEVEL"]
print(f"{YEAR=} {DAY=} {LEVEL=}")


def download():
    url = f"https://adventofcode.com/{YEAR}/day/{DAY}/input"
    response = requests.get(url, cookies={"session": SESSION})
    response.raise_for_status()
    with open("input.txt", "wb") as file:
        file.write(response.content)


def upload():
    answer = input().strip()
    url = f"https://adventofcode.com/{YEAR}/day/{DAY}/answer"
    data = {
        "level": LEVEL,
        "answer": answer,
    }
    response = requests.post(url, cookies={"session": SESSION}, data=data)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")
    print(soup.article.p.text, file=sys.stderr)


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("download")
    subparsers.add_parser("upload")
    args = parser.parse_args()
    globals()[args.command]()


if __name__ == "__main__":
    main()
