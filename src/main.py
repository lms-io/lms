from bottle import route, run, response
from time import sleep
import configparser, thread, requests, sys, bottle, api

def init(ks,rdis):
  api.keyspace = ks
  api.rdis = rdis
  app = bottle.app()
  return app

