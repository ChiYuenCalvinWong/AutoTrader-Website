from flask import Flask, request, jsonify, render_template, redirect, flash
import pusher
from database import db_session
from models import Auto
from datetime import datetime
from forms import  RegistrationForm, LoginForm
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
pusher_client = pusher.Pusher(
    app_id=os.getenv('PUSHER_APP_ID'),
    key=os.getenv('PUSHER_KEY'),
    secret=os.getenv('PUSHER_SECRET'),
    cluster=os.getenv('PUSHER_CLUSTER'),
    ssl=True)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.route('/')
def index():
    autos = Auto.query.all()
    return render_template('index.html', autos=autos)
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'dealer@auto.com' and form.password.data == '4321':
            flash('You have been logged in!', 'success')
            return redirect('backend')
        elif form.email.data == 'user@auto.com' and form.password.data == '1234':
            flash('You have been logged in!', 'success')
            return redirect('user')
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect('/')
    return render_template('register.html', title='Register', form=form)

@app.route('/backend', methods=["POST", "GET"])
def backend():
    if request.method == "POST":
        status = request.form["status"]
        year = request.form["year"]
        model = request.form["model"]
        vin = request.form["vin"]
        price = request.form["price"]

        new_auto = Auto(status, year, vin, model, price)
        db_session.add(new_auto)
        db_session.commit()

        data = {
            "id": new_auto.id,
            "status": status,
            "year": year,
            "model": model,
            "vin": vin,
            "price": price}
            
        pusher_client.trigger('table', 'new-record', {'data': data })

        return redirect("/backend", code=302)
    else:
        autos = Auto.query.all()
        return render_template('backend.html', autos=autos)

@app.route('/edit/<int:id>', methods=["POST", "GET"])
def update_record(id):
    if request.method == "POST":
        status = request.form["status"]
        year = request.form["year"]
        model = request.form["model"]
        vin = request.form["vin"]
        price = request.form["price"]

        update_auto = Auto.query.get(id)
        update_auto.status = status
        update_auto.year = year
        update_auto.model = model
        update_auto.vin = vin
        update_auto.price = price

        db_session.commit()

        data = {
            "id": update_auto.id,
            "status": status,
            "year": year,
            "model": model,
            "vin": vin,
            "price": price}

        pusher_client.trigger('table', 'update-record', {'data': data })
       
        return redirect("/backend", code=302)
    else:
        new_auto = Auto.query.get(id)
        new_auto.model = new_auto.model
        new_auto.vin = new_auto.vin

        return render_template('update_flight.html', data=new_auto)

@app.route('/delete/<int:id>', methods=["POST", "GET"])
def delete_record(id):
    delete_auto = Auto.query.get(id)
    db_session.delete(delete_auto)
    db_session.commit()
    return redirect("/backend")

@app.route('/user', methods=["POST", "GET"])
def user():
    if request.method == "POST":
        status = request.form["status"]
        year = request.form["year"]
        model = request.form["model"]
        vin = request.form["vin"]
        price = request.form["price"]

        new_auto = Auto(status, year, vin, model, price)
        db_session.add(new_auto)
        db_session.commit()

        data = {
            "id": new_auto.id,
            "status": status,
            "year": year,
            "model": model,
            "vin": vin,
            "price": price}

        pusher_client.trigger('table', 'new-record', {'data': data})

        return redirect("/user", code=302)
    else:
        autos = Auto.query.all()
        return render_template('user.html', autos=autos)

@app.route('/buy/<int:id>', methods=["POST", "GET"])
def buy_car(id):

    return redirect('/user')

# run Flask app
if __name__ == "__main__":
    app.run()