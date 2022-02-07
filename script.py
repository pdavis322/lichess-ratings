import requests
import time
import numpy as np
import re
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
    if response.status_code == requests.codes.ok:
        response = response.json()
        for r in response:
            if 'perfs' not in r or 'puzzle' not in r['perfs'] or 'prov' in r['perfs']['puzzle']:
                continue
            puzzle = r['perfs']['puzzle']['rating']
            for time in ratings.keys():
                if 'prov' not in r['perfs'][time]:
                    ratings[time].append((puzzle, r['perfs'][time]['rating']))
    else:
        print('wrong')
        time.sleep(60)
        get_ratings(users)
#get_ratings('thibault, radiant_blur')
#print(ratings)
# print(np.array([r[1] for r in ratings['blitz']]))   

# Returns comma separated list of users : length num_users
def get_users(num_users):
    users = []
    with open('/mnt/c/Users/peter/Downloads/lichess_db_standard_rated_2022-01.pgn/lichess_db_standard_rated_2022-01.pgn') as f:
        for i, line in enumerate(f):
            if len(users) > num_users:
                break
            if line[0:7] == "[White " or line[0:7] == "[Black ":
                users.append(re.findall(r'"(.*?)"', line)[0])
    return ','.join(users)

get_ratings(get_users(300))
print(ratings)