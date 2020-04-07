#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Initialize the workspace
from pymongo import MongoClient
import pprint
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time


# In[2]:


# Connect with Mongo to place data into a database
client = MongoClient('localhost', 27017)
db = client['metacritic']
test = db['test']


# In[4]:


# Test databases/collection
test.insert_one({'abc': 123})


# In[5]:


# Create Mongo collections in which to place data
altcountry = db['altcountry']
alternative = db['alternative']
blues = db['blues']
comedy = db['comedy']
country = db['country']
dance = db['dance']
electronic = db['electronic']
experimental = db['experimental']
folk = db['folk']
house = db['house']
indie = db['indie']
jazz = db['jazz']
latin = db['latin']
metal = db['metal']
pop = db['pop']
psychedelic = db['psychedelic']
punk = db['punk']
rap = db['rap']
rb = db['rb']
reggae = db['reggae']
rock = db['rock']
singersongwriter = db['singersongwriter']
soul = db['soul']
soundtrack = db['soundtrack']
techno = db['techno']
vocal = db['vocal']
world = db['world']
coll_list = [altcountry, alternative, blues, comedy, country,
             dance, electronic, experimental, folk, house, indie,
             jazz, latin, metal, pop, psychedelic, punk, rap,
             rb, reggae, rock, singersongwriter, soul,
             soundtrack, techno, vocal, world]


# In[11]:


# Create a dictionary of genres and their associated page numbers
genre_dict = {'alt-country': 6, 'alternative': 38, 'blues':6, 'comedy':0,
              'country': 25, 'dance':6, 'electronic': 79, 'experimental':10,
              'folk': 22, 'house':5, 'indie': 74, 'jazz': 13, 'latin':2,
              'metal':6, 'pop':32, 'psychedelic':0, 'punk':4, 'rap':48,
              'rb':26, 'reggae':3, 'rock': 132, 'singer-songwriter':9,
              'soul':7, 'soundtrack':2, 'techno':6, 'vocal':4, 'world':2}


# In[12]:


# Define Beautiful Soup parameters
url = 'https://www.metacritic.com/browse/albums/genre/date/{}?page={}'
user_agent = {'User-agent': 'Mozilla/5.0'}


# In[13]:


# Loop through all pages in all genre, placing them in MongoDB along the way
for (genre, pages), coll in zip(genre_dict.items(), coll_list):
    for page in range(pages):
        r = requests.get(url.format(genre, page), headers = user_agent)
        soup = BeautifulSoup(r.text, 'html.parser')
        for one_tag in soup.find_all('div', class_ = 'product_wrap'):
            # Album title
            album = one_tag.find('a').text.strip()
            # Artist
            artist = one_tag.find_all('span', class_ = 'data')[0].text.strip()
            # Date
            date = ' '.join(one_tag.find_all('span', class_ = 'data')[1].text.split())
            # Score
            score_ = one_tag.find('div', class_ = "basic_stat product_score brief_metascore").text
            score = int(''.join(char for char in score_ if char.isdigit()))
            # Used this as a way to track potential problems/troubleshoot
            print(genre, album, artist, date, score)
            coll.insert_one({'album':album, 'artist':artist, 
                             'date':date, 'score':score})
        time.sleep(15)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




