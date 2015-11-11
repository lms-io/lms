from bottle import route, run, response
from time import sleep
import configparser, thread, requests, sys, bottle, appcontext, routes

def init(ks,rdis):
  appcontext.keyspace = ks
  appcontext.rdis = rdis
  app = bottle.app()
  return app

