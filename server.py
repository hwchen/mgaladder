#! /usr/bin/env python3

# Flask server for MGA ladder

import yaml

from ladder import *

import os

from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute,
    NumberAttribute,
    JSONAttribute,
    UTCDateTimeAttribute,
    BooleanAttribute
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

# Database schema and setup

# basically, a different model for each possible query.
# for nosql, the idea is to be flat, duplicating data and
# de-normalizing for easier queries is fine (or even good)

class Ladder (Model):
    class Meta:
        table_name = 'Ladder'
        host = 'http://localhost:8000'
    ladder_id = NumberAttribute(hash_key=True)
    ladder_name = UnicodeAttribute()
    standings = JSONAttribute()
    player_count = NumberAttribute()
    last_action_id = NumberAttribute()

class Player (Model):
    class Meta:
        table_name = 'Player'
        host = 'http://localhost:8000'
    player_id = NumberAttribute (hash_key=True)
    aga_id = NumberAttribute()
    name = UnicodeAttribute()
    rank = UnicodeAttribute()

class AdminAction (Model):
    class Meta:
        table_name = 'AdminAction'
        host = 'http://localhost:8000'
    ladder_id = NumberAttribute(hash_key=True)
    timestamp = UnicodeAttribute(range_key=True)
    action_type = UnicodeAttribute() # add, drop, del, rank
    player_id = UnicodeAttribute()
    player_rank = UnicodeAttribute(null=True)

class Result (Model):
    class Meta:
        table_name = 'Result'
        host = 'http://localhost:8000'
    ladder_id = NumberAttribute(hash_key=True)
    timestamp = UnicodeAttribute(range_key=True) #can change to UTC
    game_black_id = NumberAttribute()
    game_white_id = NumberAttribute()
    game_winner_id = NumberAttribute()
    rated = BooleanAttribute()

def init_db():
    if not Ladder.exists():
        Ladder.create_table(read_capacity_units=1,
                                write_capacity_units=1,
                                wait=True)
    if not Player.exists():
        Player.create_table(read_capacity_units=1,
                                write_capacity_units=1,
                                wait=True)
    if not AdminAction.exists():
        AdminAction.create_table(read_capacity_units=1,
                                write_capacity_units=1,
                                wait=True)
    if not Result.exists():
        Result.create_table(read_capacity_units=1,
                                write_capacity_units=1,
                                wait=True)

#Read in results
def populate_db(file_path):
    stream = open(file_path, 'r')
    ladder_info = yaml.load(stream)

    # map to Ladder table
    # best way to check for existing item? try/except?
    ladder_id = 1 #for testing purposes
    ladder_name = 'MGA Ladder'
    standings = ladder_info['standings'] 
    player_count = ladder_info['id_ctr']
    last_action_id = 1 #(for testing purposes)

    new_ladder = Ladder(ladder_id      = ladder_id,
                        ladder_name    = ladder_name,
                        standings      = standings,
                        player_count   = player_count,
                        last_action_id = last_action_id)
    new_ladder.save()

    # map to Player table
    for key, value in ladder_info['players'].items():
        player_id = key 
        rank = value['rank']
        aga_id = value['aga_id']
        name = value['name']
        new_player = Player(player_id = player_id,
                            aga_id    = aga_id,
                            name      = name,
                            rank      = rank)
        new_player.save()

    # map to AdminAction table

    # map to Result table
    # ladder_id already assigned above 
    for res in ladder_info['results']:
        timestamp = res['time']
        game_black_id = res['black']
        game_white_id = res['white']
        game_winner_id = res['winner']
        rated = res['rated']
        new_res = Result(ladder_id = ladder_id,
                         timestamp = timestamp,
                         game_black_id = game_black_id,
                         game_white_id = game_white_id,
                         game_winner_id = game_winner_id,
                         rated = rated)
        new_res.save()
        
    return ladder_info

#Modify routes to enter db info, put up admin page
    

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
