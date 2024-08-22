from pymongo import MongoClient
import certifi
import requests
import os

ca = certifi.where()
MONGO_URI = os.getenv('MONGO_URI')

client = MongoClient(
    MONGO_URI,
    tlsCAFile=ca)

single_gameweeks = [1, 2, 5, 9, 12, 13, 16, 25, 26, 29, 30, 37, 38]
double_gameweeks = [3, 6, 7, 8, 14, 15, 17, 19, 20, 21, 23, 27, 31, 32, 33, 34, 36]
triple_gameweeks = [4, 10, 11, 18, 22, 24, 28, 35]

def get_lms():
    # get the weekly scores
    result = client['fpl_live']['weekly_scores']

    data = list(result)
    

get_lms()