import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import json
import streamlit as st
import numpy as np
from PIL import Image
from wordcloud import WordCloud
import matplotlib.pyplot as plt


def load_data():
    with open('data/weekly.json', 'r') as file:
        weekly_keywords = json.load(file)
    with open('data/combined.json') as file:
        combined_keyword = json.load(file)
    dates = [date for date in weekly_keywords]
    return combined_keyword, weekly_keywords, dates


def get_word_cloud(image, data, max_words, max_font_size):
    if image == 'default':
        wordcloud = WordCloud(width=700, height=400, repeat=True,
                              max_words=max_words, max_font_size=max_font_size, background_color='white',
                              ).generate_from_frequencies(data)
    else:
        path = f'data/image_masks/{image}.jpg'
        mask = np.array(Image.open(path))
        wordcloud = WordCloud(width=400, height=400, repeat=True,
                              max_words=max_words, max_font_size=max_font_size, background_color='white',
                              mask=mask).generate_from_frequencies(data)
    return wordcloud


st.title("Word Clouds based on Google Keyword and Twitter Hashtag trends")
image = st.sidebar.selectbox(label='Select Image Mask', options=[
                             'default', 'twitter', 'hashtag', 'heart'])


maxFontSize = st.sidebar.slider('Font Size', 10, 20)
background_color = st.sidebar.selectbox(
    label='Select background color', options=['white', 'red', 'grey', 'blue'])
repeat = st.sidebar.checkbox('repeat')
if (repeat):
    repeat = True
else:
    repeat = False


combined_keyword, weekly_keywords, dates = load_data()


st.header("Entire Year")
wordcloud = get_word_cloud(image, combined_keyword, 800, 15)
fig1 = plt.figure()
plt.imshow(wordcloud)
plt.axis("off")
st.pyplot(fig1)

st.header("Weekly")
date = st.selectbox(label='Select Date', options=dates)
keywords = weekly_keywords[date]
wordcloud = get_word_cloud(image, keywords, 200, 25)
fig2 = plt.figure()
plt.imshow(wordcloud)
plt.axis("off")
st.pyplot(fig2)
