import html
from typing import List

import requests

from extractors.CharacterFactory import CharacterFactory, Character


class MathExtractor(object):

    def __init__(self, character_factory: CharacterFactory):
        self.__char_factory = character_factory

    def fetch_math_symbols(self: 'MathExtractor') -> List[Character]:
        print('Downloading list of maths symbols...')

        data = requests.get(
            'https://unicode.org/Public/math/latest/MathClassEx-15.txt',
            timeout=60
        )  # type: requests.Response

        characters = []
        for line in data.content.decode(data.encoding).split('\n'):
            if line.startswith('#') or len(line) == 0:
                continue

            fields = line.split(';')

            symbols = self.resolve_character_range(fields[0].strip())

            for symbol in symbols:
                characters.append(self.__char_factory.get_character(symbol))

        return characters

    def resolve_character_range(self, line: str) -> List[int]:
        try:
            (start, end) = line.split('..')
            symbols = []
            for char in range(int(start, 16), int(end, 16) + 1):
                symbols.append(char)
            return symbols
        except ValueError:
            return [int(line, 16)]

    def write_file(self: 'MathExtractor', symbols: List[Character]):
        symbol_file = open(f"../picker/data/math.csv", 'w')

        for character in symbols:
            symbol_file.write(f"{character.char} {html.escape(character.name)}\n")

        symbol_file.close()

    def extract(self):
        self.write_file(self.fetch_math_symbols())
