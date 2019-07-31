FAF Scoreboard!

Queries FAForever public api for clan member ratings and sends them to an influxdb. Runs on a configurable schedule of X minutes.

This app can take either commandline arguments or a mixture of yaml file for configuration variables and environment variables for credentials, or a mix of the two.

Arguments

--apiaddress

FQDN of the faf public api

--user

FAF Username

--password

FAF Password

--clanid

The clan id as known to the FAF api. Clan ID is the identifier for a FAF clan in the FAF Database.

--influxhost

The FQDN or IP of an influx db.

--influxport

Port number of the influx api.

--influxorg

Influx org name.

--influxbucket

Influx bucket name.

--influxtoken

API token for the influx api.

--yamlconfig

yaml configuration file.


Example Config YAML

apiaddress: "api.faforever.com"

clanid: "0000"

influxhost: "192.168.1.20"

influxport: "9999"

influxorg: "skynet"

influxbucket: "fafdump"


Required Environment Variable Names

FAFUSER

FAF Username

FAFPASS

FAF Password

INFLUXTOKEN

API token for the influx api.

TODO : Add schedule as argument.
