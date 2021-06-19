from flask import Flask, request
from threading import Thread
import json

app = Flask('')

@app.route('/')
def home():
    return 'Bot is on. If you are looking for the API, go <a href=\'/api\'>here</a>'

@app.route('/api')
def api():
    with open('website/'+'api.html','r') as f:
        website = f.read()
    return website

@app.route('/api/economy')
def api_economy():
    with open('economy.json','r') as f:
        banks = json.load(f)
    memberid = request.args.get('memberid', default = 1, type = int)
    return banks['banks'][str(memberid)]

@app.route('/api/discoin')
@app.route('/api/dc')
def api_dc():
    with open('economy-dc.json','r') as f:
        banks = json.load(f)
    return banks

def run():
    app.run(host='0.0.0.0',port=80)

def keep_alive():
    t = Thread(target=run)
    t.start()