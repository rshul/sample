from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask.ext.heroku import Heroku

app = Flask(__name__)
heroku = Heroku(app)
db = SQLAlchemy(app)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost/flaskdb'

class Filestore(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(300))
	data = db.Column(db.LargeBinary)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
	file = request.files['inputFile']
	newfile = Filestore(name=file.filename, data=file.read())
	db.session.add(newfile)
	db.session.commit()
	return "saved"+file.filename+"to the database"

if __name__ == "__main__":
	app.run()