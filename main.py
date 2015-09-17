from bottle import route, run, response
from time import sleep
import configparser, thread, requests, sys, bottle
from src import api 

def init(ks):
  api.keyspace = ks
  app = bottle.app()
  return app

