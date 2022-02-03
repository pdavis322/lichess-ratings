import requests
import time
import numpy as np
from dotenv import load_dotenv
from os import getenv
load_dotenv()

headers = {
    'Authorization': 'Bearer ' + getenv('LICHESS_TOKEN'),
    'Content-Type': 'text-plain'
}

users = 'radiant_blur'

# Ratings: [(puzzle_rating, chess_rating)]
ratings = {'classical': [], 'rapid': [], 'blitz': [], 'bullet': []}

def get_ratings(users):
    response = requests.post('https://lichess.org/api/users', headers=headers, data=users)
    if response:
        response = response.json()
        for r in response:
            if 'prov' in r['perfs']['puzzle']:
                continue
            puzzle = r['perfs']['puzzle']['rating']
            for time in ratings.keys():
                if 'prov' not in r['perfs'][time]:
                    ratings[time].append((puzzle, r['perfs'][time]['rating']))
    else:
        print('wrong')
        time.sleep(60)
        get_ratings(users)
get_ratings('thibault, radiant_blur')
print(ratings)
# print(np.array([r[1] for r in ratings['blitz']]))   