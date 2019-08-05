import requests
import logging
from datetime import date, timedelta

logger = logging.getLogger(__name__)

class fafapi:
    """
    Class for api stuff
    """
    def __init__(self, url):
        self.url = url

    
    def get_token(self, username, password):
        uri = self.url + "oauth/token"
        querystring = {"client_id":"postman","client_secret":"postman","grant_type":"password","username":username,"password":password}
        headers = {
        'cache-control': "no-cache"
        }
        try:
            response = requests.request("POST", uri, headers=headers, params=querystring)
            if response.status_code != 200:
                response.raise_for_status() 
            elif response.status_code == 200:
                data = response.json()
                token = data['access_token']
        except requests.exceptions.HTTPError:
            logger.warning('request error, response code is %s', response.status_code)
            token = "error"
        
        return token

    def get_clan_info(self, token, clan_id):
        uri = self.url + "data/clan/" + str(clan_id)
        headers = {
        'cache-control': "no-cache",
        'Authorization': "Bearer " + token
        }
        try:
            response = requests.request("GET", uri, headers=headers)
            if response.status_code != 200:
                response.raise_for_status() 
            elif response.status_code == 200:
                data = response.json()
        except requests.exceptions.HTTPError:
            logger.warning('request error, response code is %s', response.status_code)
            data = "error"
        
        return data

    def get_player_info(self, token, player_id):
        uri = self.url + "data/player/" + str(player_id)
        headers = {
        'cache-control': "no-cache",
        'Authorization': "Bearer " + token
        }
        try:
            response = requests.request("GET", uri, headers=headers)
            if response.status_code != 200:
                response.raise_for_status() 
            elif response.status_code == 200:
                data = response.json()
        except requests.exceptions.HTTPError:
            logger.warning('request error, response code is %s', response.status_code)
            data = "error"
        
        return data
    
    def get_clan_player(self, token, membership_id):
        uri = self.url + "data/clanMembership/" + str(membership_id) + "/player"
        headers = {
        'cache-control': "no-cache",
        'Authorization': "Bearer " + token
        }
        try:
            response = requests.request("GET", uri, headers=headers)
            if response.status_code != 200:
                response.raise_for_status() 
            elif response.status_code == 200:
                data = response.json()
        except requests.exceptions.HTTPError:
            logger.warning('request error, response code is %s', response.status_code)
            data = "error"
        
        return data

    def get_rating_player(self, token, rating_type, player_id):
        if rating_type == 'global':
            uri = self.url + "data/globalRating/" + str(player_id)
            logger.debug(uri)
        elif rating_type == 'ladder':
            uri = self.url + "data/ladder1v1Rating/" + str(player_id)
            logger.debug(uri)
        else:
            logger.warning('No rating type supplied')
            exit() 
        headers = {
        'cache-control': "no-cache",
        'Authorization': "Bearer " + token
        }
        try:
            response = requests.request("GET", uri, headers=headers)
            if response.status_code != 200:
                response.raise_for_status() 
            elif response.status_code == 200:
                data = response.json()
        except requests.exceptions.HTTPError:
            logger.warning('request error, response code is %s', response.status_code)
            data = "error"
        
        return data

    def generate_rating_list(self, token, clan_id):
        if token != "error":
            logger.debug(token)
            apireq = fafapi(self.url)
            clan_info = apireq.get_clan_info(token, clan_id)
            clan_name = clan_info['data']['attributes']['name']
            logger.debug("Clan Name : {}" .format(clan_name))
            leader_id = clan_info['data']['relationships']['leader']['data']['id']
            leader_data = apireq.get_player_info(token, leader_id)
            leader = leader_data['data']['attributes']['login']
            logger.debug("Clan Leader : {}" .format(leader))
            ratings_list = []
            for member in clan_info['data']['relationships']['memberships']['data']:
                clan_player_id = member['id']
                player = apireq.get_clan_player(token, clan_player_id)
                player_name = player['data']['attributes']['login']
                logger.debug("Player : {}" .format(player_name))
                global_rating = apireq.get_rating_player(token, "global", player['data']['id'])
                global_rating_int = int(global_rating['data']['attributes']['rating'])
                logger.debug("{} Global Rating is : {}".format(player_name, global_rating_int))
                ladder1v1_rating = apireq.get_rating_player(token, "ladder", player['data']['id'])
                ladder1v1_rating_int = int(ladder1v1_rating['data']['attributes']['rating'])
                logger.debug("{} Ladder Rating is : {}".format(player_name, ladder1v1_rating_int))
                ratings_list.append('player_ratings' + ',' + 'player=' + player_name \
                    + ',' + 'clan=' + 'TUS' + ' ' + 'GlobalRating=' + str(global_rating_int))
                ratings_list.append('player_ratings' + ',' + 'player=' + player_name \
                    + ',' + 'clan=' + 'TUS' + ' ' + 'LadderRating=' + str(ladder1v1_rating_int))
   
            return ratings_list
        else:
            logger.warn('Invalid Token')
            return 'error'
    
    def get_player_gameStats(self, token, player_id):
        """
        Gets gates and some info from the players previous games
        """
        #Set date to the previous month so we only capture 4 weeks of games
        current_date = date.today() - timedelta(weeks=+4)
        format_date = current_date.strftime('%Y-%m-%dT%H:%M:%S') + 'Z'
        
        uri = self.url + 'data/gamePlayerStats?filter=player.id%3D%3D' + str(player_id) + ' and ' + 'scoreTime%3E' + format_date
        headers = {
        'cache-control': "no-cache",
        'Authorization': "Bearer " + token
        }
        try:
            response = requests.request("GET", uri, headers=headers)
            if response.status_code != 200:
                response.raise_for_status() 
            elif response.status_code == 200:
                data = response.json()
        except requests.exceptions.HTTPError:
            logger.warning('request error, response code is %s', response.status_code)
            data = "error"
        
        return data

    def get_player_game(self, token, game_id):
        """
        Gets gates and some info from a game
        """
        
        uri = self.url + 'data/game/' + str(game_id)
        headers = {
        'cache-control': "no-cache",
        'Authorization': "Bearer " + token
        }
        try:
            response = requests.request("GET", uri, headers=headers)
            if response.status_code != 200:
                response.raise_for_status() 
            elif response.status_code == 200:
                data = response.json()
        except requests.exceptions.HTTPError:
            logger.warning('request error, response code is %s', response.status_code)
            data = "error"
        
        return data

    def generate_games_list(self, token, player_id):
        """
        Adds games to influx
        """
        recent_games = self.get_player_gameStats(token, player_id)
        player = self.get_player_info(token, player_id)
        player_name = player['data']['attributes']['login']
        games_list = []
        for game in recent_games['data']:
            if game['attributes']['afterDeviation'] != None:
                logger.debug('Game ID : {}' .format(game['relationships']['game']['data']['id']))
                game_id = game['relationships']['game']['data']['id']

                game_data = self.get_player_game(token, game_id)
                game_name = game_data['data']['attributes']['name']
                start_time = game_data['data']['attributes']['startTime']
                end_time = game_data['data']['attributes']['endTime']
                if game_data['data']['attributes']['validity'] == 'VALID':
                    ranked = 'YES'
                else:
                    ranked = 'NO'
                
                games_list.append('player_games' + ',' + 'player=' + player_name \
                    + ',' + 'clan=' + 'TUS' + ' ' + 'Game_Name=' + game_name \
                    + ' ' + 'Start_Time=' + str(start_time) + ' ' + 'End_Time=' + str(end_time) \
                    + ' ' + 'Ranked=' + ranked)

        return games_list

