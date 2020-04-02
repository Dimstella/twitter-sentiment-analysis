import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import pandas as pd
import mysql.connector
import  settings
import numpy as np
from wordcloud import WordCloud

def Counter(df, list, x, y):
    word1 = 0
    word2 = 0
    word3 = 0
    combinations = 0

    for i in df:
        for t in list:
            if t == settings.TRACK_WORDS[0]:
                word1 += i
            elif t == settings.TRACK_WORDS[1]:
                word2 += i
            elif t == settings.TRACK_WORDS[2]:
                word3 += i
            else:
                combinations += 1

    data = [(settings.TRACK_WORDS[0], word1), (settings.TRACK_WORDS[1], word2), (settings.TRACK_WORDS[2], word3)]
    freq = pd.DataFrame(data, columns=[x, y])
    print(freq)
    return freq


def NumberofTweets(df, list, x, y):
    word1 = 0
    word2 = 0
    word3 = 0
    combinations = 0
    for t in l:
        if t == settings.TRACK_WORDS[0]:
            word1 += 1
        elif t == settings.TRACK_WORDS[1]:
            word2 += 1
        elif t == settings.TRACK_WORDS[2]:
            word3 += 1
        else:
            combinations += 1

    data = [(settings.TRACK_WORDS[0], word1), (settings.TRACK_WORDS[1], word2), (settings.TRACK_WORDS[2], word3)]
    freq = pd.DataFrame(data, columns=[x, y])
    print(freq)
    return freq

def Timeseries(df, track):
    # UTC for date time at default
    df['created_at'] = pd.to_datetime(df['created_at'])
    print("Candidates Negative Tweets Monitor: ")
    for index, tweets in df[df['sentiment'] == 'NEGATIVE'].iterrows():
        print("  " + str(tweets[2]) + "  " + tweets[1])

    # Clean and transform data to enable time series
    result = df.groupby([pd.Grouper(key='created_at', freq='5min'), 'sentiment']).count() \
        .unstack(fill_value=0).stack().reset_index()
    result['created_at'] = pd.to_datetime(result['created_at']).apply(lambda x: x.strftime('%m-%d %H:%M'))

    # Plot Line Chart for monitoring brand awareness on Twitter
    mpl.rcParams['figure.dpi'] = 200
    plt.figure(figsize=(16, 6))
    sns.set(style="darkgrid")
    ax = sns.lineplot(x="created_at", y="id_str", hue='sentiment', data=result, \
                      palette=sns.color_palette(["#FF5A5F", "#484848", "#767676"]))
    ax.set(xlabel='Time Series in UTC', ylabel="Number of '{}' mentions".format(track))
    plt.legend(title='Candidates Tweets Monitor:', loc='upper left', labels=['Negative', 'Normal', 'Positive'])
    sns.set(rc={"lines.linewidth": 1})
    plt.show()

def Densityplots(data1, data2, data3):
    d = sns.kdeplot(data1, shade=True, color="r")
    d = sns.kdeplot(data2, shade=True, color="b")
    d = sns.kdeplot(data3, shade=True, color="g")
    plt.show()

def BarPlot(freq, x, y, color):
    height = freq[y]
    bars = freq[x]
    y_pos = np.arange(len(bars))
    plt.bar(y_pos, height, color=color)
    plt.xticks(y_pos, bars)
    plt.show()

def CategoricalSentiment(n, s):
        names = ['NEGATIVE', 'NEUTRAL', 'POSITIVE']
        values = n
        plt.figure(figsize=(10, 3))
        plt.subplot(131)
        plt.bar(names, values)
        plt.subplot(132)
        plt.scatter(names, values)
        plt.subplot(133)
        plt.plot(names, values)
        plt.suptitle(s)
        plt.show()

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database=""

)
#Take values from database
df_sanders = pd.read_sql("SELECT id_str, text, created_at, sentiment, user_location, atr FROM {} WHERE atr = 'BERNIE SANDERS'".format(settings.TABLE_NAME), con=mydb)
df_warren = pd.read_sql("SELECT id_str, text, created_at, sentiment, user_location, atr FROM {} WHERE atr = 'ELIZABETH WARREN'".format(settings.TABLE_NAME), con=mydb)
df_bloom = pd.read_sql("SELECT id_str, text, created_at, sentiment, user_location, atr FROM {} WHERE atr = 'MIKE BLOOMBERG'".format(settings.TABLE_NAME), con=mydb)

