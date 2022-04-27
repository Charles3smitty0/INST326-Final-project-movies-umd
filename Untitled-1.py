"""
Final Project 
names: Getahun Seyoum, Yamlak Shimelis, Charlie Smith
Date: 04/26/2022
Course: INST 326
"""
from asyncore import read
import pandas as pd

"""We will need to find a database cv file of various movies
 we can use in our project to recommend movies"""

path = "/Users/getahunseyoum/Desktop/archive"
movies=pd.read_csv(path + "/movies_metadata.csv")
movies=pd.read_csv(path + "/credits.csv")
movies.head()

"""The user will input a movie title they've enjoyed which will then 
be used to recommend another or a list of movies they will also enjoy"""
def movie_seen(f):

"""The find_director function will take the name of the director for
for the film that was inputted by the user and match it with other films
in the dataset the director has also directed"""
def find_director(x):


"""We will then biuld the recommendation system based 
on similar actors/directors/genres/etc.""" 

