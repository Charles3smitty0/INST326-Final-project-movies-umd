"""
Final Project 
names: Getahun Seyoum, Yamlak Shimelis, Charlie Smith
Date: 04/26/2022
Course: INST 326
"""
from asyncore import read
from turtle import title
from unicodedata import category
import pandas as pd
from ast import literal_eval

"""We will need to find a database cv file of various movies
we can use in our project to recommend movies"""

movies=pd.read_csv("archive/movies_metadata.csv", low_memory=False)
credits=pd.read_csv("archive/credits.csv", low_memory=False)
credits.columns=['id', 'cast','crew']
movies_credits=movies.merge(credits,on='id')
print(movies_credits.head)

categories=['cast', 'crew', 'genres', 'production company']

for category in categories:
    movies_credits[category]=movies_credits[category].apply(literal_eval)

def find_director(d):
    """The get_list function will return a list of top 3 elements from the 
    movie data set """
    for i in d:
        if i["job"] == "Director":
            return i["name"]
    return np.nan

def find_list(l):
    if isinstance(l, list):
        names = [i["name"] for i in l]
        if len(names) > 3:
            names = names[:3]
        return names
    return []

movies_credits["director"] = movies_credits["crew"].apply(find_director)
categories = ['cast', 'crew', 'genres', 'production company']
for feature in features:
    movies_credits[category] = movies_credits[category].apply(find_list)

def data_filter(row):
    if isinstance(row, list):
        return [str.lower(i.replace(" ", "")) for l in row]
    else:
        if isinstance(row, str):
            return str.lower(row.replace(" ", ""))
        else:
            return ""
categories = ['cast', 'crew', 'genres', 'production company']
for categories in features:
        movies_credits[category] = movies_credits[category].apply(find_list)




movies_credits[category].head(10)

"""The user will input a movie title they've enjoyed which will then 
be used to recommend another or a list of movies they will also enjoy"""
def movie_seen(f):

    """The find_director function will take the name of the director for
    for the film that was inputted by the user and match it with other films
    in the dataset the director has also directed"""
def find_director(x):
    """The get_list function will return a list of top 3 elements from the 
    movie data set """
    for i in x:
        if i["job"] == "Director":
            return i["name"]
    return np.nan
    
def get_list(x):
    if isinstance(x, list):
        names = [i["name"] for i in x]
        if len(names) > 3:
            names = names[:3]
        return names
    return []

"""We will then biuld the recommendation system based 
on similar actors/directors/genres/etc.""" 

