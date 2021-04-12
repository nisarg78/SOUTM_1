# from aws import CreateServers,StopAserver,Start_cs,Command_to_server
import boto3
from bracket import Tournament,TournamentGUI
from login_signup.models import NewUser

players = NewUser.objects.all()
tournament = Tournament(list(players))
tournament.generate_bracket(bracket_class='notsingle',randomize=True)