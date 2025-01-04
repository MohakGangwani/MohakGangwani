import yaml
from flask import Flask, render_template, request, flash
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load content from params.yaml
with open('params.yaml', 'r') as file:
    content = yaml.safe_load(file)

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your secure key

# Email Configuration
SMTP_SERVER = 'smtp.gmail.com'  # Replace with your SMTP server
SMTP_PORT = 587
EMAIL_ADDRESS = 'your_email@gmail.com'  # Replace with your email
EMAIL_PASSWORD = 'your_email_password'


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
            # Prepare the email
            msg = MIMEMultipart()
            msg['From'] = EMAIL_ADDRESS
            msg['To'] = EMAIL_ADDRESS  # Send the email to yourself
            msg['Subject'] = f"New Contact Form Submission: {subject}"

            # Email body
            body = f"""
            You have a new message from your portfolio contact form:\n
            Name: {name}\n
            Email: {email}\n
            Subject: {subject}\n
            Message:\n{message}
            """
            msg.attach(MIMEText(body, 'plain'))

            # Connect to the SMTP server and send the email
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                server.send_message(msg)

            flash("Your message has been sent successfully!", "success")
        except Exception as e:
            print(f"Error: {e}")
            flash("There was an error sending your message. Please try again later.", "danger")

        return render_template('contact.html', title="Contact", success=True, content=content, navbar=navbar)

    return render_template('contact.html', title="Contact", success=False, content=content, navbar=navbar)


if __name__ == '__main__':
    app.run(debug=True)