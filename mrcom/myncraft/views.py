from django.shortcuts import render
import os
from mcrcon import MCRcon
# Create your views here.
def index(request):
    return render(request, 'index.html', {'data':'damato'})
def myncraft(request, myncraft):
    with MCRcon(os.environ['myncraft'], os.environ['cheesesteakjimmys']) as mcr:
        resp = mcr.command("/list")
        return  render (request, 'index.html', { 'data':resp})




