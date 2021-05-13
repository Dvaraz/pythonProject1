import json
from random import choice, randint, random
import re
import argparse

import conf


def create_sub_parser(parser):
    subparser = parser.add_subparsers(dest="command")
    output_format = subparser.add_parser("output_format")
    output_format.add_argument("-o", required=True, help="enter format json or csv")


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-count", help="number of elements to generate")
    parser.add_argument("-authors", default=randint(1, 3), type=int, help="number of authors,default = random from 1 to 3")
    create_sub_parser(parser)
    return parser


def title(file_name: str):
    """

    :param file_name: Enter name of file from where you will get names for book.
    :return: Random name of book chosen from file_name
    """
    with open(file_name, "r") as f:
        b = f.read()
        return (choice(b.split("\n")))


def authors(file_name: str):
    """

    :param file_name: Enter name of file from where you will get names of authors.
    :return: Random author name and surname if writing is right, else raise an error.
    """
    name_valid = re.compile(r"(?P<name>[A-Z]\w+)\s(?P<surname>[A-Z]\w+)")
    with open(file_name, "r") as f:
        author = choice(f.read().split("\n"))
        if name_valid.fullmatch(author):
            return author
        else:
            with open(file_name, "r") as f_two:
                for num, value in enumerate(f_two.readlines()):
                    if author == value.strip():
                        print(f"{author} in line {num} has invalid writing")
                        raise ValueError


def book_generator(number_of_authors):
    """
    pk incrementing by 1 every book creation.
    :return: generator that contains random generated book.
    """
    pk = 1
    while True:
        a = {"model": conf.MODEL,
             "pk": pk,
             "fields": {
                 "title": title("books.txt"),
                 "year": randint(1800, 2020),
                 "pages": randint(100, 3000),
                 "isbn13": "978-1-60487-647-5",
                 "rating": round(5 * random(), 2),
                 "price": randint(1, 123456) / 1,
                 "discount": randint(1, 100),
                 "author": [authors("authors.txt") for i in range(randint(1, number_of_authors))
                            ]}}
        pk += 1
        yield a


if __name__ == '__main__':
    parser = create_parser()
    namespace = parser.parse_args()
    c = book_generator(namespace.authors)

    if namespace.command == "output_format":
        for _ in range(int(namespace.count)):
            with open(namespace.o, "w") as f_json:
                json.dump(next(c), f_json)
    else:
        for _ in range(int(namespace.count)):
            print(json.dumps(next(c)))

    # for _ in range(4):
    #     with open("book" + str(_ + 1), "w") as f_json:
    #         json.dump(next(c), f_json)
