from flask import Flask, render_template
from bson.objectid import ObjectId
import pymongo
import os
from os import path
if path.exists("env.py"):
    import env


app = Flask(__name__)


# SET UP - WHAT CLUSTER/SEVER - WHAT DATABASE - WHAT COLLECTION
MONGO_URI = os.environ.get("MONGO_URI")
DBS_NAME = "first_database"
COLLECTION_NAME = "actors"


# CONNECTING TO IT
def mongo_connect(url):
    try:
        conn = pymongo.MongoClient(url)
        print("Mongo is connected!")
        return conn
    except pymongo.errors.ConnectionFailure as e:
        print("Could not connect to MongoDB: %s") % e


# REPRESENTS THE DATABASE
conn = mongo_connect(MONGO_URI)
# REPRESENTS THE COLLECTION
coll = conn[DBS_NAME][COLLECTION_NAME]


# READ
@app.route("/")
def home():
    documents = coll.find()
    return render_template('hello.html', documents=documents)


# CREATE
@app.route('/create')
def create():

    document = {"name": "Kevin",
                "nb_of_movies": "40"}

    coll.insert_one(document)

    return "A record has been created"


# UPDATE
@app.route('/update')
def update():

    query = {'name': 'Russel'}

    actor_to_update = coll.find_one(query)

    id_ = actor_to_update["_id"]
    what_doc = {'_id': ObjectId(id_)}

    doc_content = {'name': "Russel",
                   'nb_of_movies': "456"}

    coll.update(what_doc, doc_content)

    return "Record updated"


# DELETE
@app.route('/delete')
def delete():
    query = {'name': 'Kevin'}

    actor_to_delete = coll.find_one(query)

    id_ = actor_to_delete["_id"]

    coll.remove({'_id': ObjectId(id_)})

    return "A record has been deleted"


if __name__ == '__main__':
    app.run(host='0.0.0.0',
            port=5000,
            debug=True)
