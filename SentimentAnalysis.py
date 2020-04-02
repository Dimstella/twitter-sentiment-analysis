import credentials  # Import api/access_token keys from credentials.py
import settings  # Import related setting constants from settings.py
import re
import tweepy
import mysql.connector
from textblob import TextBlob
import mysql.connector



# Streaming With Tweepy
# http://docs.tweepy.org/en/v3.4.0/streaming_how_to.html#streaming-with-tweepy


# Override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):

    #Tweets are known as “status updates”. So the Status class in tweepy has properties describing the tweet.

    def on_status(self, status):  #Extract info from tweets

        if status.retweeted: # Avoid retweeted info, and only original tweets will be received
            return True
        # Extract attributes from each tweet
        id_str = status.id_str
        user_name = status.user.screen_name
        created_at = status.created_at
        text = deEmojify(status.text)  # Pre-processing the text
        sentiment = TextBlob(text).sentiment
        polarity = sentiment.polarity
        subjectivity = sentiment.subjectivity

        if polarity > 0:
            sentiment = 'POSITIVE'
        elif polarity < 0:
            sentiment = 'NEGATIVE'
        else:
            sentiment = 'NEUTRAL'

        #Add to variable x the trackword of every tweet
        list=[]
        for i in settings.TRACK_WORDS:
            if i in text.upper():
                list.append(i)
                x = ' '.join([str(elem) for elem in list])


        user_location = deEmojify(status.user.location)
        user_followers_count = status.user.followers_count
        longitude = None
        latitude = None
        if status.coordinates:
            longitude = status.coordinates['coordinates'][0]
            latitude = status.coordinates['coordinates'][1]

        tweet_count = status.user.statuses_count
        retweet_count = status.retweet_count

        hash_list = re.findall(r"#(\w+)", text)
        hashtags = ' '.join([str(elem) for elem in hash_list])
        print(status.text)
        print("Long: {}, Lati: {}".format(longitude, latitude))


        if list != []: #Avoid the no relevant tweets
            # Store all data in MySQL
            if mydb.is_connected():
                mycursor = mydb.cursor()
                sql = "INSERT INTO {} (id_str, atr, user_name, tweet_count, created_at, text, polarity, subjectivity, user_location, user_followers_count, longitude, latitude, retweet_count, hashtags, sentiment) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)".format(
                    settings.TABLE_NAME)
                val = (id_str, x, user_name, tweet_count, created_at, clean_tweet(text), polarity, subjectivity, user_location, \
                        user_followers_count, longitude, latitude, retweet_count, hashtags, sentiment)
                mycursor.execute(sql, val)
                mydb.commit()
                mycursor.close()

    def on_error(self, status_code): #Stop srcraping data as it exceed to the thresold.

        if status_code == 420:  # return False to disconnect the stream

            return False


def clean_tweet(tweet): #Clean tweet text by removing links and special characters

    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) \
                                |(\w+:\/\/\S+)", " ", tweet).split())


def deEmojify(text): #Remove emoji characters

    if text:
        return text.encode('ascii', 'ignore').decode('ascii')
    else:
        return None


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database=""

)


auth = tweepy.OAuthHandler(credentials.API_KEY, credentials.API_SECRET_KEY)
auth.set_access_token(credentials.ACCESS_TOKEN, credentials.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
myStream.filter(languages=["en"], track=settings.TRACK_WORDS)
mydb.close()

