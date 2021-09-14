import School
import os
from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app# Initialize Flask App
app = Flask(__name__)# Initialize Firestore DB
cred = credentials.Certificate('key.json')
default_app = initialize_app(cred)
db = firestore.client()
todo_ref = db.collection('todos')

def idGenerator():

    doc_ref = db.collection(u'school').document()
    return doc_ref.id


@app.route('/')
def hello_world():
    return 'A casa platita'




@app.route('/add', methods=['POST'])
def create():

    my_data = {"name": "IPM"}
    doc_ref = db.collection(u'schools').document()
    doc_ref.set(my_data)

    try:
        id = request.json['id']
        todo_ref.document(id).set(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"

@app.route('/getSchool', methods=['GET', 'POST'])
def getSchool():

    #doc_ref = db.collection(u'school').document(u'lhrtFyMTfLFawLGOtp3J')

    #doc = doc_ref.get()
    #schoolR = School.from_dict()   #hay que hacer una funcion para poder traducir lo que llega de de doc a School
    doc_ref = db.collection(u'schools').document(u'lhrtFyMTfLFawLGOtp3J')

    doc = doc_ref.get()
    print(doc.to_dict())
    print(doc)

    try:
        id = request.json['id']
        todo_ref.document(id).set(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"

port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=port)
