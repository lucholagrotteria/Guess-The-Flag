from flask import Blueprint, render_template, request, session, flash, redirect, url_for
import json, random

views = Blueprint('views', __name__)

def load_data(route):
    try:
        with open(route) as f:
            return json.load(f)
    
    except FileNotFoundError:
        flash('Error: file not found', category='error')
        return {}


def get_country_data(session, data):
    country_code = session.get('country_code')
    country_name = data.get(country_code)
    
    return country_code, country_name

@views.route('/', methods=['GET', 'POST'])
def home():
    route = 'data/flags.json'
    data = load_data(route)
    
    if 'country_codes' not in session:
        session['country_codes'] = list(data.keys())

    country_codes = session['country_codes']
    right_answers = session.get('right_answers', 0)

    if len(country_codes) > 0:
        if 'country_code' not in session:
            session['country_code'] = random.choice(country_codes)

        country_code, country_name = get_country_data(session, data)


    if request.method == 'POST':
        country = request.form.get('country')

        print(country, country_name)

        if country.lower() == country_name.lower():
            print('Match!')
            flash('Right answer!', category='success')
            country_codes.remove(country_code)
            right_answers += 1
            session['country_codes'] = country_codes
            session['right_answers'] = right_answers

            if len(country_codes) > 0:
                session['country_code'] = random.choice(country_codes)
                country_code, country_name = get_country_data(session, data)
            else:
                session.pop('country_code')

        else:
            flash('Wrong answer!', category='error')


    return render_template('home.html', country_code=country_code, right_answers=right_answers)

@views.route('/restart', methods=['POST'])
def restart():
    session.pop('right_answers', None)
    session.pop('country_codes', None)
    session.pop('country_code', None)
    session.pop('country_name', None)
    return redirect(url_for('views.home'))