followers = pd.read_sql("SELECT user_followers_count FROM {} WHERE user_followers_count>10000".format(settings.TABLE_NAME), con=mydb)
tweet_counter = pd.read_sql("SELECT tweet_count FROM {} WHERE user_followers_count>10000".format(settings.TABLE_NAME), con=mydb)
theme = pd.read_sql('SELECT atr FROM {}'.format(settings.TABLE_NAME), con=mydb)
l = []
for i in theme.values:
    for j in i:
        l.append(j)

pol_sanders = pd.read_sql("SELECT  polarity as polarity_sanders FROM {} WHERE atr = 'BERNIE SANDERS'".format(settings.TABLE_NAME), con=mydb)
pol_warren = pd.read_sql("SELECT  polarity as polarity_warren FROM {} WHERE atr = 'ELIZABETH WARREN'".format(settings.TABLE_NAME), con=mydb)
pol_bloom = pd.read_sql("SELECT  polarity as polarity_bloomberg FROM {} WHERE atr = 'MIKE BLOOMBERG'".format(settings.TABLE_NAME), con=mydb)
subj_warren = pd.read_sql("SELECT  subjectivity as subjectivity_warren FROM {} WHERE atr = 'ELIZABETH WARREN'".format(settings.TABLE_NAME), con=mydb)
subj_sanders = pd.read_sql("SELECT  subjectivity as subjectivity_sanders FROM {} WHERE atr = 'BERNIE SANDERS'".format(settings.TABLE_NAME), con=mydb)
subj_bloom = pd.read_sql("SELECT  subjectivity as subjectivity_bloomberg FROM {} WHERE atr = 'MIKE BLOOMBERG'".format(settings.TABLE_NAME), con=mydb)

#Tables with the number of attributes for each track word
followers = Counter(followers['user_followers_count'], l, 'Candidates', 'Number of followers')
UserTweets = Counter(tweet_counter['tweet_count'], l, 'Candidates', 'Number of users tweets')
tweets_no = NumberofTweets(theme['atr'], l, 'Candidates', 'Number of tweets')

#Bar plots that shows the distribution of observations at every track word
BarPlot(followers, 'Candidates', 'Number of followers', ('#ff4554', '#ff6714', '#a12222'))
BarPlot(UserTweets, 'Candidates', 'Number of users tweets',  ('#ff8000', '#dc6900', '#ffce26'))
BarPlot(tweets_no, 'Candidates', 'Number of tweets',  ('#00c3e3', '#7170ff', '#8afccf'))

#Time series graph for the flactuation of the sentiment through time
Timeseries(df_sanders, settings.TRACK_WORDS[0])
Timeseries(df_warren, settings.TRACK_WORDS[1])
Timeseries(df_bloom, settings.TRACK_WORDS[2])

#Denity plots for the sentiment analysis at polarity and subjectivity for the track words
Densityplots(pol_sanders["polarity_sanders"], pol_warren["polarity_warren"], pol_bloom["polarity_bloomberg"])
Densityplots(subj_sanders["subjectivity_sanders"], subj_warren["subjectivity_warren"], subj_bloom["subjectivity_bloomberg"])

#Count the sentiment from each category
cursor = mydb.cursor()
cursor.execute("select sentiment,count(sentiment) from main.tweet group by sentiment;")
rows = cursor.fetchall()
cursor.execute("select count(sentiment) from main.tweet where atr = 'BERNIE SANDERS' group by sentiment;")
sanders = [item[0] for item in cursor.fetchall()]
cursor.execute("select count(sentiment) from main.tweet where atr = 'ELIZABETH WARREN' group by sentiment;")
warren = [item[0] for item in cursor.fetchall()]
cursor.execute("select count(sentiment) from main.tweet where atr = 'MIKE BLOOMBERG' group by sentiment;")
bloomberg = [item[0] for item in cursor.fetchall()]

CategoricalSentiment(sanders, 'Categorical sentiment for BERNIE SANDERS')
CategoricalSentiment(warren, 'Categorical sentiment for ELIZABETH WARREN')
CategoricalSentiment(bloomberg, 'Categorical sentiment for MIKE BLOOMBERG')



#Graphs after debate of 26/02/2020

theme_after = pd.read_sql("SELECT atr FROM {} WHERE user_followers_count>10000 and created_at >= '2020-02-27 18:07:40'".format(settings.TABLE_NAME), con=mydb)
l = []
for i in theme_after.values:
    for j in i:
        l.append(j)

