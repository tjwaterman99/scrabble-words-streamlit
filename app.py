import string
import pandas as pd
import streamlit as st
from functools import reduce
from itertools import combinations


twl_words_url = "https://raw.githubusercontent.com/speedreeder/ScrabbleWordChecker/master/twl06.txt"
primes = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101]
letters = string.ascii_lowercase
letter_map = dict(zip(letters, primes))


def anagramize(word: str) -> int:
    """
    Two words are anagrams if they "hash" to the same value
    """

    nums = [letter_map[c] for c in str(word)]
    return reduce(lambda x, y: x*y, nums)


@st.cache_data
def load_dictionary():
    data = pd.read_csv(twl_words_url, header=None, names=['word'], dtype={'word': str})
    data.set_index(data['word'].apply(anagramize), inplace=True)
    res: dict[str, list] = dict()
    for index, word in data.itertuples():
        if index not in res:
            res[index] = [word]
        else:
            res[index].append(word)
    return res


st.title("Scrabble word finder")
word = st.text_input("Enter your letters to find matching words")

data = load_dictionary()

if word:
    results = list()
    for n in range(1, len(word) + 1):
        combs = combinations(word, n)
        for comb in combs:
            y = anagramize(''.join(comb))
            # y
            try:
                anagrams = data[y]
                results.extend(anagrams)
            except KeyError:
                pass
    df = pd.DataFrame(results)
    df.columns = ['Word']
    st.dataframe(df, hide_index=True, use_container_width=True)