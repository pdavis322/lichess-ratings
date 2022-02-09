import requests
from time import sleep
import numpy as np
import matplotlib.pyplot as plt
import re
import dill
from dotenv import load_dotenv
from os import getenv
load_dotenv()

headers = {
    'Authorization': 'Bearer ' + getenv('LICHESS_TOKEN'),
    'Content-Type': 'text-plain'
}




# Ratings: [(puzzle_rating, chess_rating)]
def get_ratings(users, start=None, end=None, ratings=None):
    ratings = {'classical': [], 'rapid': [], 'blitz': [], 'bullet': []} if not ratings else ratings
    if not start:
        start, end = 0, len(users) if len(users) <= 300 else 300
    while start < len(users):
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
            print(f'Found {start} user ratings')
        else:
            print(f'Lichess API returned error ' + str(response.status_code))
            # Sleep 61 seconds: API documentation says to wait 1 minute if we get response 429
            sleep(61)
    print('Found ratings')
    return ratings





# Returns list of usernames
def get_users(num_users, start=0):
    # Don't count the same user twice
    users = set()
    index = 0
    with open('/mnt/c/Users/peter/Downloads/lichess_db_standard_rated_2022-01.pgn/lichess_db_standard_rated_2022-01.pgn') as f:
        for line in f:
            if index < start:
                index += 1
                continue
            if len(users) >= num_users:
                break
            if line[0:7] == "[White " or line[0:7] == "[Black ":
                username = re.findall(r'"(.*?)"', line)[0]
                if username not in users:
                    users.add(username)
    # Need to convert to list to go 300 users at a time for API
    print('Collected list of users')
    return list(users)

ratings = None
print('Reading previous ratings dict from file')
with open("ratings2.dill", "rb") as f:
    ratings = dill.load(f)
ratings = get_ratings(get_users(10000, start=20000), ratings=ratings)
print('Writing ratings dict to file')
with open("ratings2.dill", "wb") as f:
    dill.dump(ratings, f)



print(len(ratings['blitz']))
print(len(ratings['bullet']))
print(len(ratings['classical']))
print(len(ratings['rapid']))
# Sort by puzzle rating
ratings['blitz'].sort(key=lambda x:x[0])
# X axis is puzzle, y axis is game rating
blitz_x = np.array([r[0] for r in ratings['blitz']])
blitz_y = np.array([r[1] for r in ratings['blitz']])
coef = np.polyfit(blitz_x, blitz_y, 1)
print(coef)
poly1d_fn = np.poly1d(coef) 
plt.plot(blitz_x,blitz_y, 'yo', blitz_x, poly1d_fn(blitz_x), '--k') 
plt.show()