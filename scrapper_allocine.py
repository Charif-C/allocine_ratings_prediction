# coding: utf-8

# In[94]:


from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


# In[95]:


url='http://www.allocine.fr/films/?page=1'


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
        film_producers = str()
        try:
            for producer_container in container.div.div.find('div', class_='meta-body-item meta-body-direction light').find_all(['a', 'span']):
                producer = producer_container.text
                film_producers += "{} ; ".format(producer)
            producers.append(film_producers)
        except AttributeError:
            producers.append(np.nan)
        
        # The actors
        film_actors = str()
        for actor_container in container.div.div.find('div', class_='meta-body-item meta-body-actor light').find_all(['span', 'a']):
            actor=actor_container.text
            film_actors += "{} ; ".format(actor)
        actors.append(film_actors)

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
                       'actors': actors,
                       'press_rating': press_ratings,
                       'spectators_rating' : spectators_ratings})
print(test_df.info())
test_df

test_df.to_csv('test.csv') # Change version
