#!env/bin/python3
# -*- coding: utf-8 -*-
import requests, re
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from bs4 import BeautifulSoup

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test-bowlers-howstat.db'
db = SQLAlchemy(app)

class Bowler(db.Model):
    __tablename__ = 'bowlers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), index=True)
    bowled = db.Column(db.Integer)
    caught = db.Column(db.Integer)
    caught_behind = db.Column(db.Integer)
    lbw = db.Column(db.Integer)
    stumped = db.Column(db.Integer)
    hit_wicket = db.Column(db.Integer)
    total = db.Column(db.Integer)

    def __init__(self, **kwargs):
        super(Bowler, self).__init__(**kwargs)

    def __repr__(self):
        return self.name

db.create_all()
# Fetch from Howstat

def get_url(player):
    url = "http://www.howstat.com.au/cricket/Statistics/Players/PlayerDismissBowlGraph.asp?PlayerID={}".format(player)
    return url

for i in range(24, 3176): #3176
    i = '{0:04}'.format(i)
    url = get_url(i)
    print(url)

    player_page = requests.get(url)

    if player_page.status_code is 200:
        soup = BeautifulSoup(player_page.text, 'html.parser')

        player_name = soup.title.string.split(" - ")[1]

        bowled = soup.find(text=re.compile('Bowled'))

        if bowled is not None:
            bowled = bowled.findNext('td').text.strip()
            caught = soup.find(text=re.compile('Caught')).findNext('td').text.strip()
            caught_behind = soup.find(text=re.compile('Caught Behind')).findNext('td').text.strip()
            lbw = soup.find(text=re.compile('LBW')).findNext('td').text.strip()
            stumped = soup.find(text=re.compile('Stumped')).findNext('td').text.strip()
            hit_wicket = soup.find(text=re.compile('Hit Wicket')).findNext('td').text.strip()

            bowler_table = {"name":player_name, "bowled":bowled, "caught":caught,
                            "caught_behind":caught_behind, "lbw":lbw, "stumped":stumped,
                            "hit_wicket":hit_wicket}

            player = Bowler(name=player_name, bowled=bowled, caught=caught,
                            caught_behind=caught_behind, lbw=lbw, stumped=stumped,
                            hit_wicket=hit_wicket)
            db.session.add(player)
            db.session.commit()
            print(bowler_table) #[0].strip()

# bowlers = Bowler.query.all()

