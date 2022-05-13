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
    
def create_list(l):
    """
    Args: 
        l(list): Creats a list of the names of directors

    Return: 
        (list): This will return the first three names on the dataset  
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
    movies_data[trait] = movies_data[trait].apply(create_list)


def cleanup_dataset(rows):
    """ Converts into lowercase and removes whitespace characters
    Args:
        rows(string): rows of data
    
    Returns:
        String of data after whitespace characters are removed and characters are lowercase
    """
    #if type(rows) is list:
    if isinstance(rows, list):
        #for r in rows:
            #str.lower(i.replace(" ", "")) or try str.lower(i.strip())
        return [str.lower(r.replace(" ", "")) for r in rows]
    else:
        #if type(rows) is str
        if isinstance(rows, str):
            #str.lower(rows.strip())
            return str.lower(rows.replace(" ", ""))
        else:
            return ""
traits = ['cast', 'keywords', 'director', 'genres']
for trait in traits:
    movies_data[trait] = movies_data[trait].apply(cleanup_dataset)


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

"""
We earned about sklearn from(citation below):
How to install scikit-learn on macos? GeeksforGeeks. (2021, September 30). Retrieved May 9, 2022, 
from https://www.geeksforgeeks.org/how-to-install-scikit-learn-on-macos/ 

CountVectorizer is used to load the data and change it into a vectorizer. It counts the number of times a 
word is used and outputs a visual

cosine_similarity is used to computes similarity as the normalized dot product of the output

"""
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

counts_vectorizer = CountVectorizer(stop_words="english")
counts_matrix = counts_vectorizer.fit_transform(movies_data["soup"])

print(counts_matrix.shape)

cosine_movies = cosine_similarity(counts_matrix, counts_matrix) 
print(cosine_movies.shape)

movies_dataset = movies_data.reset_index()
movie_indc = pd.Series(movies_dataset.index, index=movies_dataset['original_title'])

movie_indc = pd.Series(movies_dataset.index, index=movies_dataset["original_title"]).drop_duplicates()
print(movie_indc.head())

def list_recommendation(original_title, cosine_movies):
    """
    Args:
        Original_title(string): Takes the title of the movie inputed
        cosine_movies(list): takes other movies similar to the one the user inputed
    
    Return:
        movies_rec(list): A list of movies the user might be interested in based on their input
    """
    movies_idex = movie_indc[original_title]
    movie_scores = list(enumerate(cosine_movies[movies_idex]))
    movie_scores= sorted(movie_scores, key=lambda x: x[1], reverse=True)
    movie_scores= movie_scores[1:11]
    movie_ids = [idc[0] for idc in movie_scores]
    movies_rec = movies_data["original_title"].iloc[movie_ids]
    return movies_rec

print("This is a content based movie reccomendation system.")
print("Input a movie that you have enjoyed, and the system will return similar movies to that title.")
user_input = input()
print("Movies similar to:")
print(user_input)

print(list_recommendation(user_input, cosine_movies))

#Examples that work include "The Dark Knight Rises" or "The Avengers"

