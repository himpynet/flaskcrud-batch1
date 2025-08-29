from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy	

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///employee.db"

db = SQLAlchemy(app)
app.app_context().push()

class Employee(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200), nullable = False)
    email = db.Column(db.String(200), nullable = False)

    def __repr__(self):
        return f"{self.sno} - {self.name}"
    
@app.route("/", methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        # print('post done')
        # print(request.form['name'])
        name = request.form['name']
        email = request.form['email']
        employee = Employee(name = name, email = email)
        db.session.add(employee)
        db.session.commit()
    allemployee = Employee.query.all()
    return render_template("index.html", allemployee=allemployee)

@app.route("/display")
def display():
    allemployee = Employee.query.all()
    print(allemployee)
    return "This is page 2"

@app.route("/delete/<int:sno>")
def delete(sno):
    employee = Employee.query.filter_by(sno=sno).first()
    db.session.delete(employee)
    db.session.commit()
    return redirect("/")

@app.route("/update/<int:sno>", methods=['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        employee = Employee.query.filter_by(sno=sno).first()
        employee.name = name
        employee.email = email
        db.session.add(employee)
        db.session.commit()
        return redirect('/')
    employee = Employee.query.filter_by(sno=sno).first()
    return render_template("update.html", employee=employee)
    
    
if __name__ == "__main__":
    app.run(debug=True)