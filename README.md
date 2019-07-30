FAF Scoreboard!

Arguments; 

('-a', '--apiaddress', required=False, action='store', help='Remote host to connect to')
('-u', '--user', required=True, action='store', help='User name to use when connecting to host')
('-p', '--password', required=True, action='store', help='Password to use when connecting to host')
('-c', '--clanid', required=False, action='store', help='ID of the FAF Clan')
('-i', '--influxhost', required=False, action='store', help='Remote influx api endpoint')
('-x', '--influxport', required=False, action='store', help='Remote influx api endpoint port')
('-o', '--influxorg', required=False, action='store', help='Influx Org Name')
('-b', '--influxbucket', required=False, action='store', help='Influx Bucket Name')
('-t', '--influxtoken', required=True, action='store', help='Influx API Token')
('-y', '--yamlconfig', required=False, dest='config_file', type=argparse.FileType(mode='r'), help='YAML Configuration File')
