from django.contrib import admin

# Register your models here.
from .models import Tournament,Team,Match,Server

admin.site.register(Tournament)
admin.site.register(Team)
admin.site.register(Match)
admin.site.register(Server)