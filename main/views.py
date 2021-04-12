from django.shortcuts import render,redirect
from .models import Tournament,Team,Match,Server
from django.views.generic import DetailView , ListView, CreateView, UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from login_signup.models import NewUser
from django.shortcuts import get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
import datetime
from django.db.models import Q
from django import forms,template
from .aws import CreateServers,StopAserver
import random
from django.urls import reverse
from django.contrib import messages
from .aws import Csstatus,CScommand

# Create your views here.




def register(request,pk):
    if request.method == 'POST':
        team = request.POST.get('team')
        tournament = Tournament.objects.get(id = request.POST.get(id = pk))
        tournament.teams.add(team)
        return redirect(tournament)
    else:
        d = datetime.datetime.strptime(str(datetime.date.today()),'%Y-%m-%d')
        d = d.date()
        args = {'tournaments': Tournament.objects.filter(Q(registration_starts__lte =d) & Q(registration_ends__gte = d )),
                'teams':request.user.team_set.all()}
        return render(request,'register.html',args)



class tournamentCreate(LoginRequiredMixin,CreateView):
    model = Tournament
    template_name = 'tournament_reg.html'

    fields = ['name' , 'game' , 'description' ,
            'sponsored_by', 'registration_starts',
             'registration_ends','tournament_starts', 'tournament_ends' ,
             'banner', 'logo' , 'prizepool' ,'sponsored_by' ,'contact_no','contact_email' ]
  
  
    def form_valid(self,form):
        form.instance.organizer = self.request.user
        
        return super().form_valid(form)



    def get_form(self, form_class=None):
        
        if form_class is None:
            form_class = self.get_form_class()
        
       

        form = super(tournamentCreate, self).get_form(form_class)
      
        form.fields['name'].widget = forms.TextInput(attrs={'placeholder': 'Name'})
        form.fields['game'].widget = forms.TextInput(attrs={'placeholder': 'CSGO'})
        form.fields['registration_starts'].widget = forms.TextInput(attrs={'placeholder': 'DD/MM/YYYY'})
        form.fields['registration_ends'].widget = forms.TextInput(attrs={'placeholder': 'DD/MM/YYYY'})
        form.fields['tournament_starts'].widget = forms.TextInput(attrs={'placeholder': 'DD/MM/YYYY'})
        form.fields['tournament_ends'].widget = forms.TextInput(attrs={'placeholder': 'DD/MM/YYYY'})
        form.fields['prizepool'].widget = forms.TextInput(attrs={'placeholder': '₹'})
        form.fields['sponsored_by'].widget = forms.TextInput(attrs={'placeholder': 'Leave blank if none'})
        return form


class tournamentUpdate(LoginRequiredMixin,UpdateView):
    model = Tournament
    template_name = 'tournament_form.html'

    fields = ['name' , 'game' , 'description' ,
            'sponsored_by', 'registration_starts',
             'registration_ends','tournament_starts', 'tournament_ends' ,
             'banner', 'logo' , 'prizepool' ,'sponsored_by','contact_no','contact_email' ]
             
    def form_valid(self,form):
        form.instance.organizer = self.request.user
        
        
        return super().form_valid(form)
   


    def get_form(self, form_class=None):
        
        if form_class is None:
            form_class = self.get_form_class()
       

        form = super(tournamentUpdate, self).get_form(form_class)
    
        form.fields['name'].widget = forms.TextInput(attrs={'placeholder': 'Name'})
        form.fields['game'].widget = forms.TextInput(attrs={'placeholder': 'CSGO'})
        form.fields['registration_starts'].widget = forms.TextInput(attrs={'placeholder': 'DD/MM/YYYY'})
        form.fields['registration_ends'].widget = forms.TextInput(attrs={'placeholder': 'DD/MM/YYYY'})
        form.fields['tournament_starts'].widget = forms.TextInput(attrs={'placeholder': 'DD/MM/YYYY'})
        form.fields['tournament_ends'].widget = forms.TextInput(attrs={'placeholder': 'DD/MM/YYYY'})
        form.fields['prizepool'].widget = forms.TextInput(attrs={'placeholder': '₹'})
        form.fields['sponsored_by'].widget = forms.TextInput(attrs={'placeholder': 'Leave blank if none'})
        return form
        


