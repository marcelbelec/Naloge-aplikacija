# Flask moduli za spletno aplikacijo
from flask import Flask, render_template, request, redirect, url_for, abort
from werkzeug.exceptions import HTTPException

# Moduli za obrazce
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

# Moduli za delo z bazo podatkov
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc

# Ustvarimo Flask aplikacijo in naložimo konfiguracijo
app = Flask(__name__, instance_relative_config=False)
app.config.from_pyfile('config.py')

# Nastavimo bazo podatkov
db = SQLAlchemy(app)

# Glavna stran, kjer prikažemo naloge
@app.route('/', methods=['GET', 'POST'])
@app.route('/<filter>', methods=['GET', 'POST'])
def list_tasks(filter='all'):
    # Preverimo, ali je filter veljaven; če ni, vrnemo 404 napako
    if filter not in ['all', 'active', 'completed']:
        abort(404)

    records = None
    count = 0

    # Pridobimo naloge glede na filter (vse, aktivne, zaključene)
    if filter == 'all':
        records = db.session.query(Task)
        count = db.session.query(Task).count()
    elif filter == 'active':
        records = db.session.query(Task).filter(Task.complete == 0)
        count = db.session.query(Task).filter(Task.complete == 0).count()
    elif filter == 'completed':
        records = db.session.query(Task).filter(Task.complete == 1)
        count = db.session.query(Task).filter(Task.complete == 1).count()

    # Pripravimo obrazec za dodajanje naloge
    form = AddTaskForm()

    # Obdelamo podatke iz obrazca
    if form.validate_on_submit():
        if request.method == 'POST' and 'submit' in request.form:
            # Ustvarimo nov zapis (nalogo) in jo shranimo v bazo
            record = Task(
                title = request.form.get('title'),
                complete = 0
            )
            db.session.merge(record)
            db.session.commit()

    # Prikažemo glavno stran z nalogami
    return render_template('index.html', data=records, count=count, filter=filter, form=form)

# Izbrišemo nalogo glede na ID
@app.route('/task/delete/<id>', methods=['GET', 'POST'])
def delete_task(id):
    # Pridobimo nalogo iz baze
    record = db.session.query(Task).get(id)
    form = DeleteTaskForm()

    # Obdelamo obrazec za brisanje naloge
    if form.validate_on_submit():
        if request.method == 'POST' and 'submit' in request.form:
            db.session.delete(record)
            db.session.commit()
        return redirect(url_for('list_tasks'))

    return render_template('delete.html', title='Izbriši nalogo', form=form)

# Preklopimo status naloge (končana/nekončana)
@app.route('/task/status/<id>/<filter>', methods=['GET', 'POST'])
def toggle_task_status(id, filter='all'):
    # Pridobimo nalogo iz baze
    record = db.session.query(Task).get(id)
    # Spremenimo status naloge
    record.complete = not record.complete

    try:
        db.session.commit()
    except exc.SQLAlchemyError:
        return {}

    return {'id': id, 'filter': filter}

# Prikaz strani z napakami
@app.errorhandler(HTTPException)
def handle_exception(error):
    return render_template('error.html', error=error), error.code

# Obrazec za dodajanje nalog
class AddTaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired('Vnesite naslov naloge!')])
    submit = SubmitField('Dodaj')

# Obrazec za brisanje nalog
class DeleteTaskForm(FlaskForm):
    submit = SubmitField('Izbriši')

# Definicija modela za naloge
class Task(db.Model):
    __tablename__ = 'task'
    id       = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    title    = db.Column(db.String, nullable=False)
    complete = db.Column(db.Boolean, default=0)

    def __init__(self, title, complete=0):
        self.title = title
        self.complete = complete

    def __repr__(self):
        return '<Task %r>' % self.title

# Ustvarimo bazo podatkov, če še ne obstaja
with app.app_context():
    db.create_all()

# Zagon aplikacije
if __name__ == '__main__':
    app.run(debug=True)