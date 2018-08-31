from django.shortcuts import render
import os
from mcrcon import MCRcon
# Create your views here.
def index(request):
    return render(request, 'index.html', {'data':'damato'})
def myncraft(request, PODSESSION):
    with MCRcon(PODSESSION, 'cheesesteakjimmys') as mcr:
        return render(request, 'index.html', {'data': mcr.command("/list")})
