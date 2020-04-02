import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import mysql.connector
import  settings
import numpy as np
import mysql.connector

Northeast =['NEW ENGLAND', 'CONNECTICUT', 'MAINE', 'MASSACHUSETTS', 'NEW HAMPSHIRE', 'RHODE ISLAND', 'VERMONT', 'MID-ATLANTIC',
            'NEW JERSEY', 'NEW YORK', 'NEW JERSEY', 'PENNSYLVANIA']
Midwest =['EAST NORTH CENTRAL', 'ILLINOIS', 'INDIANA', 'MICHIGAN', 'OHIO', 'WISCONSIN', 'WEST NORTH CENTRAL', 'IOWA', 'KANSAS',
          'MINNESOTA', 'MISSOURI', 'NEBRASKA', 'NORTH DAKOTA', 'SOUTH DAKOTA']
South =['SOUTH ATLANTIC', 'DELAWARE', 'FLORIDA', 'GEORGIA', 'MARYLAND', 'NORTH CAROLINA', 'SOUTH CAROLINA', 'VIRGINIA',
        'DISTRICT OF COLUMBIA', 'WEST VIRGINIA', 'EAST SOUTH CENTRAL', 'ALABAMA', 'KENTUCKY', 'MISSISSIPPI', 'TENNESSEE',
        'WEST SOUTH CENTRAL', 'ARKANSAS', 'LOUISIANA', 'OKLAHOMA', 'TEXAS']
West =['MOUNTAIN', 'ARIZONA', 'COLORADO', 'IDAHO', 'MONTANA', 'NEVADA', 'NEW MEXICO', 'UTAH', 'WYOMING', 'PACIFIC',
       'ALASKA', 'CALIFORNIA', 'HAWAII', 'OREGON', 'WASHINGTON',  'SEATTLE']

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database=""

)

location = pd.read_sql('SELECT user_location, polarity FROM {}'.format(settings.TABLE_NAME), con=mydb)
northeast = {}
midwest = {}
south = {}
west = {}

ne = 0
mw = 0
so = 0
we = 0
other = 0


for loc in location['user_location']:
    if loc != None:

        if loc.upper() in Northeast:
            ne +=1
            northeast[loc] = location['polarity']
        elif loc.upper() in Midwest:
            mw +=1
            midwest[loc] = location['polarity']
        elif loc.upper() in South:
            so += 1
            south[loc] = location['polarity']
        elif loc.upper() in West:
            we += 1
            west[loc] = location['polarity']
        else:
            other += 1





dt = [ne, mw, so, we]
su = ne + mw + so + we
d = sns.kdeplot(dt, shade=True, color="r")
plt.show()
data = [('Northeast', (ne*100)/su), ('Midwest', (mw*100)/su), ('South', (so*100)/su), ('West', (we*100)/su)]
freq = pd.DataFrame(data, columns=['Location', 'Number of tweets'])
height = freq['Number of tweets']
bars = freq['Location']
y_pos = np.arange(len(bars))
plt.bar(y_pos, height, color=('#ff4554', '#ff6714', '#a12222'))
plt.title('Percentage % of tweets distribution at US Regions')
plt.xticks(y_pos, bars)
plt.show()