class tournamentDetails(DetailView):
    model = Tournament
    template_name = 'tournament.html'
    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)

        # status
        d = datetime.datetime.strptime(str(datetime.date.today()),'%Y-%m-%d')
        d = d.date()
        
      
        if d < self.get_object().registration_starts:
            context["status"] = "Upcoming"
         
        
        elif self.get_object().registration_starts <= d and self.get_object().registration_ends >= d:
            context["status"] = "Registration started"

        elif d > self.get_object().registration_ends:
            context["status"] = "Registration ended"
           
        elif self.get_object().tournament_starts <= d and self.get_object().tournament_ends >= d:
            context["status"] = "Ongoing"
            
        elif self.get_object().tournament_ends <= d:
            context["status"] = "Finished"
        
        
        ok = self.get_object()
        context["title"] = ok
        matches = list(ok.match_set.order_by('status'))
       
        matches.reverse()
        context["matches"] = matches
        if ok.winner:
            context["status"] = "Finished"
        if self.request.user.is_authenticated:
            if len(Tournament.objects.filter(organizer=self.request.user.id)) > 0:
                context['Hosted'] = True
            else:
                context['Hosted'] = False
            temp = Tournament.objects.filter(organizer = self.request.user)
            for i in temp:
                context["tourna_id"] = i.id
        
        flag = True
        for match in context["matches"]:
            print(match.status)
            if match.status == "Pending":
                flag = False
                print(flag)
                break 
                
        context["flag"] = flag
        servers = ok.servers.filter(is_assigned = False)
        context['servers'] = servers
        return context


    







class Home(ListView):
    queryset = Tournament.objects.filter(is_feat= True)
    template_name = 'index.html'
    context_object_name = 'tournaments'



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            if len(Tournament.objects.filter(organizer=self.request.user.id)) > 0:
                context['Hosted'] = True
            else:
                context['Hosted'] = False
        
            temp = Tournament.objects.filter(organizer = self.request.user)
            if temp:
                for i in temp:
                    context["tourna_id"] = i.id
        context['title'] = 'Home'


        return context


class Tournaments(ListView):
    queryset = Tournament.objects.all()

    template_name= 'tournaments.html'

    def get_context_data(self, **kwargs):
        
       
        context = super().get_context_data(**kwargs)
        context['title'] = 'Tournaments'
        if self.request.user.is_authenticated:
            if len(Tournament.objects.filter(organizer=self.request.user.id)) > 0:
                context['Hosted'] = True
            else:
                context['Hosted'] = False
            
            temp = Tournament.objects.filter(organizer = self.request.user)
            for i in temp:
                context["tourna_id"] = i.id


        d = datetime.datetime.strptime(str(datetime.date.today()),'%Y-%m-%d')
        d = d.date()
        register = []
        tournament = []
        future = []
        print(self.queryset)
        for query in self.queryset:
            if d < query.registration_starts:
                future.append(query)
            elif query.registration_starts <= d and query.registration_ends >= d:
                register.append(query)
            elif query.tournament_starts <= d and query.tournament_ends >= d:
                tournament.append(query)
        
        

        context["registers"] = register
        context["current"] = tournament
        context["future"] = future
        return context






class teamDetails(DetailView):
    model = Team
    template_name = 'team.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.temp = self.get_object()
        context["title"] = self.temp
        if self.request.user.is_authenticated:
            if len(Tournament.objects.filter(organizer=self.request.user.id)) > 0:
                context['Hosted'] = True
            else:
                context['Hosted'] = False
  
        
        print(Match.objects.filter(Q(team_1 = self.temp)| Q(team_2 = self.temp)))
        context["matches"] = Match.objects.filter(Q(team_1 = self.temp)| Q(team_2 = self.temp))
       
        return context


            
class matchCreate(LoginRequiredMixin,CreateView):
    model = Match
    template_name = 'match_form.html'


    fields = [ 'status', 'start_time', 'end_time','tournament']


    

    def form_valid(self,form,**kwargs):
   
        form.instance.team_1 = Team.objects.get(id = self.request.POST.get('team_1'))
        form.instance.team_2 = Team.objects.get(id = self.request.POST.get('team_2'))
        form.instance.server = Server.objects.get(id = self.request.POST.get('server'))
        form.instance.server.is_assigned = True
        return super().form_valid(form)     


    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        form = super(matchCreate, self).get_form(None)
  
        tournament = Tournament.objects.get(id = self.kwargs["id"])
        context['teams'] = tournament.teams.all()
        context['servers'] = tournament.servers.filter(is_assigned= False)
        context['form']= form
        return context


    

    
   
   
   

 

class matchUpdate(LoginRequiredMixin,UpdateView):
    model = Match
    template_name = 'match_form.html'


    fields = [ 'status', 'start_time', 'end_time','tournament']

  

    def form_valid(self,form,**kwargs):
   
        form.instance.team_1 = Team.objects.get(id = self.request.POST.get('team_1'))
        form.instance.team_2 = Team.objects.get(id = self.request.POST.get('team_2'))
        form.instance.server = Server.objects.get(id = self.request.POST.get('server'))
        form.instance.server.is_assigned = True
        return super().form_valid(form)     


    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        form = super(matchUpdate, self).get_form(None)
  
        tournament = Tournament.objects.get(id = self.kwargs["id"])
        
        context['teams'] = tournament.teams.all()
        context['servers'] = tournament.servers.filter(is_assigned= False)
        context['form']= form
        context['update'] = True
        context['idd'] = self.kwargs["id"]
        return context


