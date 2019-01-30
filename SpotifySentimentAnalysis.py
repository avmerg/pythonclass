#Upload Spotify API information
import spotipy
import sys
import spotipy.util as util

token = util.prompt_for_user_token("email",'user-library-read',client_id='client id',client_secret='client secret',redirect_uri='http://localhost/')


import sys
import spotipy
import spotipy.util as util
import pandas as pd

scope = 'user-library-read'
username = 'yourusername'


#Look at my saved songs (Don't judge!)
if token:
    sp = spotipy.Spotify(auth=token)
    results = sp.current_user_saved_tracks()
    for item in results['items']:
        track = item['track']
        print(track['name'] + ' - ' + track['artists'][0]['name'])
        #x = track['name'] + ' - ' + track['artists'][0]['name']
else:
    print("Can't get token for", username)
    

# Look Pink Floyd's albums

pinkFloyd_uri = 'spotify:artist:0k17h0D3J5VfsdmQ1iZtE9'

results = sp.artist_albums(pinkFloyd_uri, album_type='album')
albums = results['items']
while results['next']:
    results = sp.next(results)
    albums.extend(results['items'])
for album in albums:
    print(album['name'])

    

#Get top tracks from backstreet boys
backstreet = []
import pprint
import pandas as pd

artist1= 'spotify:artist:5rSXSAkZ67PYJSvpUpkOr7'
response = sp.artist_top_tracks(artist1)

for track in response['tracks']:
        backstreet.append(track['name'])

print(backstreet)


# get top LinkinPark tracks
linkinPark = []

artist2= 'spotify:artist:6XyY86QOPPrYVGvF9ch6wz'

response = sp.artist_top_tracks(artist2)

for track in response['tracks']:
     linkinPark.append(track['name'])

print(linkinPark)

#merge into a DataFrame
songs = pd.DataFrame(
    {'Backstreet': backstreet,
     'LinkinP': linkinPark
    })

display(songs)

################################
# Load vaderSentiment 
try: 
    import vaderSentiment
except ModuleNotFoundError:
    import sys
    !{sys.executable} -m pip install vaderSentiment
    import vaderSentiment
    
    
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re

analyzer = SentimentIntensityAnalyzer()
for c,tweet in enumerate(songs["Backstreet"]):
    vs = analyzer.polarity_scores(tweet)
    print("{:-<65} {}".format(tweet, str(vs)))
    
    if c  >= 5:break

#map a column with the sentiment score onto the dataframe. Only get back positive.

songs["BackstreetS"] = songs["Backstreet"].map(lambda x: analyzer.polarity_scores(x)["pos"])
display(songs)


# Map positive sentiment on LinkinPark songs
for c,tweet in enumerate(songs["LinkinP"]):
    vs = analyzer.polarity_scores(tweet)
    print("{:-<65} {}".format(tweet, str(vs)))
    
    if c  >= 5:break

songs["LinkinPS"] = songs["LinkinP"].map(lambda x: analyzer.polarity_scores(x)["pos"])
display(songs)

#Compare positivity of these band's song titles

from scipy.stats import ttest_ind
from scipy import stats

stats.ttest_ind(songs['BackstreetS'], songs['LinkinPS'], equal_var = False)

#The positive sentiment of these songs are significant on a .1 level
#but sample size is pretty low