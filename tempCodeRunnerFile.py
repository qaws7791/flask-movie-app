@app.route('/movie/<int:id>')
def movie(id):
    return render_template('comment.html',id=id)