"""
Final Project 
names: Getahun Seyoum, Yamlak Shimelis, Charlie Smith
Date: 04/26/2022
Course: INST 326
"""
from asyncore import read
import pandas as pd
import numpy as np

pd.set_option("display.max_columns", None)
pd.options.display.width = 0


"""We will need to find a database cv file of various movies
 we can use in our project to recommend movies"""


movies_data = pd.read_csv('tmdb_5000_movies.csv')
credits_data = pd.read_csv('tmdb_5000_credits.csv')

credits_data.columns = ['id','title','cast','crew']
movies_data = movies_data.merge(credits_data, on="id")


from ast import literal_eval
traits = ["cast", "crew", "keywords", "genres"]

for trait in traits:
    movies_data[trait] = movies_data[trait].apply(literal_eval)


def find_director(d):
    for i in d:
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

movies_data["director"] = movies_data["crew"].apply(find_director)
traits = ["cast", "keywords", "genres"]
for trait in traits:
    movies_data[trait] = movies_data[trait].apply(get_list)


def clean_data(row):
    if isinstance(row, list):
        return [str.lower(i.replace(" ", "")) for i in row]
    else:
        if isinstance(row, str):
            return str.lower(row.replace(" ", ""))
        else:
            return ""
traits = ['cast', 'keywords', 'director', 'genres']
for trait in traits:
    movies_data[trait] = movies_data[trait].apply(clean_data)


def movie_soup(traits):
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

