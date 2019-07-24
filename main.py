from fafclient import fafapi
import logging
import argparse

logging.basicConfig(level=logging.INFO)
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
   args = parser.parse_args()
   return args
args = GetArgs()
host = "https://" + args.address + "/"
username = args.user
password = args.password
clan_id = args.clanid
print(host)
apireq = fafapi(host)

token = apireq.get_token(username, password)
if token != "error":
    print(token)
    clan_info = apireq.get_clan_info(token, clan_id)
    print("Clan Name : ", clan_info['data']['attributes']['name'])
    leader_id = clan_info['data']['relationships']['leader']['data']['id']
    leader_data = apireq.get_player_info(token, leader_id)
    leader = leader_data['data']['attributes']['login']
    print("Clan Leader :", leader)
    for member in clan_info['data']['relationships']['memberships']['data']:
        clan_player_id = member['id']
        player = apireq.get_clan_player(token, clan_player_id)
        print("Player : ", player['data']['attributes']['login'])
        global_rating = apireq.get_rating_player(token, "global", player['data']['id'])
        print("{} Global Rating is : {}".format(player['data']['attributes']['login'], int(global_rating['data']['attributes']['rating'])))
        ladder1v1_rating = apireq.get_rating_player(token, "ladder", player['data']['id'])
        print("{} Ladder Rating is : {}".format(player['data']['attributes']['login'], int(ladder1v1_rating['data']['attributes']['rating'])))
else:
    print("Any error occured getting token")



print('done')