class matchDelete(LoginRequiredMixin,DeleteView):
    model = Match
    template_name = 'match_confirm_delete.html'
    
    def delete(self, request, *args, **kwargs):
        response = super(matchDelete, self).delete(request, *args, **kwargs)
        match = self.get_object()
        match.server.is_assigned = False

        return response


    def get_success_url(self):
        return reverse('tournament', kwargs= {'pk':self.kwargs["id"]})

    success_url = 'home'
    


class userDetails(DetailView):
    model = NewUser
    template_name = 'user.html'

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.temp = self.get_object()
        context["title"] = self.temp
        if self.request.user.is_authenticated:
            if len(Tournament.objects.filter(organizer=self.request.user.id)) > 0:
                context['Hosted'] = True
            else:
                context['Hosted'] = False
        
            temp = Tournament.objects.filter(organizer = self.request.user)
            if temp:
                for i in temp:
                    context["tourna_id"] = i.id

    
        teams = self.temp.team_set.all()
        context['teams'] = teams
        
        matches = []
        for team in teams:
            for match in Match.objects.filter(Q(team_1 = team)| Q(team_2 = team)):
            
                if match not in matches:
                    matches.append(match)
        context["matches"] = matches
        return context


class teamCreate(CreateView,LoginRequiredMixin):
    model = Team
    template_name = "team_reg.html"
    fields = ["name","tag","logo",'player1','player2','player3','player4','player5','team_description']

    def form_valid(self,form):
        team = form.save(commit=False)
        team.save()
    
        team.players.add(self.request.POST.get("player_1"))
        team.players.add(self.request.POST.get("player_2"))
        team.players.add(self.request.POST.get("player_3"))
        team.players.add(self.request.POST.get("player_4"))
        team.players.add(self.request.POST.get("player_5"))

        team.save()
        form.save_m2m()
        
        return redirect(team)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["title"] = "New team"
        if self.request.user.is_authenticated:
            if len(Tournament.objects.filter(organizer=self.request.user.id)) > 0:
                context['Hosted'] = True
            else:
                context['Hosted'] = False
        
            temp = Tournament.objects.filter(organizer = self.request.user)
            if temp:
                for i in temp:
                    context["tourna_id"] = i.id

        context["players"] = NewUser.objects.all()
        return context


def random_matches(temp,teams,stage):
    teams = list(teams)
    random.shuffle(teams)

    print(teams)
    for i in range(0,len(teams),2):
        try:
            team_1 = teams[i+1]
            team_2 = teams[i]
            match = Match(team_1=team_1,team_2 = team_2,stage= stage)
            
            match.save()
            match.tournament.add(temp)
        
        except IndexError:
            team_1 = None
            team_2 = teams[i]
            match = Match(team_1=team_2,winner=team_1,stage= stage)
            
            match.save()
            match.tournament.add(temp)
            

    return redirect(temp)


def ok(request,pk):
    tournament = Tournament.objects.get(id = pk)
    if len(tournament.teams_left.all()) == 0 :
        i = 1
        stage = f'Preliminary round'
        for team in touranment.teams.all():
            tournament.teams_left.add(team)
        random_matches(tournament,tournament.teams_left.all(),stage)
    elif len(tournament.teams_left.all()) > 4 and len(tournament.teams_left.all()) <=16:
        stage = f'Quarter final'
    
        for match in tournament.match_set.all():
            
            random_matches(tournament,tournament.teams_left.all(),stage)


def test(request,pk):
    tournament = Tournament.objects.get(id = pk)   
    print(list(map(str,tournament.teams.all())))
    print('wasd1' in list(map(str,tournament.teams.all())))
    update_winners(pk)
    return redirect(tournament)


def temp(request,pk):
    tournament = Tournament.objects.get(id = pk)
    tournament.is_feat = True
    tournament.save()
    return redirect(tournament)
    
    

