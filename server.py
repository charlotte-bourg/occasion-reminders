"""Server for occasion reminders app."""

import requests
import flask 
from model import connect_to_db,db
import crud
import os 
#from quickstart.py on people api quickstart page 
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

app = flask.Flask(__name__)
app.secret_key = os.environ['FLASK_KEY']
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

@app.route('/')
def homepage():
    """Landing age"""
    return flask.render_template('homepage.html')
    
@app.route('/log-in')
def google_authenticate():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    'client_secret.json',
    scopes=['https://www.googleapis.com/auth/contacts.readonly','https://www.googleapis.com/auth/userinfo.email','https://www.googleapis.com/auth/userinfo.profile', 'openid']) #https://github.com/requests/requests-oauthlib/issues/387
    flow.redirect_uri  = 'http://localhost:5050/logged-in'
    authorization_url, state = flow.authorization_url(access_type = 'offline', include_granted_scopes = 'true')
    flask.session['state'] = state
    return flask.redirect(authorization_url)

@app.route('/logged-in')
def render_contacts():
    state = flask.session['state']
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        'client_secret.json',
        scopes=['https://www.googleapis.com/auth/contacts.readonly','https://www.googleapis.com/auth/userinfo.email','https://www.googleapis.com/auth/userinfo.profile', 'openid'],
        state=state)
    flow.redirect_uri = flask.url_for('testing', _external=True)

    authorization_response = flask.request.url
    flow.fetch_token(authorization_response=authorization_response)

    # TODO Store the credentials in the session.
    # ACTION ITEM for developers:
    #     Store user's access and refresh tokens in your data store if
    #     incorporating this code into your real app.
    credentials = flow.credentials
    flask.session['credentials'] = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes}
    res = requests.get(f'https://www.googleapis.com/oauth2/v1/userinfo?access_token={credentials.token}')
    oauth_user_details = res.json()
    if 'email' in oauth_user_details:
        email = oauth_user_details['email']
    else:
        email = ""
    if 'name' in oauth_user_details:
        name = oauth_user_details['name']
        fname, lname = name.split(" ")
    else:
        email = ""
    print(f"the logged in user is {email} with fname and lname {fname} and {lname}")
    contacts_service = build('people', 'v1', credentials = credentials) #close service later?

    results = contacts_service.people().connections().list(
        resourceName='people/me',
        pageSize=1000,
        personFields='names,birthdays,events,memberships').execute()
    connections = results.get('connections', [])

    #for person in connections:
    #    names = person.get('names', [])
    #    if names:
    #        name = names[0].get('displayName')
    #        print(name)
    return flask.render_template('logged-in.html', connections = connections)

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", port = 5050, debug=True)