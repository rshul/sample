from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)
class Filestore(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(300))
	data = db.Column(db.LargeBinary)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost/flaskdb'
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
	app.run(debug=True)