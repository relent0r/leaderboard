from fafclient import fafapi
from influxclient import influxclient
import logging
import argparse
import schedule
import time
import yaml
import os

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

#

def GetArgs():
   """
   Supports the command-line arguments listed below.
   """

   parser = argparse.ArgumentParser(description='Process args')
   parser.add_argument('-a', '--apiaddress', required=False, action='store', help='Remote host to connect to')
   parser.add_argument('-u', '--user', required=False, action='store', help='User name to use when connecting to host')
   parser.add_argument('-p', '--password', required=False, action='store', help='Password to use when connecting to host')
   parser.add_argument('-c', '--clanid', required=False, action='store', help='ID of the FAF Clan')
   parser.add_argument('-i', '--influxhost', required=False, action='store', help='Remote influx api endpoint')
   parser.add_argument('-x', '--influxport', required=False, action='store', help='Remote influx api endpoint port')
   parser.add_argument('-o', '--influxorg', required=False, action='store', help='Influx Org Name')
   parser.add_argument('-b', '--influxbucket', required=False, action='store', help='Influx Bucket Name')
   parser.add_argument('-t', '--influxtoken', required=False, action='store', help='Influx API Token')
   parser.add_argument('-y', '--yamlconfig', required=False, dest='config_file', type=argparse.FileType(mode='r'), help='YAML Configuration File')
   args = parser.parse_args()
   return args

args = GetArgs()

def config(config_file):
    """
    Gets config arguments from a yaml config file
    """
    data = yaml.load(config_file, Loader=yaml.FullLoader)
    delattr(args, 'config_file')
    arg_dict = args.__dict__
    for key, value in data.items():
        if isinstance(value, list):
            for v in value:
                 arg_dict[key].append(v)
        else:
            arg_dict[key] = value
    return args


# check if command line parameters are supplied for config options, if not check for config file and assign variables
if args.apiaddress and args.clanid and args.influxhost \
    and args.influxport and args.influxorg and args.influxbucket:
    logger.debug('Using command line parameters for config')
    host = "https://" + args.apiaddress + "/"
    clan_id = args.clanid
    influx_host = args.influxhost
    influx_port = args.influxport
    influx_org = args.influxorg
    influx_bucket = args.influxbucket
elif args.config_file:
    logger.debug('Using config file for config')
    yaml_args = config(args.config_file)
    host = "https://" + yaml_args.apiaddress + "/"
    clan_id = yaml_args.clanid
    influx_host = yaml_args.influxhost
    influx_port = yaml_args.influxport
    influx_org = yaml_args.influxorg
    influx_bucket = yaml_args.influxbucket
else:    
    logger.warn('Missing Parameters, please use either command line parameters or a yaml config file')
    exit()

# check if command line parameters are supplied for credentials, if not check environment variables and assign variables
if args.user and args.password and args.influxtoken:
    logger.debug('Using command line parameters for credentials')
    username = args.user
    password = args.password
    influx_token = args.influxtoken
elif os.environ.get('FAFUSER') and os.environ.get('FAFPASS') and os.environ.get('INFLUXTOKEN'):
    logger.debug('Using environment variables for credentials')
    username = os.environ.get('FAFUSER')
    password = os.environ.get('FAFPASS')
    influx_token = os.environ.get('INFLUXTOKEN')
else:
    logger.warn('No credentials available, please use command line parameters or environment variables')
    exit()


# Query faf api for clan member ratings and send to influxdb
def job():
    logger.debug(host)
    apireq = fafapi(host)
    influx_client = influxclient(influx_host, influx_port, influx_org, influx_token, influx_bucket)
    token = apireq.get_token(username, password)

    ratings_list = apireq.generate_rating_list(token, clan_id)        
    if ratings_list != 'error':  
        for rating in ratings_list:
            influx_client.write(rating)
    else:
        logger.warn('Ratings List has error value : {}' .format(ratings_list))

schedule.every(1).minutes.do(job)
while True:
    schedule.run_pending()
    time.sleep(30)
print('done')
