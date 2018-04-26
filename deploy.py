from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
from flask import Flask, render_template, request, jsonify,make_response
from threading import Thread
from DetectEmotion import func, stop_thread, start_thread, change_active, finaldata, clean
from graph import grph, suggest
import os
import requests
event=1
app = Flask(__name__)


'''model = model_from_json(open('./models/Face_model_architecture.json').read())
    #model.load_weights('_model_weights.h5')
model.load_weights('./models/Face_model_weights.h5')
sgd = SGD(lr=0.1, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd)
'''
thread1=Thread(target=func,args=())

start=1
welcome=0

time=-1
budget=-1
def whenclickplanitinerary():
    headers = {
    'Authorization': 'Bearer ac36ea3d844d4145aa2e7d71854a5c64',
    }

    params = (
    ('v', '20170712'),
    ('e', 'custom_event'),
    ('timezone', 'Asia/Calcutta\''),
    ('lang', 'en'),
    ('sessionId', '1234567890'),
    )
    response = requests.get('https://api.dialogflow.com/v1/query', headers=headers, params=params)
    data = response.json()
    listtohtml=[]
    param=data.get("result").get("parameters")

    for i in data['result']['fulfillment']['messages']:
        listtohtml.append(i['speech'])
    num=len(listtohtml)
    return num,listtohtml


def todiagflow():
    headers = {
    'Authorization': 'Bearer ac36ea3d844d4145aa2e7d71854a5c64',
    }

    params = (
    ('v', '20170712'),
    ('e', 'custom_welcome'),
    ('timezone', 'Asia/Calcutta\''),
    ('lang', 'en'),
    ('sessionId', '1234567890'),
    )

    response = requests.get('https://api.dialogflow.com/v1/query', headers=headers, params=params)
    data = response.json()
    listtohtml=[]

    for i in data['result']['fulfillment']['messages']:
        listtohtml.append(i['speech'])
    num=len(listtohtml)
    return num,listtohtml

def respond_to_query(s):
    global time,budget
    headers = {
    'Authorization': 'Bearer ac36ea3d844d4145aa2e7d71854a5c64',
    }

    params = (
    ('v', '20170712'),
    ('query', s),
    ('lang', 'en'),
    ('sessionId', '1234567890'),
    ('timezone', 'Asia/Calcutta'),
    )

    response = requests.get('https://api.dialogflow.com/v1/query', headers=headers, params=params)
    data=response.json()

    param=data.get("result").get("parameters")

    #for getting budget
    if 'unit-currency' in param:
        budget=param['unit-currency']['amount']
        print(budget)

    #for getting time
    if 'duration' in param:
        time=param['duration']['amount']
        print(time)
    listtohtml=[]
    for i in data['result']['fulfillment']['messages']:
        listtohtml.append(i['speech'])
    num=len(listtohtml)
    return num,listtohtml


@app.route('/',methods=['POST','GET'])
def main():
    start_thread()
    global thread1
    global welcome
    num,listtohtml=todiagflow()
    print(listtohtml)
    if welcome==1:
        num=0
    else:
        welcome=1
    if thread1.isAlive()==False:
        thread1.start()
    return render_template("index.html",bot_string=listtohtml,bot_number=num)

@app.route('/background',methods=['POST','GET'])
def a():
    if request.method == 'GET':
        data = int(request.args.get('data'))
        sec_no=int(data/10)
        slide_no=data%10
        change_active(sec_no,slide_no)
        return jsonify({})

@app.route('/todo',methods=['GET','POST'])
def b():
    stop_thread()
    if request.method=='GET':
        prob=finaldata()
        #print(prob)
        res=suggest(prob)
        #res1=grph(res['sugg_cities'],time,res['pref'])
        #print(res1['daycnt'])
        return render_template("dir.html",courses=res['sugg_places'],done=0)

@app.route('/planit',methods=['GET'])
def planit():
    stop_thread()
    headers = {
    'Authorization': 'Bearer ac36ea3d844d4145aa2e7d71854a5c64',
    }

    params = (
    ('v', '20170712'),
    ('e', 'custom_event'),
    ('timezone', 'Asia/Calcutta\''),
    ('lang', 'en'),
    ('sessionId', '1234567890'),
    )
    response = requests.get('https://api.dialogflow.com/v1/query', headers=headers, params=params)
    data = response.json()
    listtohtml=[]
    param=data.get("result").get("parameters")

    for i in data['result']['fulfillment']['messages']:
        listtohtml.append(i['speech'])
    num=len(listtohtml)

    data = int(request.args.get('data'))
    sec_no=int(data/10)
    slide_no=data%10
    change_active(sec_no,slide_no)

    return jsonify({'bot_number':num,'bot_string':listtohtml})

@app.route('/stopcam',methods=['GET'])
def c():
    stop_thread()
    data = int(request.args.get('data'))
    sec_no=int(data/10)
    slide_no=data%10
    change_active(sec_no,slide_no)
    return jsonify({})

@app.route('/strtcam',methods=['GET'])
def d():
    start_thread()
    return jsonify({})

@app.route('/null',methods=['GET'])
def e():
    start_thread()
    clean()
    return jsonify({})

@app.route('/chat')
def f():
    global welcome
    num,listtohtml=todiagflow()
    print(listtohtml)
    if welcome==1:
        num=0
    else:
        welcome=1
    return render_template('yoyo.html',bot_string=listtohtml,bot_number=num)

@app.route('/sss',methods=['GET'])
def sss():
    s=request.args.get('data')
    num,listtohtml=respond_to_query(s)

    print(listtohtml)
    print(num)
    res={
        'bot_string':listtohtml,
        'bot_number':num
     }
    # res=json.dumps(res)
    return jsonify(res)



if __name__ == '__main__':
    #port = int(os.getenv('PORT', 5000))
    app.run(debug=False)
