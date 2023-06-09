from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db


bettor = Blueprint('bettor', __name__)

# getting the bet stats for a team
@bettor.route('/bettingstats/<team_ID>', methods=['GET'])
def get_betstats(team_ID):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT team_name, home_money, ats, mov, cover_percent FROM Bet_Stats JOIN Team USING (team_id) \
                        WHERE team_id = {0};'.format(team_ID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# getting the team stats for a team
@bettor.route('/teamstats/<team_ID>', methods=['GET'])
def get_teamstats(team_ID):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT team_name, location, coach_1, coach_2, wins, losses, avg_on_base, \
       avg_era, total_hits, total_rbi, total_ks, team_bat_avg \
            FROM Team_Stats JOIN Team USING (team_id) WHERE team_ID = {0};'.format(team_ID))

    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# creating a new bet slip in the DB
@bettor.route('/bet', methods = ['POST'])
def create_new_bet():
   the_data = request.json
   current_app.logger.info(the_data)

   bet = the_data['bet_type']
   description = the_data['bet_description']
   amount = the_data['amount']
   game = the_data['game_id']
   ssn = the_data['ssn']

   query = 'insert into Bet_Slip (bet_type, bet_description, amount, game_id, ssn) values ("'
   query += bet + '", "'
   query += description + '", '
   query += str(amount) + ', '
   query += str(game) + ', "'
   query += str(ssn) + '")'''
   current_app.logger.info(query)

   cursor = db.get_db().cursor()
   cursor.execute(query)
   db.get_db().commit()

   return 'Success!'

# updating a bet post game with the results
@bettor.route('/updatebet', methods = ['PUT'])
def update_finalized_bet():   
   the_data = request.json
   current_app.logger.info(the_data)

   id = the_data['bet_id']
   payout = the_data['payout']
   rate = the_data['return_rate']

   query = 'UPDATE Bet_Slip SET payout ='
   query += str(payout) + ', return_rate ='
   query += str(rate) + ' WHERE bet_id ='
   query += str(id) + ';'
   
   current_app.logger.info(query)

   cursor = db.get_db().cursor()
   cursor.execute(query)
   db.get_db().commit()

   return 'Success!'

# creating a new article for the user/DB archive
@bettor.route('/article', methods = ['POST'])
def create_new_article():
   the_data = request.json
   current_app.logger.info(the_data)

   link = the_data['new_hyperlink']
   article_title = the_data['title']
   body = the_data['article_body']
   
   query = 'INSERT INTO News_Article (hyperlink, title, article_body) VALUES ("'
   query +=  link + '", "'
   query += article_title + '", "'
   query += body + '");'''

   current_app.logger.info(query)

   cursor = db.get_db().cursor()
   cursor.execute(query)
   db.get_db().commit()

   return 'Success!'

# deleting an article from the archive
@bettor.route('/deletearticle', methods = ['DELETE'])
def remove_article():
   the_data = request.json
   current_app.logger.info(the_data)
   
   link = the_data['hyperlink']
   
   query = 'DELETE FROM News_Article WHERE hyperlink = "'
   query += link + '";'

   current_app.logger.info(query)

   cursor = db.get_db().cursor()
   cursor.execute(query)
   db.get_db().commit()

   return 'Success!'

#  getting a bettor's account balance
@bettor.route('/earnings/<account_NO>', methods=['GET'])
def get_earnings(account_NO):
    cursor = db.get_db().cursor()

    query = 'SELECT balance, fName, lName, username, age, ssn FROM Earnings_Account \
                JOIN Account_Profile USING (ssn) WHERE account_no = {0};'.format(account_NO) 
    
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

# get game results and all bets placed on a game
@bettor.route('/betinfo/<game_id>', methods=['GET'])
def get_article(game_id):
    cursor = db.get_db().cursor()

    query = 'SELECT result, game_date, home_team, away_team, home_score, away_score, bet_type, bet_description, amount, payout \
    FROM Game JOIN Game_Stats USING (game_id) JOIN Bet_Slip USING (game_id) WHERE game_id = {0};'.format(game_id) 
    
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

# get a list of games based from a date on - for appsmith development
@bettor.route('/gameid/<date>', methods=['GET'])
def get_gameid2(date):
    cursor = db.get_db().cursor()
    
    query = 'SELECT game_date, result, home_team, away_team, game_id FROM Game WHERE game_date >= "'
    query += str(date) + '" ORDER BY game_date ASC LIMIT 5;' 

    cursor.execute(query)
    
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        current_app.logger.info(row)
        json_data.append(dict(zip(row_headers, row)))
    
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# get the bet id of the last placed bet - for appsmith development
@bettor.route('/recentbetid', methods=['GET'])
def max_betid():
    cursor = db.get_db().cursor()
    
    query = 'SELECT MAX(bet_id) AS user_bet_id FROM Bet_Slip;'

    cursor.execute(query)
    
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        current_app.logger.info(row)
        json_data.append(dict(zip(row_headers, row)))
    
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response