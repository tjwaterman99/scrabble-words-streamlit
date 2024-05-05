from streamlit_scrabble_app.anagramer import ScrabbleDictionary


def test_load_twl06():
    dictionary = ScrabbleDictionary('twl06')
    assert dictionary.raw.words
    assert 'a' in dictionary.valid_letters
    assert dictionary.parse_letters('aba') == ('a', 'a', 'b')
    assert 'bat' in dictionary.find_anagrams('bat')
    assert 'tab' in dictionary.find_anagrams('bat')
    assert len(dictionary.find_anagrams('a')) == 0
    assert ('a', 'a') in dictionary.find_letter_subsets('aa')
    assert ('a',) in dictionary.find_letter_subsets('aa')
    assert ('b',) not in dictionary.find_letter_subsets('aa')
    assert ('a', 'b') in dictionary.find_letter_subsets('aab')
    assert ('a', 'b') in dictionary.find_letter_subsets('aabAXz')
    assert 'cat' in dictionary.find_subanagrams('act')
    assert 'act' in dictionary.find_subanagrams('act')
    assert 'at' in dictionary.find_subanagrams('act')