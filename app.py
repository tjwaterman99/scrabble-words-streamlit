import pandas as pd
import streamlit as st
from streamlit_scrabble_app import ScrabbleDictionary


@st.cache_data
def load_dictionary(name: str):
    return ScrabbleDictionary(name)


st.title("Scrabble word finder")
name = st.sidebar.selectbox("Dictionary", ['twl06', 'sowpods'])
word = st.text_input("Enter a set of letters")
dictionary = load_dictionary(name)
if word:
    anagrams = dictionary.find_subanagrams(word)
    df = pd.DataFrame(anagrams)
    df.columns = ['Word']
    st.dataframe(df, hide_index=True, use_container_width=True)