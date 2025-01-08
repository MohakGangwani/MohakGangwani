import yaml
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mail import Mail, Message

# Load content from params.yaml
with open('params.yaml', 'r') as file:
    content = yaml.safe_load(file)

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your secure key

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = content['email']['id']  # Replace with your email
app.config['MAIL_PASSWORD'] = content['email']['password']  # Replace with your email password
app.config['MAIL_DEFAULT_SENDER'] = content['email']['id']  # Replace with your email

mail = Mail(app)


@app.route('/')
@app.route('/index')
def home():
    navbar = {
        'index': 'active',
        'resume': 'inactive',
        'projects': 'inactive',
        'services': 'inactive',
        'contact': 'inactive'
    }
    return render_template('index.html', title="Home", content=content, navbar=navbar)

@app.route('/resume')
def resume():
    navbar = {
        'index': 'inactive',
        'resume': 'active',
        'projects': 'inactive',
        'services': 'inactive',
        'contact': 'inactive'
    }
    return render_template('resume.html', title="Resume", content=content, navbar=navbar)

@app.route('/projects')
def projects():
    navbar = {
        'index': 'inactive',
        'resume': 'inactive',
        'projects': 'active',
        'services': 'inactive',
        'contact': 'inactive'
    }
    return render_template('projects.html', title="Projects", content=content, navbar=navbar)

@app.route('/services')
def services():
    navbar = {
        'index': 'inactive',
        'resume': 'inactive',
        'projects': 'inactive',
        'services': 'active',
        'contact': 'inactive'
    }
    return render_template('services.html', title="Services", content=content, navbar=navbar)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    print("Got in Contact")
    navbar = {
        'index': 'inactive',
        'resume': 'inactive',
        'projects': 'inactive',
        'services': 'inactive',
        'contact': 'active'
    }

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']

        try:
            # Send email
            msg = Message(subject=f"Contact Form: {subject}",
                          sender=email,
                          recipients=[content['email']['id']])
            msg.body = f"""New message from {name} ({email}):\n\n{message}"""
            mail.send(msg)

            # Add a success flash message
            print(f"Email sent successfully to {email}")
            flash('Message was sent successfully', 'success')
            return redirect(url_for('contact'))

        except Exception as e:
            # Add an error flash message
            print(f"Error: {e}")
            flash('Failed to send the message. Please try again.', 'danger')
            return redirect(url_for('contact'))

    return render_template('contact.html', title="Contact", content=content, navbar=navbar)


if __name__ == '__main__':
    app.run(debug=True)