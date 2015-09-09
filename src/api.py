from bottle import route,request 
import configparser, thread, requests, sys, jsonpickle, random, os, zipfile, shutil 

config = configparser.ConfigParser()
config.read('config.ini')

@route('/sys/')
def sys_hello():
    return "0.1" 
