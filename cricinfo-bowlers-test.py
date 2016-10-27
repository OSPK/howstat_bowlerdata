#!env/bin/python3
# -*- coding: utf-8 -*-
import requests, re
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from bs4 import BeautifulSoup

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test-bowlers-cricinfo.db'
db = SQLAlchemy(app)

class Bowler(db.Model):
    __tablename__ = 'bowlers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), index=True)
    country = db.Column(db.String(80))
    span = db.Column(db.String(80))
    matches = db.Column(db.Integer)
    innings = db.Column(db.Integer)
    balls = db.Column(db.Integer)
    runs = db.Column(db.Integer)
    wickets = db.Column(db.Integer)
    bbi = db.Column(db.Integer)
    bbm = db.Column(db.Integer)
    average = db.Column(db.Integer)
    economy = db.Column(db.Integer)
    strike_rate = db.Column(db.Integer)
    fives = db.Column(db.Integer)
    tens = db.Column(db.Integer)

    def __init__(self, **kwargs):
        super(Bowler, self).__init__(**kwargs)

    def __repr__(self):
        return self.name + ": " + str(self.runs)

db.create_all()

# Fetch from Cricinfo
def get_page(page):
    url = "http://stats.espncricinfo.com/ci/engine/stats/index.html?class=1;filter=advanced;orderby=wickets;page={};size=200;template=results;type=bowling".format(page)
    return url

for i in range(1, 16):
    url = get_page(i)
    print(url)

    get_results = requests.get(url)

    if get_results.status_code is 200:

        soup = BeautifulSoup(get_results.text, 'html.parser')

        data = soup.find_all('tr', attrs={'class': 'data1'})

        for row in data:
            first_td = row.findNext('td')
            name = first_td.text.split("(")[0].strip()
            country = first_td.text.split("(")[1].strip(")").strip()
            span = first_td.findNext('td')
            matches = span.findNext('td')
            innings = matches.findNext('td')
            balls = innings.findNext('td')
            runs = balls.findNext('td')
            wickets = runs.findNext('td')
            bbi = wickets.findNext('td')
            bbm = bbi.findNext('td')
            average = bbm.findNext('td')
            economy = average.findNext('td')
            strike_rate = economy.findNext('td')
            fives = strike_rate.findNext('td')
            tens = fives.findNext('td')

            player = Bowler(name=name, country=country, span=span.text,
                            matches=matches.text, innings=innings.text, balls=balls.text,
                            runs=runs.text, wickets=wickets.text, bbi=bbi.text,
                            bbm=bbm.text, average=average.text, economy=economy.text,
                            strike_rate=strike_rate.text, fives=fives.text, tens=tens.text)

            print(player)
            db.session.add(player)
            db.session.commit()

# # bowlers = Bowler.query.all()

