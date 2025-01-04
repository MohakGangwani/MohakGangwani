import yaml
from flask import Flask, render_template, request

# Load content from params.yaml
with open('params.yaml', 'r') as file:
    content = yaml.safe_load(file)

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def home():
    return render_template('index.html', title="Home", content=content)

@app.route('/resume')
def resume():
    return render_template('resume.html', title="Resume", content=content)

@app.route('/projects')
def projects():
    return render_template('projects.html', title="Projects", content=content)

@app.route('/services')
def services():
    return render_template('services.html', title="Services", content=content)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        # Process the form data (e.g., save to database or send an email)
        return render_template('contact.html', title="Contact", success=True, name=name, content=content)
    return render_template('contact.html', title="Contact", success=False, content=content)

if __name__ == '__main__':
    app.run(debug=True)