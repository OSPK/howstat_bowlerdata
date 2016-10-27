#!env/bin/python3
# -*- coding: utf-8 -*-
import requests, re
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from bs4 import BeautifulSoup

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///oneday-batsmen-cricinfo.db'
db = SQLAlchemy(app)

class Batsman(db.Model):
    __tablename__ = 'batsmen'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), index=True)
    country = db.Column(db.String(80))
    span = db.Column(db.String(80))
    matches = db.Column(db.Integer)
    innings = db.Column(db.Integer)
    not_out = db.Column(db.Integer)
    runs = db.Column(db.Integer)
    highest_score = db.Column(db.Integer)
    average = db.Column(db.Integer)
    hundreds = db.Column(db.Integer)
    fifties = db.Column(db.Integer)
    ducks = db.Column(db.Integer)

    def __init__(self, **kwargs):
        super(Batsman, self).__init__(**kwargs)

    def __repr__(self):
        return self.name + ": " + str(self.runs)

db.create_all()

# Fetch from Cricinfo
def get_page(page):
    url = "http://stats.espncricinfo.com/ci/engine/stats/index.html?class=2;filter=advanced;orderby=runs;page={};size=200;template=results;type=batting".format(page)
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
            not_out = innings.findNext('td')
            runs = not_out.findNext('td')
            highest_score = runs.findNext('td')
            average = highest_score.findNext('td')
            hundreds = average.findNext('td')
            fifties = hundreds.findNext('td')
            ducks = fifties.findNext('td')

            player = Batsman(name=name, country=country, span=span.text,
                      matches=matches.text, innings=innings.text, not_out=not_out.text,
                      runs=runs.text, highest_score=highest_score.text,
                      average=average.text, hundreds=hundreds.text,
                      fifties=fifties.text, ducks=ducks.text)

            print(player)
            db.session.add(player)
            db.session.commit()

# # bowlers = Bowler.query.all()

