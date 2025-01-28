import yaml
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mail import Mail, Message
import datetime
import geoip2.database

# Load content from params.yaml
with open('params.yaml', 'r') as file:
    content = yaml.safe_load(file)

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = content['email']['id']
app.config['MAIL_PASSWORD'] = content['email']['password']
app.config['MAIL_DEFAULT_SENDER'] = content['email']['id']

mail = Mail(app)




# Path to the GeoIP2 database (you need to download this)
GEOIP_DATABASE_PATH = 'GeoLite2-City.mmdb'

def log_user_access():
    # Get user IP address
    user_ip = request.remote_addr
    # Get user agent (browser/device info)
    user_agent = request.headers.get('User-Agent')
    # Get current timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Get location information using GeoIP2
    try:
        with geoip2.database.Reader(GEOIP_DATABASE_PATH) as reader:
            response = reader.city(user_ip)
            city = response.city.name
            country = response.country.name
            # Log the details (you can save this to a file or database)
            log_entry = f"Time: {timestamp}, IP: {user_ip}, Location: {city}, {country}, User Agent: {user_agent}\n"
    except Exception as e:
        exception = e
        city = "Unknown"
        country = "Unknown"
        # Log the details (you can save this to a file or database)
        log_entry = f"Time: {timestamp}, IP: {user_ip}, Location: {city}, {country}, User Agent: {user_agent}\nError: {e}\n"
    print(log_entry)
    with open("access_log.txt", "a") as log_file:
        log_file.write(log_entry)




@app.route('/')
@app.route('/index')
def home():
    log_user_access()
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
            # Send email
            msg = Message(subject=f"Contact Form: {subject}",
                          sender=app.config['MAIL_DEFAULT_SENDER'],
                          recipients=[app.config['MAIL_DEFAULT_SENDER']])
            msg.body = f"""New message from {name} ({email}):\n\n{message}"""
            mail.send(msg)

            # Add a success flash message
            flash('Message Sent Successfully!', 'success')

        except Exception as e:
            # Add an error flash message
            flash(f'Failed to send the message. Error: {str(e)}', 'danger')

        # Redirect to the contact page (GET request)
        return redirect(url_for('contact'))

    return render_template('contact.html', title="Contact", content=content, navbar=navbar)


if __name__ == '__main__':
    app.run()