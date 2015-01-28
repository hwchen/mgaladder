#! /usr/bin/env python3

# Flask server for MGA ladder

import os

from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute, NumberAttribute
)

from flask import Flask, jsonify

app = Flask(__name__, static_url_path='')

@app.route('/')
def index():
    """ serves static file for testing purposes"""
    return app.send_static_file('index.html') 

@app.route('/results')
def results():
    resultsList = {"results": [
        {"black": "Walther", "white": "Andrew"},
        {"black": "Walther", "white": "Chun"}
        ]}
    return jsonify(resultsList)

@app.route('/rankings')
def rankings():
    rankingsList = {"rankings": [
        {"Walther": "5d"},
        {"Andrew": "1k"}
        ]}
    return jsonify(rankingsList)

# Database

class DB_players (Model):
    class Meta:
        table_name = 'players'
        host = 'http://localhost:8000'
    player_id = NumberAttribute(hash_key=True)
    player_name = UnicodeAttribute(range_key=True)

def test():
    print('hello world')

if __name__ == '__main__':
    if not DB_players.exists():
        DB_players.create_table(read_capacity_units=1,
                                write_capacity_units=1,
                                wait=True)
    app.run(debug=True)
