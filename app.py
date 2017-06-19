from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask.ext.heroku import Heroku
import hashlib



app = Flask(__name__)
app.secret_key = 'abcdefgjklmnopqrstuvwxyz1234567'
heroku = Heroku(app)
db = SQLAlchemy(app)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost/flaskdb'

class Filestore(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(300))
	data = db.Column(db.LargeBinary)

@app.route('/', methods=['GET','POST'])
def index():

	if request.method == 'POST':
		sha256 = hashlib.sha256()
		data = None
		file = request.files['inputFile']
		data = file.read()
		sha256.update(data)
		hsh = sha256.hexdigest()
		newfile = Filestore(name=hsh, data=data)
		db.session.add(newfile)
		db.session.commit()
		num = Filestore.query.filter_by(name=hsh).count()
		flash("This file was uploaded " +str(num)+" times")
		return redirect(url_for('index'))
	try:
		rows = Filestore.query.all()
		
	except:
		rows = None
	

	return render_template('index.html', rows=rows)
@app.route('/delrows')
def delrows():
	try:
		Filestore.query.delete()
		db.session.commit()
	except:
		print("error")
	return redirect(url_for('index'))

if __name__ == "__main__":
	app.run()