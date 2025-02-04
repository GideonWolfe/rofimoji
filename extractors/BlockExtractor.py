import html

import requests

from extractors.BlockFactory import BlockFactory
from extractors.CharacterFactory import CharacterFactory


class BlockExtractor(object):
    def __init__(self, character_factory: CharacterFactory):
        super().__init__()
        self.__blocks = []
        self.__block_factory = BlockFactory(character_factory)

    def fetch_blocks(self: 'BlockExtractor'):
        print('Downloading list of all blocks')

        response = requests.get(
            'https://www.unicode.org/Public/13.0.0/ucd/Blocks.txt',
            timeout=60
        )  # type: requests.Response

        lines = response.content.decode(response.encoding).split('\n')

        for line in lines:
            if line.startswith('#') or line.startswith('@') or len(line) == 0:
                continue
            fields = line.split(';')
            self.__blocks.append(self.__block_factory.build_block_from_range(fields[1].strip(), fields[0].strip()))

    def write_to_files(self: 'BlockExtractor'):
        for block in self.__blocks:
            if len(block.characters) == 0:
                continue

            symbol_file = open(f"../picker/data/{block.name.lower().replace(' ', '_')}.csv", 'w')

            for character in block.characters:
                symbol_file.write(f"{character.char} {html.escape(character.name)}\n")

            symbol_file.close()

    def extract(self):
        self.fetch_blocks()
        self.write_to_files()
