from fafclient import fafapi
from influxclient import influxclient
import logging
import argparse

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def GetArgs():
   """
   Supports the command-line arguments listed below.
   """

   parser = argparse.ArgumentParser(description='Process args for powering on a Virtual Machine')
   parser.add_argument('-a', '--address', required=True, action='store', help='Remote host to connect to')
   parser.add_argument('-u', '--user', required=True, action='store', help='User name to use when connecting to host')
   parser.add_argument('-p', '--password', required=True, action='store', help='Password to use when connecting to host')
   parser.add_argument('-c', '--clanid', required=True, action='store', help='ID of the FAF Clan')
   parser.add_argument('-i', '--influxserver', required=True, action='store', help='Remote influx api endpoint')
   parser.add_argument('-x', '--influxport', required=True, action='store', help='Remote influx api endpoint port')
   parser.add_argument('-o', '--influxorg', required=True, action='store', help='Influx Org Name')
   parser.add_argument('-b', '--influxbucket', required=True, action='store', help='Influx Bucket Name')
   parser.add_argument('-t', '--influxtoken', required=True, action='store', help='Influx API Token')
   args = parser.parse_args()
   return args
args = GetArgs()

# Set variables
host = "https://" + args.address + "/"
username = args.user
password = args.password
clan_id = args.clanid
influx_host = args.influxserver
influx_port = args.influxport
influx_org = args.influxorg
influx_bucket = args.influxbucket
influx_token = args.influxtoken



logger.debug(host)
apireq = fafapi(host)
client = influxclient(influx_host, influx_port, influx_org, influx_token, influx_bucket)
token = apireq.get_token(username, password)
if token != "error":
    logger.debug(token)
    clan_info = apireq.get_clan_info(token, clan_id)
    clan_name = clan_info['data']['attributes']['name']
    logger.debug("Clan Name : {}" .format(clan_name))
    leader_id = clan_info['data']['relationships']['leader']['data']['id']
    leader_data = apireq.get_player_info(token, leader_id)
    leader = leader_data['data']['attributes']['login']
    logger.debug("Clan Leader : {}" .format(leader))
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
        client.write('player_ratings' + ',' + 'player=' + player_name \
            + ',' + 'clan=' + 'TUS' + ' ' + 'GlobalRating=' + str(global_rating_int))
        client.write('player_ratings' + ',' + 'player=' + player_name \
            + ',' + 'clan=' + 'TUS' + ' ' + 'LadderRating=' + str(ladder1v1_rating_int))
else:
    print("Any error occured getting token")

#def generate_influx_data()

print('done')
