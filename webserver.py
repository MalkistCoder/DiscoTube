from flask import Flask, request
from threading import Thread
import json

app = Flask('')

@app.route('/')
def home():
  return 'Webserver, Check . Bot, Check'

@app.route('/api')
def api():
  return '''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta property="og:title" content="DiscoTube API">
    <meta property="og:description" content="Welcome to the DiscoTube API!">
    <title>DiscoTube API Home Page</title>
  </head>
  <body>
    <h1 id="title">DISCOTUBE API</h1>
    <ul id="apis">
      <li>Currency Stats: here</li>
      <li>Cog Levels: here</li>
      <li>Currency Shop: here</li>
      <li>8Ball Brain: Coming Soon!</li>
    </ul>
  </body>
</html>'''

@app.route('/api/levels')
def api_levels():
  return json.load(open('economy.json','r'))[request.args.get('memberid')]


def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
  t = Thread(target=run)
  t.start()