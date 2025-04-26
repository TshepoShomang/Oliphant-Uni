from flask import Flask, render_template, request, redirect, url_for, session
import firebase_admin
from firebase_admin import credentials, firestore
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

cred = credentials.Certificate("data.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


ADMIN_USERNAME = 'DokoelaBu'
ADMIN_PASSWORD = 'Player$Bu'

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/contributors")
def contributors():
    return render_template("contributors.html")

@app.route("/director")
def director():
    return render_template("director.html")

@app.route("/home")
def back():
    return render_template("home.html")

@app.route("/pricing")
def pricing():
    return render_template("pricing.html")

@app.route("/service")
def service():
    return render_template("service.html")

@app.route("/whyUs")
def whyUs():
    return render_template("whyUs.html")

@app.route("/application_page")
def application_page():
    return render_template("application.html")


@app.route('/submit_application', methods=['POST'])
def submit_application():
    id_number = request.form['id_number']

    uploads_dir = os.path.join(os.getcwd(), 'uploads')
    if not os.path.exists(uploads_dir):
        os.makedirs(uploads_dir)
    
    data = {
        'personal_info': {
            'title': request.form['title'],
            'dob': request.form['dob'],
            'gender': request.form['gender'],
            'initials': request.form['initials'],
            'name': request.form['name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'address': request.form['address'],
            'phone': request.form['phone'],
            'marital_status': request.form['marital_status'],
            'home_language': request.form['home_language'],
            'ethnic_group': request.form['ethnic_group'],
            'employed': request.form['employed'],
            'apply_residence': request.form['apply_residence'],
            'disability': request.form['disability'],
        },
        'application_info': {
            'institution1': request.form['institution1'],
            'institution2': request.form['institution2'],
            'institution3': request.form['institution3'],
            'course1': request.form['course1'],
            'course2': request.form['course2'],
            'course3': request.form['course3'],
        }
    }

    files = {}
    for field in ['id_document', 'cover_letter', 'latest_report']:
        file = request.files.get(field)
        if file and file.filename != '':
            filename = f"{id_number}_{field}.pdf"
            file_path = os.path.join('uploads', filename)
            file.save(file_path)
            files[field] = file_path

    # Save everything in Firestore under 1 document
    db.collection('applications').document(id_number).set({
        'data': data,
        'files': files
    })

    return 'Application submitted successfully! 🎉'



# Admin
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            return 'Invalid credentials. Try again.'
    
    return render_template('admin.html')

# Dashboard Route
@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    docs = db.collection('applications').stream()

    applicants = []
    for doc in docs:
        data = doc.to_dict()
        applicants.append({
            'id': doc.id,
            'name': data['data']['personal_info']['name'],
            'last_name': data['data']['personal_info']['last_name']
        })
    
    return render_template('dash.html', applicants=applicants)

# View Applicant Details Route
@app.route('/admin/view/<id>')
def admin_view(id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    doc = db.collection('applications').document(id).get()
    if doc.exists:
        data = doc.to_dict()
        flat_data = {}

        # Flatten nested fields for display
        for section, section_data in data['data'].items():
            for key, value in section_data.items():
                flat_data[key] = value

        return render_template('detail.html', applicant=flat_data)
    else:
        return 'Applicant not found', 404

# Logout Route
@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))

    

    

if __name__ == "__main__":
    app.run(debug=True)
