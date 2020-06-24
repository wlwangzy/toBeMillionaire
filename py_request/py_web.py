# -*- coding: utf-8 -*- 
from flask import Flask, jsonify, request
from flask_cors import *
from py_request import *
from INCLUDE import *
import json

app = Flask(__name__)
CORS(app, supports_credentials=True)

def encodeJson(status, data):
    reDic = {}
    reDic["status"] = status
    reDic["data"] = data

    return jsonify(reDic)

@app.route('/getUrlData', methods=['GET', 'POST'])
def getUrlData():
    sUrl = request.args['sUrl']
    status, data = toGetRquest(sUrl)

    return encodeJson(status, data)

@app.route('/downLoadExcel', methods=['GET', 'POST'])
def downLoadExcel():
    #request.json.get("sData")
    status = True
    #print sData
    #name=request.form.get('sData')
    sData = request.args['sData']
    outPutFile = request.args['outPutFile']
    praseData = json.loads(sData)
    #app.logger.debug(outPutFile)
    basedir = os.path.abspath(os.path.dirname(__file__))
    updateExcelData(basedir + "/web/output/" + outPutFile, praseData)

    return encodeJson(status, "/output/" + outPutFile)

def createServer():
    app.run(host='0.0.0.0', port=8080, debug=True)

if __name__ == "__main__":
    createServer()