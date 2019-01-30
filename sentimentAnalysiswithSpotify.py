{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "#Upload Spotify API information\n",
    "import spotipy\n",
    "import sys\n",
    "import spotipy.util as util\n",
    "\n",
    "token = util.prompt_for_user_token(\"email\",'user-library-read',client_id='client id',client_secret='client secret',redirect_uri='http://localhost/')\n",
    "\n",
    "\n",
    "import sys\n",
    "import spotipy\n",
    "import spotipy.util as util\n",
    "import pandas as pd\n",
    "\n",
    "scope = 'user-library-read'\n",
    "username = 'alivatchu@gmail.com'\n",
    "\n",
    "\n",
    "#Look at my saved songs (Don't judge!)\n",
    "if token:\n",
    "    sp = spotipy.Spotify(auth=token)\n",
    "    results = sp.current_user_saved_tracks()\n",
    "    for item in results['items']:\n",
    "        track = item['track']\n",
    "        print(track['name'] + ' - ' + track['artists'][0]['name'])\n",
    "        #x = track['name'] + ' - ' + track['artists'][0]['name']\n",
    "else:\n",
    "    print(\"Can't get token for\", username)\n",
    "    \n",
    "\n",
    "# Look Pink Floyd's albums\n",
    "\n",
    "pinkFloyd_uri = 'spotify:artist:0k17h0D3J5VfsdmQ1iZtE9'\n",
    "\n",
    "results = sp.artist_albums(pinkFloyd_uri, album_type='album')\n",
    "albums = results['items']\n",
    "while results['next']:\n",
    "    results = sp.next(results)\n",
    "    albums.extend(results['items'])\n",
    "for album in albums:\n",
    "    print(album['name'])\n",
    "\n",
    "    \n",
    "\n",
    "#Get top tracks from backstreet boys\n",
    "backstreet = []\n",
    "import pprint\n",
    "import pandas as pd\n",
    "\n",
    "artist1= 'spotify:artist:5rSXSAkZ67PYJSvpUpkOr7'\n",
    "response = sp.artist_top_tracks(artist1)\n",
    "\n",
    "for track in response['tracks']:\n",
    "        backstreet.append(track['name'])\n",
    "\n",
    "print(backstreet)\n",
    "\n",
    "\n",
    "# get top LinkinPark tracks\n",
    "linkinPark = []\n",
    "\n",
    "artist2= 'spotify:artist:6XyY86QOPPrYVGvF9ch6wz'\n",
    "\n",
    "response = sp.artist_top_tracks(artist2)\n",
    "\n",
    "for track in response['tracks']:\n",
    "     linkinPark.append(track['name'])\n",
    "\n",
    "print(linkinPark)\n",
    "\n",
    "#merge into a DataFrame\n",
    "songs = pd.DataFrame(\n",
    "    {'Backstreet': backstreet,\n",
    "     'LinkinP': linkinPark\n",
    "    })\n",
    "\n",
    "display(songs)\n",
    "\n",
    "################################\n",
    "# Load vaderSentiment \n",
    "try: \n",
    "    import vaderSentiment\n",
    "except ModuleNotFoundError:\n",
    "    import sys\n",
    "    !{sys.executable} -m pip install vaderSentiment\n",
    "    import vaderSentiment\n",
    "    \n",
    "    \n",
    "from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer\n",
    "import re\n",
    "\n",
    "analyzer = SentimentIntensityAnalyzer()\n",
    "for c,tweet in enumerate(songs[\"Backstreet\"]):\n",
    "    vs = analyzer.polarity_scores(tweet)\n",
    "    print(\"{:-<65} {}\".format(tweet, str(vs)))\n",
    "    \n",
    "    if c  >= 5:break\n",
    "\n",
    "#map a column with the sentiment score onto the dataframe. Only get back positive.\n",
    "\n",
    "songs[\"BackstreetS\"] = songs[\"Backstreet\"].map(lambda x: analyzer.polarity_scores(x)[\"pos\"])\n",
    "display(songs)\n",
    "\n",
    "\n",
    "# Map positive sentiment on LinkinPark songs\n",
    "for c,tweet in enumerate(songs[\"LinkinP\"]):\n",
    "    vs = analyzer.polarity_scores(tweet)\n",
    "    print(\"{:-<65} {}\".format(tweet, str(vs)))\n",
    "    \n",
    "    if c  >= 5:break\n",
    "\n",
    "songs[\"LinkinPS\"] = songs[\"LinkinP\"].map(lambda x: analyzer.polarity_scores(x)[\"pos\"])\n",
    "display(songs)\n",
    "\n",
    "#Compare positivity of these band's song titles\n",
    "\n",
    "from scipy.stats import ttest_ind\n",
    "from scipy import stats\n",
    "\n",
    "stats.ttest_ind(songs['BackstreetS'], songs['LinkinPS'], equal_var = False)\n",
    "\n",
    "#The positive sentiment of these songs are significant on a .1 level\n",
    "#but sample size is pretty low"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.6.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}