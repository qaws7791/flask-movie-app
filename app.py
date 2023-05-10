import os
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, jsonify, json,url_for
from pymongo import MongoClient

# flask
app = Flask(__name__)

# mongodb
load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")
print(MONGODB_URI)
client = MongoClient(MONGODB_URI)
print(client)
db = client['flask-movie-app']


# movie genre list
with open('./genre.json','rt',encoding='UTF8') as file:
    jsonData = json.load(file)['genres']

genreList = {}
for genre in jsonData:
    genreList[genre['id']] = genre['name']
print(genreList)

##### flask app #####

## HOME
@app.route('/')
def home():
    return render_template('index.html')

## create comment
@app.route("/api/comment", methods=["POST"])
def create_comment():
    name = request.form['name']
    comment = request.form['comment']
    star = request.form['star']
    movie_id = request.form['movie_id']
    doc = {
        'name': name,
        'comment': comment,
        'star': star,
        'movie_id' : movie_id
    }
    result =  db['comment'].insert_one(doc)
    print(result)
    return jsonify({'msg': '저장 완료!'})

## get comment list
@app.route("/api/comment/<int:id>", methods=["GET"])
def get_comments(id):
    all_comments = list(db.comment.find({'movie_id':str(id)}, {'_id': False}))

    return jsonify({'result': all_comments})
    


@app.route('/movie/<int:id>')
def movie(id):
    return render_template('comment.html',id=id)
    
@app.route('/genre/<int:id>')
def genre(id):
    if id in genreList:
        return render_template('genre.html',id=id)
    else:
        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run('0.0.0.0', port=5050, debug=True)