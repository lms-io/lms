import random, os, uuid, bcrypt, sys, inspect, setup

from cassandra.cluster import Cluster
from webtest import TestApp


def test_version():
  app = setup.app() 
  res = app.get('/version') 
  print res.json
  assert res.json.get('version') == "0.1.0"


