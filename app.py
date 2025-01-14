import yaml
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mail import Mail, Message
import math
from src.utils import *
install_spacy_model()

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



MOVIES_DF = load_preprocess_data(content['movierecommender']).reset_index().rename(columns={'index': 'id'})
MOVIES_DF['processed_title'] = MOVIES_DF['title'].str.lower()
MOVIES_LIST = MOVIES_DF.to_dict(orient='records')
MOVIES_PER_PAGE = 25
# Preprocess MOVIES_LIST into a dictionary for quick lookup
MOVIES_DICT = {movie['id']: movie for movie in MOVIES_LIST}


# Preload recommendation system data
vectors = get_vector(None, content['movierecommender'])  # Assuming this loads all vectors at once
model = get_sim_model(vectors, content['movierecommender'])  # Load the model only once
PRELOADED_DATA = {
    "movies": MOVIES_DF.set_index("id").to_dict(orient="index"),  # Dictionary for quick ID lookups
    "vectors": vectors,
    "model": model,
    "params": content['movierecommender'],
}

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

@app.route('/projects/movierecommender', methods=['GET', 'POST'])
def recommenderhome():
    query = request.args.get('query', '').lower()
    page = int(request.args.get('page', 1))

    # Filter and paginate movies
    filtered_movies = [movie for movie in MOVIES_LIST if query in movie['processed_title']] if query else MOVIES_LIST
    total_movies = len(filtered_movies)
    total_pages = math.ceil(total_movies / MOVIES_PER_PAGE)
    start_idx = (page - 1) * MOVIES_PER_PAGE
    movies_to_display = filtered_movies[start_idx:start_idx + MOVIES_PER_PAGE]
    navbar = {
        'index': 'inactive',
        'resume': 'inactive',
        'projects': 'active',
        'services': 'inactive',
        'contact': 'inactive'
    }
    return render_template(
        'recommender.html',
        title='Recommender System',
        movies={movie['id']: movie for movie in movies_to_display},
        query=query,
        page=page,
        total_pages=total_pages,
        content=content,
        navbar=navbar
    )


@app.route('/projects/movierecommender/movie/<int:movie_id>')
def movie_details(movie_id):
    # Get the current page number (for pagination)
    page = request.args.get('page', 1, type=int)
    query = request.args.get('query', '', type=str)
    
    # Find the movie by ID
    movie = MOVIES_DICT.get(movie_id)
    if not movie:
        return "Movie not found", 404
    
    # Get recommendations using preloaded data
    recommendations = recommend_movie(movie_id, PRELOADED_DATA)
    
    # Navbar state to highlight the active page
    navbar = {
        'index': '',
        'resume': '',
        'projects': 'active',
        'contact': ''
    }
    
    # Render movie details page with dynamic navbar
    return render_template(
        'movie_details.html',
        movie=movie,
        recommendations=recommendations,
        navbar=navbar,
        query=query,
        page=page,
        title=f"Movie Details - {movie['title']}"
    )


if __name__ == '__main__':
    app.run()