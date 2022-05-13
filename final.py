"""
Final Project 
names: Getahun Seyoum, Yamlak Shimelis, Charlie Smith
Date: 04/26/2022
Course: INST 326
"""
from asyncore import read
import pandas as pd
import numpy as np

"""

set_options expands the dataset within the terminal to make it easier to view

"""
pd.set_option("display.max_columns", None)
pd.options.display.width = 0


""" 

We found a movies and credits database on kaggle.com
(https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata?select=tmdb_5000_credits.csv).
We used a dataset with only 5000 movies for better functionality. We used pandas to read in and view the dataset. 
We isoated 4 coulumn in the dataset('id','title','cast','crew') that were useful for the content-based systems

We merged the two datasets through the common column 'id'

"""
movies_data = pd.read_csv('tmdb_5000_movies.csv')
credits_data = pd.read_csv('tmdb_5000_credits.csv')
credits_data.columns = ['id','title','cast','crew']
movies_data = movies_data.merge(credits_data, on="id")

"""
The original dataset presented the traits in a form of lists. We imported literal_eval so it can allow us to 
access the data in the collumns as strings. We then isolated "cast", "crew", "keywords", "genres" from the dataset 
and created a new list named "traits."

The for loop created below allows us to apply literal_eval to each trait. 
"""

from ast import literal_eval
traits = ["cast", "crew", "keywords", "genres"]

for trait in traits:
    movies_data[trait] = movies_data[trait].apply(literal_eval)


def find_director(d):
    """
   
    Args:
        d: seperates the name(string) of the director the user inputs.
        
    Returns:
        The name of the director (string)
    """
    for j in d:
        #if j["job"] is "Director"
        if j["job"] == "Director":
            return j["name"]
    
def get_list(l):
    """
    Args: 
        l(list): Creats a list of the names of directors

    Return: 
        (list) This will return the first three names on the dataset  
    """
    #if type(l) is list:
    if isinstance(l, list):
        #for j in l:
            #list_names = j["name"]
        list_names = [j["name"] for j in l]
        if len(list_names) > 3:
            list_names = list_names[:3]
        return list_names
    return []

"""
This is retrieving
"""
movies_data["director"] = movies_data["crew"].apply(find_director)
traits = ["cast", "keywords", "genres"]
for trait in traits:
    movies_data[trait] = movies_data[trait].apply(get_list)


def clean_data(row):
    """ Converts into lowercase and removes whitespace characters
    Args:
        row(string): row of data
    
    Returns:
        String of data after whitespace characters are removed and characters are lowercase
    """
    #if type(row) is list:
    if isinstance(row, list):
        #for i in row:
            #str.lower(i.replace(" ", "")) or try str.lower(i.strip())
        return [str.lower(i.replace(" ", "")) for i in row]
    else:
        #if type(row) is str
        if isinstance(row, str):
            #str.lower(row.strip())
            return str.lower(row.replace(" ", ""))
        else:
            return ""
traits = ['cast', 'keywords', 'director', 'genres']
for trait in traits:
    movies_data[trait] = movies_data[trait].apply(clean_data)


def movie_soup(traits):
    """
    Args: 
        traits(string): Isolates specific columns in the data we'd like to use and see    
    Returns: 
        All data (strings) joined together
    """
    return ' '.join(traits['keywords']) + ' ' + ' '.join(traits['cast']) + ' ' + traits['director'] + ' ' + ' '.join(traits['genres'])
movies_data["soup"] = movies_data.apply(movie_soup, axis=1)
print(movies_data["soup"].head())

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

count_vectorizer = CountVectorizer(stop_words="english")
count_matrix = count_vectorizer.fit_transform(movies_data["soup"])

print(count_matrix.shape)

cosine_sim2 = cosine_similarity(count_matrix, count_matrix) 
print(cosine_sim2.shape)

movies_data = movies_data.reset_index()
indices = pd.Series(movies_data.index, index=movies_data['original_title'])

indices = pd.Series(movies_data.index, index=movies_data["original_title"]).drop_duplicates()
print(indices.head())

def get_recommendations(original_title, cosine_sim2):
    idx = indices[original_title]
    sim_scores = list(enumerate(cosine_sim2[idx]))
    sim_scores= sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores= sim_scores[1:11]
    movies_indices = [ind[0] for ind in sim_scores]
    movies = movies_data["original_title"].iloc[movies_indices]
    return movies

print("This is a content based movie reccomendation system.")
print("Input a movie that you have enjoyed, and the system will return similar movies to that title.")
m = input()
print("Movies similar to:")
print(m)

print(get_recommendations(m, cosine_sim2))

#Examples that work include "The Dark Knight Rises" or "The Avengers"

