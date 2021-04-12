from django.db import models
from login_signup import models as _
from django.contrib.postgres.fields import ArrayField
from django.urls import reverse
import boto3
from . import aws
ec2r = boto3.resource('ec2')
# Create your models here.

class Server(models.Model):
    aws_id = models.CharField(max_length=20, blank= True)
    ip = models.CharField(max_length=20, blank= False)
    port = models.IntegerField(null=False , default= 27015)
    is_assigned = models.BooleanField(default=False)
    

    def __str__(self):
        return f'{self.ip}:{self.port}'

    
    def state(self):
        return aws.ServerState(self.aws_id)


    def Startinstance(self):
        instance = aws.StartAserver(self.aws_id)
        return instance

    
    def Stopinstance(self):
        instance = aws.StopAserver(self.aws_id)
        return instance


    def LaunchCS(self):
        return aws.Start_cs(self.ip)

    
    def StopCS(self):
        return aws.Stop_cs(self.ip)

    
    def RestartCs(self):
        return aws.Restart_cs(self.ip)


    def SetIp(self):
        instance = ec2r.Instance(self.aws_id)
        self.ip = instance.public_ip_address
        self.save()
     
        return self.ip


    def Csstatus(self):
        if self.state() == 'running':
            return aws.Csstatus(self.ip)


    def get_absolute_url(self):
  
        return reverse("server", kwargs= {'pk': self.pk})


    def terminate(self):
        return aws.Terminate(self.aws_id)



class Team(models.Model):
    name = models.CharField(max_length=50,  null=False)
    tag = models.CharField(max_length=10, blank=True, null=True)
    logo = models.ImageField(upload_to="logos", blank=True, null=True)
    players = models.ManyToManyField(_.NewUser)
    team_description = models.CharField(max_length=150 , blank= True, null=True)
    player1 = models.CharField(max_length = 150, blank=True)
    player2 = models.CharField(max_length = 150, blank=True)
    player3 = models.CharField(max_length = 150, blank=True)
    player4 = models.CharField(max_length = 150, blank=True)
    player5 = models.CharField(max_length = 150, blank=True)



    def __str__(self):
        return self.name


    def get_absolute_url(self):
        print(reverse("team", kwargs= {'pk': self.pk}))
        return reverse("team", kwargs= {'pk': self.pk})


class Tournament(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    description = models.TextField(default = '')
    registration_starts = models.DateField(blank=False,null=False)
    registration_ends = models.DateField(blank=False,null=False)
    tournament_starts = models.DateField(blank=False,null=False)
    tournament_ends = models.DateField(blank=False,null=False)
    teams_left = models.ManyToManyField(Team,related_name= 'teams_left')
    teams = models.ManyToManyField(Team,related_name= 'tournament_teams')
    banner = models.ImageField(upload_to="tournament_banners")
    logo = models.ImageField(upload_to="tournament_logo",default='../static/images/logo.png')
    organizer = models.ForeignKey(_.NewUser,on_delete=models.CASCADE)
    prizepool = models.IntegerField(blank=False,null=False)
    game = models.CharField(max_length=10, blank=True, null=True)
    contact_email = models.EmailField(max_length=254)
    contact_no = models.IntegerField(blank=False,null=True)
    sponsored_by = models.CharField(max_length=50, blank=True, null=True)
    is_feat = models.BooleanField(default=False)
    servers = models.ManyToManyField(Server)
    winner = models.ForeignKey(Team, blank= True,null=True,on_delete=models.CASCADE,related_name='tournament_winner')
    


    def __str__(self):
        return self.name
    

    def get_absolute_url(self):
        print(reverse('tournament', kwargs= {'pk': self.pk}))
        return reverse('tournament', kwargs= {'pk': self.pk})




class Match(models.Model):
   

    server = models.ForeignKey(Server, on_delete= models.CASCADE, blank=True, null=True)

 
    stage = models.CharField(max_length = 50,blank=True, null=True)
    uuid = models.CharField(default='uuid4', max_length=100)
    
    team_1 = models.ForeignKey(
        Team, on_delete=models.SET_NULL, blank=True, null=True, related_name="team_1"
    )
    team_2 = models.ForeignKey(
        Team, on_delete=models.SET_NULL, blank=True, null=True, related_name="team_2"
    )
    
    winner = models.ForeignKey(
        Team, on_delete=models.SET_NULL, blank=True, null=True, related_name="winner"
    )
    status = models.CharField(max_length=50, default="Pending")
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    skip_veto = models.BooleanField(default=True)
    team_1_score = models.IntegerField(default=0)
    team_2_score = models.IntegerField(default=0)
    veto_mappool = models.CharField(max_length=500, blank=True, null=True)
    match_map = models.CharField(max_length=20, blank=True, default='Default Dust2')
    max_maps = models.IntegerField(default=1)
    tournament = models.ManyToManyField(Tournament)

    class Meta:
        verbose_name = ("Match")
        verbose_name_plural = ("Matches")

    def teams(self):
        t1 = self.team_1

        t2 = self.team_2
        return f"{t1} vs {t2}"

    
    def setwinner(self,team):
        self.winner = team
        self.status = "DONE"
        self.save()

    
    @property
    def match_config(self) -> dict:
        t1_info = self.team_1.team_information if self.team_1 else {}
        t2_info = self.team_2.team_information if self.team_2 else {}
        return {
            "match_id": self.uuid,
            "num_maps": 1,
            "maplist": [{"de_dust2": ""}],
            "skip_veto": self.skip_veto,
            "veto_first": "team1",
            "side_type": "always_knife",
            "players_per_team": 5,
            "min_players_to_ready": 1,
            "team1": t1_info,
            "team2": t2_info,
            "cvars": {
                "hostname": f"Match - {t1_info.get('name')} vs {t2_info.get('name')}"
            },
        }
    
    def get_absolute_url(self):
    
  
        return reverse('home')

