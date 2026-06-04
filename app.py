from flask import Flask, render_template, request, redirect
from models import db, Patient


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


# Health Prediction Function
def predict_health(glucose, haemoglobin, cholesterol):

    if glucose > 180:
        return "High Diabetes Risk"

    elif cholesterol > 240:
        return "High Cholesterol Risk"

    elif haemoglobin < 12:
        return "Possible Anaemia"

    return "Normal"


# Home Page - Read Records
@app.route('/')
def index():

    patients = Patient.query.all()

    return render_template(
        'index.html',
        patients=patients
    )


# Add Patient - Create
@app.route('/add', methods=['GET', 'POST'])
def add_patient():

    if request.method == 'POST':

        glucose = float(request.form['glucose'])
        haemoglobin = float(request.form['haemoglobin'])
        cholesterol = float(request.form['cholesterol'])

        remarks = predict_health(
            glucose,
            haemoglobin,
            cholesterol
        )

        patient = Patient(
            full_name=request.form['full_name'],
            dob=request.form['dob'],
            email=request.form['email'],
            glucose=glucose,
            haemoglobin=haemoglobin,
            cholesterol=cholesterol,
            remarks=remarks
        )

        db.session.add(patient)
        db.session.commit()

        return redirect('/')

    return render_template('add_patient.html')


# Edit Patient - Update
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_patient(id):

    patient = Patient.query.get_or_404(id)

    if request.method == 'POST':

        patient.full_name = request.form['full_name']
        patient.dob = request.form['dob']
        patient.email = request.form['email']

        patient.glucose = float(request.form['glucose'])
        patient.haemoglobin = float(request.form['haemoglobin'])
        patient.cholesterol = float(request.form['cholesterol'])

        patient.remarks = predict_health(
            patient.glucose,
            patient.haemoglobin,
            patient.cholesterol
        )

        db.session.commit()

        return redirect('/')

    return render_template(
        'edit_patient.html',
        patient=patient
    )


# Delete Patient
@app.route('/delete/<int:id>')
def delete_patient(id):

    patient = Patient.query.get_or_404(id)

    db.session.delete(patient)
    db.session.commit()

    return redirect('/')


if __name__ == '__main__':

    with app.app_context():
        db.create_all()

    app.run(debug=True)