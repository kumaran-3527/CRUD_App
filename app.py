
from flask import Flask, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    thing = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
    	return '<Task %r>' % self.id

@app.route('/home' , methods = ['POST' , 'GET'])
def index():
    
    if request.method == 'POST':
        thing_name = request.form['thing']
        thing_location = request.form['location']
        new_thing = todo(thing=thing_name, location=thing_location)
        
        try:

            db.session.add(new_thing)
            db.session.commit()
            return redirect('/')
        
        except:

            return ' There was a problem adding the information'
    elif request.method == 'GET':

        tasks = todo.query.order_by(todo.date_created).all()
        return tasks

@app.route('/delete/<int:id>')
def delete(id):
	task_to_delete = todo.query.get_or_404(id)

	try:
		db.session.delete(task_to_delete)
		db.session.commit()
		return redirect('/')
	except:
		return 'There was a problem deleting that task'
    

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
	task = todo.query.get_or_404(id)

	if request.method == 'POST':
		task.thing = request.form['thing']
		task.location = request.form['location']
		try:
			db.session.commit()
			return redirect('/')
		except:
			return 'There was a problem updating your task'
	else:
		return task


if __name__ == "__main__":
	app.run()





