from django.shortcuts import render
from django.http import HttpResponse
from . import models

def index(request):
    message = "Salut tout le monde !"
    return HttpResponse(message)

def listings(request):
    albums = ["<li>{}</li>".format(album['name']) for album in models.ALBUMS]
    message = """<ul>{}</ul>""".format("\n".join(albums))
    return HttpResponse(message)

def detail(request, album_id):
    id = int(album_id)
    album= models.ALBUMS[id]
    artists = " ".join([artist['name'] for artist in album['artists']])
    message = "Le blaz de l'artiste est {} il est cré par {}".format(album['name'], artists)
    return HttpResponse(message)

def search(request):
    pass