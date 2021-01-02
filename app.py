from flask import Flask, render_template, request
from config.models import db

from views.send_email import send_email
from config.models import Feedback

app = Flask(__name__)

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/webtasks'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://khzvpmtkdffnup:56d605f53b517d12446d92cf5a4b8df82ac0bd3b6d73476e58b49a2e73fd3442@ec2-54-197-34-207.compute-1.amazonaws.com:5432/d91kf548ftrtdj'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
app.app_context().push()


@app.before_first_request
def create_tables():
    print("printing before function fires")
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        customer = request.form['customer']
        dealer = request.form['dealer']
        rating = request.form['rating']
        comments = request.form['comments']
        print(customer, dealer, rating, comments)
        if customer == '' or dealer == '':
            return render_template('index.html', message='Please enter required fields')
        if db.session.query(Feedback).filter(Feedback.customer == customer).count() == 0:
            data = Feedback(customer, dealer, rating, comments)
            db.session.add(data)
            db.session.commit()
            # send_email(customer, dealer, rating, comments)
            return render_template('dashboard.html')
        return render_template('index.html', message='You have already submitted feedback')


if __name__ == '__main__':
    app.run(debug=True)
