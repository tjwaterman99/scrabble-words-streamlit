import pandas as pd
import streamlit as st
from streamlit_scrabble_app import ScrabbleDictionary


@st.cache_data
def load_dictionary(name: str):
    return ScrabbleDictionary(name)


st.title("Scrabble word finder")
name = st.sidebar.selectbox("Dictionary", ['twl06', 'sowpods'])


def filter_starting_letters(df, chars):
    return df.where(df['Word'].str.startswith(chars))


dictionary = load_dictionary(name)
word = st.text_input("Enter a set of letters", placeholder="Scrabble")

with st.container():
    col1, col2, col3 = st.columns(3, gap='medium')
    min_length, max_length = col3.slider("Length", 2, 12, (2,12))
    starts_with = col1.text_input("Starts with",help="Optional", value=None)
    ends_with = col2.text_input("Ends with", value=None)
    
    
if word:
    anagrams = dictionary.find_subanagrams(word)
    df = pd.DataFrame(anagrams)
    df.columns = ['Word']
    df = df[df['Word'].apply(lambda w: len(w) >= min_length and len(w) <= max_length)]
    if starts_with:
        df = df[df['Word'].str.startswith(starts_with)]
    if ends_with:
        df = df[df['Word'].str.endswith(ends_with)]
    if len(df.index) > 0:
        st.dataframe(df, hide_index=True, use_container_width=True)
    else:
        st.error("No words found")
