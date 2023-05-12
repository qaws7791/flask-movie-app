import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, jsonify, json,url_for
from pymongo import MongoClient

# flask
app = Flask(__name__)

# mongodb
load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")
client = MongoClient(MONGODB_URI)
print(client)
db = client['flask-movie-app']


# movie genre list
current_path = Path(__file__)
file_name = "genre.json"
file_path = current_path.with_name(file_name)
with open(file_path,'rt',encoding='UTF8') as file:
    jsonData = json.load(file)['genres']

genreList = {}
for genre in jsonData:
    genreList[genre['id']] = genre['name']

##### flask app #####

## HOME page
@app.route('/')
def home():
    return render_template('index.html')

## Movie page
@app.route('/movie/<int:id>')
def movie(id):
    return render_template('comment.html',id=id)
    
## Genre page
@app.route('/genre/<int:id>')
def genre(id):
    if id in genreList:
        return render_template('genre.html',id=id)
    else:
        return redirect(url_for('home'))

##### api #####
## create comment
@app.route("/api/comment", methods=["POST"])
def create_comment():
    name = request.form['name']
    comment = request.form['comment']
    star = request.form['star']
    movie_id = request.form['movie_id']
    movie_title = request.form['movie_title']
    movie_poster = request.form['movie_poster']
    movie_genres = []
    index = 0
    while True:
        genre_id = request.form.get(f'genres[{index}][id]')
        genre_name = request.form.get(f'genres[{index}][name]')
        if genre_id is None or genre_name is None:
            break
        movie_genres.append({'id': genre_id, 'name': genre_name})
        index += 1
    doc = {
        'name': name,
        'comment': comment,
        'star': star,
        'movie_id' : movie_id,
        'movie_title': movie_title,
        'movie_poster': movie_poster,
        'movie_genres' : movie_genres
    }
    result =  db['comment'].insert_one(doc)
    return jsonify({'msg': '저장 완료!'})

## get comment list
@app.route("/api/comment", methods=["GET"])
def get_comments():
    movieId = request.args.get('movieId')
    all_comments = list(db.comment.find({'movie_id':str(movieId)}, {'_id': False}).sort("_id",-1))
    return jsonify({'result': all_comments})

## get recently comment list
@app.route("/api/recent/<int:limit>", methods=["GET"])
def get_recent_comments(limit):
    all_comments = list(db.comment.find({}, {'_id': False}).sort("_id",-1).limit(limit))
    return jsonify({'result': all_comments})

## get genre comment list
@app.route("/api/genre/<int:genre>", methods=["GET"])
def get_genre_comments(genre):
    if genre in genreList:
        all_comments = list(db.comment.find({'movie_genres.id':str(genre)}, {'_id': False}).sort("_id",-1).limit(10))
        return jsonify({'result': all_comments})
    else:
        return jsonify({'result': []})
    
if __name__ == '__main__':
    app.run('0.0.0.0', port=5050, debug=True)