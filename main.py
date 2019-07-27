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
influx_client = influxclient(influx_host, influx_port, influx_org, influx_token, influx_bucket)
token = apireq.get_token(username, password)

ratings_list = apireq.generate_rating_list(host, token, clan_id)        
if ratings_list != 'error':  
    for rating in ratings_list:
        influx_client.write(rating)
else:
    logger.warn('Ratings List has error value : {}' .format(ratings_list))

print('done')
