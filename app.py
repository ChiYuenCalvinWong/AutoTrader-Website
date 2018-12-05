from flask import Flask, request, jsonify, render_template, redirect, flash, url_for
import pusher
from database import db_session
from models import Flight
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
    flights = Flight.query.all()
    return render_template('index.html', flights=flights)

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


@app.route('/user', methods=["POST", "GET"])
def user():
    if request.method == "POST":
        flight = request.form["flight"]
        destination = request.form["destination"]
        check_in = datetime.strptime(request.form['check_in'], '%d-%m-%Y %H:%M %p')
        departure = datetime.strptime(request.form['departure'], '%d-%m-%Y %H:%M %p')
        status = request.form["status"]

        new_flight = Flight(flight, destination, departure, check_in, status)
        db_session.add(new_flight)
        db_session.commit()

        data = {
            "id": new_flight.id,
            "flight": flight,
            "destination": destination,
            "check_in": request.form['check_in'],
            "departure": request.form['departure'],
            "status": status}

        pusher_client.trigger('table', 'new-record', {'data': data})

        return redirect("/user", code=302)
    else:
        flights = Flight.query.all()
        return render_template('user.html', flights=flights)

@app.route('/buy/<int:id>', methods=["POST", "GET"])
def buy_car(id):

    return redirect('/user')

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
        flight = request.form["flight"]
        destination = request.form["destination"]
        check_in = datetime.strptime(request.form['check_in'], '%d-%m-%Y %H:%M %p')
        departure = datetime.strptime(request.form['departure'], '%d-%m-%Y %H:%M %p')
        status = request.form["status"]

        new_flight = Flight(flight, destination, departure, check_in, status)
        db_session.add(new_flight)
        db_session.commit()

        data = {
            "id": new_flight.id,
            "flight": flight,
            "destination": destination,
            "check_in": request.form['check_in'],
            "departure": request.form['departure'],
            "status": status}
            
        pusher_client.trigger('table', 'new-record', {'data': data })

        return redirect("/backend", code=302)
    else:
        flights = Flight.query.all()
        return render_template('backend.html', flights=flights)

@app.route('/edit/<int:id>', methods=["POST", "GET"])
def update_record(id):
    if request.method == "POST":
        flight = request.form["flight"]
        destination = request.form["destination"]
        check_in = datetime.strptime(request.form['check_in'], '%d-%m-%Y %H:%M %p')
        departure = datetime.strptime(request.form['departure'], '%d-%m-%Y %H:%M %p')
        status = request.form["status"]

        update_flight = Flight.query.get(id)
        update_flight.flight = flight
        update_flight.destination = destination
        update_flight.check_in = check_in
        update_flight.departure = departure
        update_flight.status = status

        db_session.commit()

        data = {
            "id": id,
            "flight": flight,
            "destination": destination,
            "check_in": request.form['check_in'],
            "departure": request.form['departure'],
            "status": status}

        pusher_client.trigger('table', 'update-record', {'data': data })

        return redirect("/backend", code=302)
    else:
        new_flight = Flight.query.get(id)
        new_flight.check_in = new_flight.check_in.strftime("%d-%m-%Y %H:%M %p")
        new_flight.departure = new_flight.departure.strftime("%d-%m-%Y %H:%M %p")

        return render_template('update_flight.html', data=new_flight)

@app.route('/delete/<int:id>', methods=["POST", "GET"])
def delete_record(id):
    delete_flight = Flight.query.get(id)
    db_session.delete(delete_flight)
    db_session.commit()
    return redirect("/backend")


# run Flask app
if __name__ == "__main__":
    app.run()