from itertools import combinations
import string
from pathlib import Path
from pydantic import BaseModel


class RawScrabbleDictionary(BaseModel):
    words: set[str]


class ScrabbleDictionary:
    def __init__(self, name: str, valid_letters: set[str] = set(string.ascii_lowercase)):
        self.valid_letters = valid_letters
        self.name = name
        self.raw = self.load()
        self.index = self.build_index()

    def load(self) -> RawScrabbleDictionary:
        path = Path(__file__).parent / 'dictionaries' / f"{self.name}.txt"
        with open(path) as fh:
            words = fh.readlines()
            return RawScrabbleDictionary(words=words)

    def parse_letters(self, word: str) -> list[str]:
        return tuple([c for c in sorted(word) if c in self.valid_letters])

    def build_index(self) -> dict[tuple[str], list[str]]:
        result: dict[tuple[str], list[str]] = dict()
        for word in self.raw.words:
            word = word.strip()
            letters = self.parse_letters(word)
            counts = tuple(sorted(letters))
            if counts in result:
                result[counts].append(word)
            else:
                result[counts] = [word]
        return result

    def find_anagrams(self, word: str) -> set[str]:
        parsed = self.parse_letters(word)
        anagrams = self.index.get(parsed, list())
        return set(anagrams)
    
    def find_letter_subsets(self, word) -> set[tuple[str]]:
        split = tuple(word)
        result = set()
        for n in range(1, len(split) + 1):
            for c in combinations(split, n):
                result.add(c)
        return result

    def find_subanagrams(self, word) -> set[str]:
        result = set()
        for c in self.find_letter_subsets(word):
            anagrams = self.find_anagrams(''.join(c))
            for r in anagrams:
                result.add(r)
        return result