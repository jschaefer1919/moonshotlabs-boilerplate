from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db


analyst = Blueprint('analyst', __name__)

# returns basic info on a player
@analyst.route('/playerinfo/<surname>', methods=['GET'])
def get_player_info(surname):
    cursor = db.get_db().cursor()
    
    cursor.execute('SELECT p_fName, p_lName, player_id, position, age, draft_year, pick_number,college, salary, cur_team, jersey_number \
                    FROM Player WHERE p_lName = "' + surname + '";')

    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# creates a new player profile/info in the DB
@analyst.route('/newplayer', methods = ['POST'])
def create_new_player():
   the_data = request.json
   current_app.logger.info(the_data)

   fName = the_data['p_fName']
   lName = the_data['p_lName']
   age = the_data['age']
   position = the_data['position']
   salary = the_data['salary']
   team = the_data['cur_team']
   draft_yr = the_data['draft_year']
   pick_num = the_data['pick_number']
   college = the_data['college']
   jersey_num = the_data['jersey_number']

   query = 'insert into Player (p_fname, p_lname, age, position, salary, cur_team, draft_year, pick_number, college, jersey_number) values ("'
   query += fName + '", "'
   query += lName + '", '
   query += str(age) + ', "'
   query += position + '", '
   query += str(salary) + ', "'
   query += team + '", '
   query += str(draft_yr) + ', '
   query += str(pick_num) + ', "'
   query += college + '", '
   query += str(jersey_num) + ');'''

   current_app.logger.info(query)

   cursor = db.get_db().cursor()
   cursor.execute(query)
   db.get_db().commit()

   return 'Success!'

# updates an existing player's info in the DB
@analyst.route('/updateplayer', methods = ['PUT'])
def update_player_profile():   
   the_data = request.json
   current_app.logger.info(the_data)
   
   fName = the_data['p_fName2']
   lName = the_data['p_lName2']
   age = the_data['age2']
   position = the_data['position2']
   salary = the_data['salary2']
   team = the_data['cur_team2']
   draft_yr = the_data['draft_year2']
   pick_num = the_data['pick_number2']
   college = the_data['college2']
   jersey_num = the_data['jersey_number2']
   id = the_data['player_id2']

   query = 'UPDATE Player SET p_fName = "'
   query += fName + '", p_lName = "'
   query += lName + '", age = '
   query += str(age) + ', position = "'
   query += position + '", salary = '
   query += str(salary) + ', cur_team = "'
   query += team + '", draft_year = '
   query += str(draft_yr) + ', pick_number = '
   query += str(pick_num) + ', college = "'
   query += college + '", jersey_number = '
   query += str(jersey_num) + ' WHERE player_id ='
   query += str(id) + ';' 
   
   current_app.logger.info(query)

   cursor = db.get_db().cursor()
   cursor.execute(query)
   db.get_db().commit()

   return 'Success!'

# removes a highlight from the DB
@analyst.route('/delhighlight', methods = ['DELETE'])
def remove_highlight():
   the_data = request.json
   current_app.logger.info(the_data)
   
   clip_id = the_data['clip_id']
   game_id = the_data['game_id']

   query = 'DELETE FROM Highlight WHERE clip_id = '
   query += str(clip_id) + ' AND game_id = '
   query += str(game_id) + ';'

   current_app.logger.info(query)

   cursor = db.get_db().cursor()
   cursor.execute(query)
   db.get_db().commit()

   return 'Success!'

# gets the advnaced stats on a team
@analyst.route('/advstats/<team_ID>', methods=['GET'])
def get_advstats(team_ID):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT team_name, wgdp, spd, iso, bb_percent, slugg_percent, run_diff \
                        FROM Advanced_Stats JOIN Team USING (team_id) WHERE team_id = {0};'.format(team_ID))
    
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# gets the top 5 pitches in the league based on era
@analyst.route('/toppitchers', methods=['GET'])
def get_top_pitchers():
    cursor = db.get_db().cursor()

    cursor.execute('SELECT p_fName, p_lName, cur_team, era FROM Player JOIN Player_Stats USING (player_id)\
                    WHERE position = "Pitcher" ORDER BY era DESC LIMIT 5;')
    
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# gets the stats for all players on a team
@analyst.route('/playerstats/<team_ID>', methods=['GET'])
def get_playerstats_team(team_ID):
    cursor = db.get_db().cursor()    
    
    cursor.execute('SELECT cur_team,p_fName, p_lName, position, rbi, hits, ks, slg, obs, era, \
        bat_avg, games_played FROM Player JOIN Player_Stats USING (player_id) WHERE team_id = {0};'.format(team_ID))

    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# gets the injury history of a player based on last name
@analyst.route('/injuryhistory/<p_lNAME>', methods=['GET'])
def get_player_injury_history(p_lNAME):
    cursor = db.get_db().cursor()
    
    query = 'SELECT p_fName, p_lName,title, upd_body, injury_date FROM Player JOIN Injury_Update USING (player_id) \
                        WHERE p_lName = "'
    query += p_lNAME + '";'

    cursor.execute(query)

    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# get the player_id of a player in the DB based on last name - used for dev in appsmith
@analyst.route('/playerprof/<last_name>', methods=['GET'])
def get_playerid(last_name):
    cursor = db.get_db().cursor()
    
    query = 'SELECT player_id FROM Player WHERE p_lName = "'
    query += last_name + '";'
    cursor.execute(query)
    
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))

    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response
