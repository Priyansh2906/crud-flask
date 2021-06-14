from flask import Flask,url_for,redirect,render_template,request,session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from time import sleep
app = Flask(__name__)
app.secret_key = "Priyansh"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Task_master(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    content = db.Column(db.String(250),nullable=False)
    date_created = db.Column(db.DateTime,default = datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/' , methods=['POST','GET'])
def index():
    if request.method == 'POST':
        task = request.form['content']
        task_model = Task_master(content=task)

        try:
            db.session.add(task_model)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an error adding your task to the database!!!"

    else:
        tasks = Task_master.query.order_by(Task_master.date_created).all()
        return render_template('index.html' ,tasks=tasks,session=session)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Task_master.query.get_or_404(id)
    
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "There was an error deleting rhat task. Please try again later!"

@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):

    task_to_update = Task_master.query.get_or_404(id)
    if request.method=='POST':
        task_to_update.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was an error updating the task. Please try again later!"
    else:
        return render_template('update.html',task=task_to_update)

@app.route('/login' , methods=["POST","GET"])
def login():
    if request.method == 'POST':
        username = request.form.to_dict()
        for i in username : 
            print(i + ":" + username[i])
        session['user'] = username
        return redirect(url_for('user'))
    else:
        if "user" in session:
            return redirect(url_for("user"))
        return render_template('login.html')

@app.route('/user')
def user():
    if "user" in session:
        var1 = session['user']
        return "<h1> User " + str(var1) +" logged in successfully!!!</h1> <br><br>  <a href='/'>Go-To Task Masker!!</a>"
        
    else:
        if "user" in session:
            return redirect(url_for('user')) #checks is the user is already logged in i.e. the data is availablw in session

        return redirect(url_for('login'))
@app.route('/logout')
def logout():
    session.pop('user',None)
    return render_template('logout.html')


@app.route('/hello/<name>/<int:id>')
def hello(name,id):
        pid = str(id)
        return "Hello "+name+" "+pid+"!!"

@app.route('/hello/admin')
def hello_admin():
    return('Hello admin user!!')

@app.route('/hello/guest/<guest>')
def hello_guest(guest):
        return "Hello Guest user with name "+guest+"!!!"

@app.route('/hello/user/<name>')
def hello_user(name):
    if name=='admin':
        return redirect(url_for('hello_admin'))
    else:
        return redirect(url_for('hello_guest',guest=name))

if __name__ == '__main__':
    app.run(debug = True)