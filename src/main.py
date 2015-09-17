from bottle import route, run, response
from time import sleep
import configparser, thread, requests, sys, bottle, api

def init(ks):
  api.keyspace = ks
  app = bottle.app()
  return app