followers_after = pd.read_sql("SELECT user_followers_count FROM {} WHERE user_followers_count>10000 and created_at >= '2020-02-27 18:07:40'".format(settings.TABLE_NAME), con=mydb)
tweet_counter_after = pd.read_sql("SELECT tweet_count FROM {} WHERE user_followers_count>10000 and created_at >= '2020-02-27 18:07:40'".format(settings.TABLE_NAME), con=mydb)

sanders_after = pd.read_sql("SELECT  id_str, text, created_at, sentiment, user_location, atr, polarity as polarity_sanders, subjectivity as subjectivity_sanders FROM {} WHERE atr = 'BERNIE SANDERS' and created_at >= '2020-02-27 18:07:40'".format(settings.TABLE_NAME), con=mydb)
warren_after = pd.read_sql("SELECT  id_str, text, created_at, sentiment, user_location, atr, polarity as polarity_warren, subjectivity as subjectivity_warren FROM {} WHERE atr = 'ELIZABETH WARREN' and created_at >= '2020-02-27 18:07:40'".format(settings.TABLE_NAME), con=mydb)
bloom_after = pd.read_sql("SELECT  id_str, text, created_at, sentiment, user_location, atr, polarity as polarity_bloomberg, subjectivity as subjectivity_bloomberg FROM {} WHERE atr = 'MIKE BLOOMBERG' and created_at >= '2020-02-27 18:07:40'".format(settings.TABLE_NAME), con=mydb)


#Tables with the number of attributes for each track word
followers_af = Counter(followers_after['user_followers_count'], l, 'Candidates', 'Number of followers')
UserTweets_af = Counter(tweet_counter_after['tweet_count'], l, 'Candidates', 'Number of users tweets')
tweets_no_af = NumberofTweets(theme_after['atr'], l, 'Candidates', 'Number of tweets')

BarPlot(followers_af, 'Candidates', 'Number of followers', ('#ff4554', '#ff6714', '#a12222'))
BarPlot(UserTweets_af, 'Candidates', 'Number of users tweets',  ('#ff8000', '#dc6900', '#ffce26'))
BarPlot(tweets_no_af, 'Candidates', 'Number of tweets',  ('#00c3e3', '#7170ff', '#8afccf'))

#Time series graph for the flactuation of the sentiment through time
Timeseries(sanders_after, settings.TRACK_WORDS[0])
Timeseries(warren_after, settings.TRACK_WORDS[1])
Timeseries(bloom_after, settings.TRACK_WORDS[2])

#Denity plots for the sentiment analysis at polarity and subjectivity for the track words
Densityplots(sanders_after["polarity_sanders"], warren_after["polarity_warren"], bloom_after["polarity_bloomberg"])
Densityplots(sanders_after["subjectivity_sanders"], warren_after["subjectivity_warren"], bloom_after["subjectivity_bloomberg"])

#Count the sentiment from each category
cursor = mydb.cursor()
cursor.execute("select sentiment,count(sentiment) from main.tweet group by sentiment;")
rows = cursor.fetchall()
cursor.execute("select count(sentiment) from main.tweet where atr = 'BERNIE SANDERS' and created_at >= '2020-02-27 18:07:40' group by sentiment;")
sanders_a = [item[0] for item in cursor.fetchall()]
cursor.execute("select count(sentiment) from main.tweet where atr = 'ELIZABETH WARREN' and created_at >= '2020-02-27 18:07:40' group by sentiment;")
warren_a = [item[0] for item in cursor.fetchall()]
cursor.execute("select count(sentiment) from main.tweet where atr = 'MIKE BLOOMBERG' and created_at >= '2020-02-27 18:07:40' group by sentiment;")
bloomberg_a = [item[0] for item in cursor.fetchall()]

CategoricalSentiment(sanders_a, 'Categorical sentiment for BERNIE SANDERS')
CategoricalSentiment(warren_a, 'Categorical sentiment for ELIZABETH WARREN')
CategoricalSentiment(bloomberg_a, 'Categorical sentiment for MIKE BLOOMBERG')


#Visualization with high frequency words
combi = pd.read_sql("SELECT  text FROM {}".format(settings.TABLE_NAME), con=mydb)
all_words = ' ' .join([text for text in combi['text']])
combi = pd.read_sql("SELECT  text FROM {}".format(settings.TABLE_NAME), con=mydb)

all_words = ' ' .join([text for text in combi['text']])
wordcloud = WordCloud(width = 800, height = 500).generate(all_words)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()