class serverDetails(DeleteView,LoginRequiredMixin):
    model = Server
    template_name = 'server.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
    
        context["state"] = obj.state()
        if context["state"] == 'running':
            obj.SetIp()
            print(obj.ip)
            context["csstatus"] = obj.Csstatus()

        self.temp = self.get_object()
        context["title"] = self.temp
        if self.request.user.is_authenticated:
            if len(Tournament.objects.filter(organizer=self.request.user.id)) > 0:
                context['Hosted'] = True
            else:
                context['Hosted'] = False
        
            temp = Tournament.objects.filter(organizer = self.request.user)
            if temp:
                for i in temp:
                    context["tourna_id"] = i.id

        

        return context

    def SetIp(id):
        obj = Server.objects.get(id = id)
        instance = ec2r.Instance(self.aws_id)
        obj.ip = instance.public_ip_address
     
        return self.ip
    
    def Start(self,pk):
        
        obj = Server.objects.get(id = pk)
        
        messages.success(self, obj.Startinstance())
        obj.SetIp()
        return redirect(obj)


    def Stop(self,pk):
        obj = Server.objects.get(id = pk)
        obj.SetIp()
        messages.success(self, obj.Stopinstance())
        return redirect(obj)

    
    def LaunchCS(self,pk):
        obj = Server.objects.get(id = pk)
        obj.SetIp()
        messages.success(self, obj.LaunchCS())
        return redirect(obj)

    
    def StopCS(self,pk):
        obj = Server.objects.get(id = pk)
        obj.SetIp()
        messages.success(self, obj.StopCS())
        return redirect(obj)


    def CommandCS(self,pk):
        obj = Server.objects.get(id = pk)
        command = self.POST.get('command')
        messages.success(self, CScommand(obj.ip,command))
        return redirect(obj)
   

class searchTournament(ListView):
    
    template_name = 'search.html'
    def get_queryset(self):
        self.inpt = self.request.GET.get("search")


        return Tournament.objects.filter(name= self.inpt)

    def get_context_data(self,**kwargs):
        
        context = super().get_context_data(**kwargs)
        
        self.inpt = self.request.GET.get("search")

        context["title"] = f'search: {self.inpt}'
  
        if self.request.user.is_authenticated:
            if len(Tournament.objects.filter(organizer=self.request.user.id)) > 0:
                context['Hosted'] = True
            else:
                context['Hosted'] = False
        
            temp = Tournament.objects.filter(organizer = self.request.user)
            if temp:
                for i in temp:
                    context["tourna_id"] = i.id

        return context


def get_servers(request,pk):
    touranment = Tournament.objects.get(id=pk)
    temp = request.POST.get('servers')
    if int(temp) > 0:
        servers = CreateServers(int(temp))
        for server in servers:
            ip,port = server["ip"].split(':')
            aws_id = server["instance"]
            ok = Server(ip = ip,port = port ,aws_id= aws_id)
            ok.save()
            StopAserver(aws_id)
           
            touranment.servers.add(ok)
    return redirect(touranment)


def FirstMatches(request,pk):
    tournament = Tournament.objects.get(id=pk)
    teams = tournament.teams.all()
    print(len(teams))
    tournament.match_set.clear()
    
    for team in teams:
        tournament.teams_left.add(team)
        tournament.save()
    left = tournament.teams_left.all()
    print(left)
    if len(left) > 16:
        random_matches(tournament,left,"Preliminary round")
    elif len(left) > 4 and len(left) <= 16:
        random_matches(tournament,left,"Quarter finals")
    elif len(left) > 2 and len(left) <=4:
        random_matches(tournament,left,"Semi finals")
    elif len(left) <=2 and len(left)>0:
        random_matches(tournament,left,"Finals")


    left = tournament.teams_left.all()
    print(len(left))
    return redirect(tournament)



def set_winner(request,pk,**kwargs):
    tournament = Tournament.objects.get(id=pk)
    print(tournament)
    match = Match.objects.get(id = kwargs.get("id"))
    winner = Team.objects.get(id = request.POST.get("winner"))
    match.winner = winner
    match.status = "Done"
    server = match.server
    if server:
        server.is_assigned = False
        server.save()

    
    if match.stage == 'Finals':
        tournament.winner = winner
        servers = tournament.servers.all()
        for server in servers:
            server.terminate()
            server.delete()
        tournament.servers.clear()
        
    if winner == match.team_1:
        tournament.teams_left.remove(match.team_2)
    elif winner == match.team_2:
        tournament.teams_left.remove(match.team_1)
    tournament.save()
    match.save()
    
    print(match.winner)
    print(tournament.teams_left.all())
    return redirect(tournament)


def next_round(request,pk):
    tournament = Tournament.objects.get(id = pk)
    left = tournament.teams_left.all()
    if len(left) > 16:
        random_matches(tournament,left,"Preliminary round")
    elif len(left) > 4 and len(left) <= 16:
        random_matches(tournament,left,"Quarter finals")
    elif len(left) > 2 and len(left) <=4:
        random_matches(tournament,left,"Semi finals")
    elif len(left) <=2 and len(left)>0:
        random_matches(tournament,left,"Finals")
    return redirect(tournament)


def set_server(request,pk,**kwargs):
    tournament = Tournament.objects.get(id = pk)
    match = Match.objects.get(id = kwargs.get("id"))
 
    server = Server.objects.get(id = request.POST.get("server"))
    match.server = server
    server.is_assigned = True
    server.save()
    match.save()
    return redirect(tournament)