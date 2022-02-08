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
    start, end = 0, len(users) if len(users) <= 300 else 300
    while start == 0 or end < len(users):
        response = requests.post('https://lichess.org/api/users', headers=headers, data=','.join(users[start:end]))
        if response.status_code == requests.codes.ok:
            response = response.json()
            for r in response:
                if 'perfs' not in r or 'puzzle' not in r['perfs'] or 'prov' in r['perfs']['puzzle']:
                    continue
                puzzle = r['perfs']['puzzle']['rating']
                for time in ratings.keys():
                    if time not in r['perfs'] or 'prov' in r['perfs'][time]:
                        continue
                    ratings[time].append((puzzle, r['perfs'][time]['rating']))
            start, end = end, len(users) if len(users) - end <= 300 else end + 300
        else:
            print('wrong')
            time.sleep(60)
            get_ratings(users)

# print(np.array([r[1] for r in ratings['blitz']]))   



# Returns list of usernames
def get_users(num_users):
    # Don't count the same user twice
    users = set()
    with open('/mnt/c/Users/peter/Downloads/lichess_db_standard_rated_2022-01.pgn/lichess_db_standard_rated_2022-01.pgn') as f:
        for i, line in enumerate(f):
            if len(users) >= num_users:
                break
            if line[0:7] == "[White " or line[0:7] == "[Black ":
                username = re.findall(r'"(.*?)"', line)[0]
                if username not in users:
                    users.add(username)
    # Need to convert to list to go 300 users at a time for API
    return list(users)

get_ratings(get_users(1000))
#print(len(ratings['blitz']) + len(ratings['bullet']) + len(ratings['classical']) + len(ratings['rapid']))