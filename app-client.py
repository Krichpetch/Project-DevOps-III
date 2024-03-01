from flask import Flask, request, jsonify
import requests
import json
import os

app = Flask(__name__)

#GET REST APIs

@app.route('/getuser/<id_memo>', methods = ['GET'])
def get_user(id_memo):
    api_url = "http://127.0.0.1:5000/getuser/v1" + id_memo
    response = requests.get(api_url)
    
    return jsonify(response.json())

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port=5005, debug=True)