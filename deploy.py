from keras.models import model_from_json
from keras.optimizers import SGD

from flask import Flask, render_template, request, jsonify
from threading import Thread
from DetectEmotion import func, stop_thread, start_thread
from graph import grph

app = Flask(__name__)


'''model = model_from_json(open('./models/Face_model_architecture.json').read())
    #model.load_weights('_model_weights.h5')
model.load_weights('./models/Face_model_weights.h5')
sgd = SGD(lr=0.1, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd)
'''
thread1=Thread(target=func,args=())

@app.route('/',methods=['POST','GET'])
def main():
    start_thread()
    global thread1
    if thread1.isAlive()==False:
        thread1.start()
    return render_template("index.html")

@app.route('/background',methods=['POST','GET'])
def a():
    if request.method == 'GET':
        print(val)
        data = request.args.get('data')
        print (data)
        return jsonify({})

@app.route('/plan',methods=['GET','POST'])
def b():
    stop_thread()
    if request.method=='GET':
        data=request.args.get('data')
        print(data)
        res=grph([0,1,2,3,4])
        return render_template("dir.html",fixedpts=res['fixedpts'],waypts=res['waypts'])
    else:
        data=request.get_json()
        print(data['val'])
        res=grph([0,1,2,3,4])
        return render_template("dir.html",fixedpts=res['fixedpts'],waypts=res['waypts'])


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)


    if(req.get("result").get("action")=="ask_time"):

        param=req.get("result").get("parameters")
        #budget
        print(param['unit-currency']['amount'])
    elif(req.get("result").get("action")=="thank"):
        param=req.get("result").get("parameters")
        #time
        print(param['duration']['amount'])
    res = {}

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r



if __name__ == '__main__':
    app.run(debug=False)