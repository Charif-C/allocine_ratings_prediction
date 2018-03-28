# coding: utf-8

# In[1]:


from requests import get
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep, time
from random import randint
from IPython.core.display import clear_output
from warnings import warn
import numpy as np


# In[6]:


pages_url = [str(i) for i in range(1,5)]
annees_url = [str(i) for i in range(2010,2017)]

# Lists to store the scraped data in
names=[]
dates=[]
producers=[]
actors=[]
press_ratings=[]
spectators_ratings=[]

# Preparing the monitoring of the loop
start_time = time()
requests = 0

# For every year in the interval 2010-2017
for annee_url in annees_url:

    # For every page in the interval 1-4
    for page_url in pages_url:

        # Make a get request
        response = get('http://www.allocine.fr/films/decennie-2010/annee-' + annee_url + '/?page=' + page_url)

        # Pause the loop
        sleep(randint(8,15))

        # Monitor the requests
        requests += 1
        elapsed_time = time() - start_time
        print('Request:{}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))
        clear_output(wait = True)

        # Throw a warning for non-200 status codes
        if response.status_code != 200:
            warn('Request: {}; Status code: {}'.format(requests, response.status_code))

        # Break the loop if the number of requests is greater than expected
        if requests > 100:
            warn('Number of requests was greater than expected.')
            break

        # Parse the content of the request with BeautifulSoup
        page_html = BeautifulSoup(response.text, 'html.parser')

        # Select all the 15 movie containers from a single page
        movie_containers = page_html.find_all('div', class_ = 'card card-entity card-entity-list cf')

        # For every movie of these 15, extract data from individual movie container
        for container in movie_containers:

            rating_box=container.find('div', class_='rating-holder').find_all('div', class_='rating-item')

            # If the movie has ratings, then extract:
            if rating_box != []:

                # Scrape the name
                try:
                    name=container.div.h2.a.text
                    names.append(name)
                except AttributeError:
                    names.append(np.nan)

                # Scrape the date
                try:
                    date=container.div.div.div.span.text
                    dates.append(date)
                except AttributeError:
                    dates.append(np.nan)

                # Scrape the producer
                try:
                    producer=container.div.div.find('div', class_='meta-body-item meta-body-direction light').span.text
                    producers.append(producer)
                except AttributeError:
                    producers.append(np.nan)

                # Scrape the actors
                try:
                    film_actors = str()
                    for actor_container in container.div.div.find('div', class_='meta-body-item meta-body-actor light').find_all('span'):
                        actor=actor_container.text
                        film_actors += "{} ; ".format(actor)
                    actors.append(film_actors)
                except AttributeError:
                    actors.append(np.nan)

                try:
                    type_rating=container.find('div', class_='rating-holder').find_all('div', class_='rating-item')[0].span.text
                    first_rating=container.find('div', class_='rating-holder').find_all('div', class_='rating-item')[0].div.find('span', class_='stareval-note').text[-3:]
                    first_rating=float(first_rating.replace(',', '.'))
                    # Scrape the press rating
                    if type_rating == ' Presse ':
                        press=first_rating
                        press_ratings.append(press)
                        if len(container.find('div', class_='rating-holder').find_all('div', class_='rating-item')) > 2:
                            spectator=container.find('div', class_='rating-holder').find_all('div', class_='rating-item')[1].div.find('span', class_='stareval-note').text[-3:]
                            spectator=float(spectator.replace(',', '.'))
                            spectators_ratings.append(spectator)
                        else:
                            spectators_ratings.append(np.nan)
                    # Scrape the spectators rating
                    else:
                        spectator=first_rating
                        spectators_ratings.append(spectator)
                        press_ratings.append(np.nan)
                except AttributeError:
                    spectators_ratings.append(np.nan)
                    press_ratings.append(np.nan)


# In[7]:


test_df = pd.DataFrame({'movie': names,
                       'date': dates,
                       'producer': producers,
                       'actors': actors,
                       'press_rating': press_ratings,
                       'spectators_rating' : spectators_ratings})
print(test_df.info())
test_df.head(15)

test_df.to_csv('scrapperv8.csv') # Change version!
