import boto3
from aws import CreateServers,StopAserver,StartAserver,Start_cs,Command_to_server,get_rcon,CScommand
from rcon_service import execute_rcon_cmd

ip = '35.154.225.9'
import valve.source.a2s

SERVER_ADDRESS = (ip, 27015)

with valve.source.a2s.ServerQuerier(SERVER_ADDRESS) as server:
    info = server.info()
    players = server.players()

print("{player_count}/{max_players} {server_name}".format(**info))


for player in sorted(players["players"],
                     key=lambda p: p["score"], reverse=True):
    print("{score} {name}".format(**player))
