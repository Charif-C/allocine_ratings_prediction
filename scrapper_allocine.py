# coding: utf-8

# In[94]:


from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


# In[95]:


url='http://www.allocine.fr/films/genre-13025/decennie-2010/annee-2017/'


# In[96]:


response=get(url)


# In[97]:


html_soup = BeautifulSoup(response.text, 'html.parser')


# In[98]:


movie_containers = html_soup.find_all('div', class_ = 'card card-entity card-entity-list cf')


# In[99]:


# Lists to store the scraped data in
names=[]
dates=[]
producers=[]
actors=[]
press_ratings=[]
spectators_ratings=[]

# Extract data from individual movie container
for container in movie_containers:

    rating_box=container.find('div', class_='rating-holder').find_all('div', class_='rating-item')
    
    # If the movie has ratings, then extract:
    if rating_box != []:

        # The name
        name=container.div.h2.a.text
        names.append(name)
        
        # The date
        date=container.div.div.div.span.text
        dates.append(date)
        
        # The producer
        try:
            producer=container.div.div.find('div', class_='meta-body-item meta-body-direction light').span.text
            producers.append(producer)
        except AttributeError:
            producers.append(np.nan)
        
        # The actors
        actor=container.div.div.find('div', class_='meta-body-item meta-body-actor light').span.text
        actors.append(actor)

        type_rating=container.find('div', class_='rating-holder').find_all('div', class_='rating-item')[0].span.text
        first_rating=container.find('div', class_='rating-holder').find_all('div', class_='rating-item')[0].div.find('span', class_='stareval-note').text[-3:]
        # The press rating
        if type_rating == ' Presse ':
            press=first_rating
            press_ratings.append(press)
            if len(container.find('div', class_='rating-holder').find_all('div', class_='rating-item')) == 2:
                spectator=container.find('div', class_='rating-holder').find_all('div', class_='rating-item')[1].div.find('span', class_='stareval-note').text[-3:]
                spectators_ratings.append(spectator)
            else:
                spectators_ratings.append(np.nan)
        # The spectators rating
        elif type_rating == ' Spectateurs ':
            spectator=first_rating
            spectators_ratings.append(spectator)
            press_ratings.append(np.nan)


# In[100]:


test_df = pd.DataFrame({'movie': names,
                       'date': dates,
                       'producer': producers,
                       'actor': actors,
                       'press_rating': press_ratings,
                       'spectators_rating' : spectators_ratings})
print(test_df.info())
test_df

test_df.to_csv('scrapperv3.csv')
