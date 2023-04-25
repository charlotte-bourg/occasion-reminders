"""Server for occasion reminders app."""

import requests
import flask #is from flask import * worse? consider being more specific on modules 
from model import connect_to_db,db
import crud
import os 
from datetime import datetime
#from quickstart.py on people api quickstart page 
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

app = flask.Flask(__name__)
app.secret_key = os.environ['FLASK_KEY']
SCOPES = ['https://www.googleapis.com/auth/contacts.readonly',
                'https://www.googleapis.com/auth/userinfo.email',
                'https://www.googleapis.com/auth/userinfo.profile', 
                'https://www.googleapis.com/auth/calendar.readonly',
                'https://www.googleapis.com/auth/calendar.events',
                'openid'] #https://github.com/requests/requests-oauthlib/issues/387
CLIENT_SECRETS_FILE = 'client_secret.json'

@app.route('/')
def index():
    """Landing page"""
    return flask.render_template('index.html')

@app.route('/logout')
def clear_session_vars():
    flask.session.clear()
    return flask.redirect('/')
    
@app.route('/authenticate')
def google_authenticate():
    """Allow user to authenticate with Google account / oauth"""
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes = SCOPES) 
    flow.redirect_uri  = 'http://localhost:5050/oauthcallback'
    authorization_url, state = flow.authorization_url(access_type = 'offline', 
                                                      include_granted_scopes = 'true')
    flask.session['state'] = state
    return flask.redirect(authorization_url)

@app.route('/oauthcallback')
def oauthcallback():
    state = flask.session['state']
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, 
                                                                   scopes = SCOPES, 
                                                                   state=state)
    flow.redirect_uri = flask.url_for('oauthcallback', _external=True)

    authorization_response = flask.request.url
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    flask.session['credentials'] = credentials_to_dict(credentials)
    application_user_login() 
    
    return flask.redirect('/homepage')

@app.route('/homepage')
def display_logged_in_homepage():
    """Logged in homepage"""
    
    return flask.render_template('homepage.html')

@app.route('/manage-tiers')
def manage_tiers():
    """Edit tiers"""
    user = crud.get_user_by_id(flask.session["user_id"])
    tiers = crud.get_tiers_by_user(user)
    return flask.render_template('tiers.html', tiers=tiers)

@app.route('/update-tier', methods = ['POST'])
def update_tier():
    occasion_id = flask.request.json["occasion_id"]
    tier_id = flask.request.json["tier_id"]
    crud.update_tier(occasion_id, tier_id)
    db.session.commit()
    name = crud.get_tier_name_by_id(tier_id)
    print(f"name is {name}")
    return {
        "success": True,
        "tier_name": name}

@app.route('/add-tier', methods = ['POST'])
def add_tier():
    """Add tier"""
    user = crud.get_user_by_id(flask.session["user_id"])
    name = flask.request.form.get("tier-name")
    description = flask.request.form.get("tier-desc")
    days_ahead = flask.request.form.get("tier-days-ahead")
    reminder_type = flask.request.form.get("tier-reminder-type")
    tier = crud.create_tier(user, name, description, days_ahead, reminder_type,"tbd")
    db.session.add(tier)
    db.session.commit()
    return flask.redirect('/manage-tiers')

@app.route('/import-contacts')
def import_contacts():
    user = crud.get_user_by_id(flask.session["user_id"])
    if "contacts_imported" not in flask.session:
        credentials = Credentials(**flask.session['credentials'])
        contacts_service = build('people', 'v1', credentials = credentials)
        results = contacts_service.people().connections().list(
            resourceName='people/me',
            pageSize=1000,
            personFields='names,birthdays,events,memberships').execute()
        connections = results.get('connections', [])
        for person in connections:
            fname = person["names"][0]["givenName"] #todo can there be multiple names? 
            lname = person["names"][0]["familyName"]
            birthday_json = person["birthdays"][0]["date"] #todo can there be multiple birthdays
            birthday = datetime(birthday_json["year"], birthday_json["month"], birthday_json["day"]) #todo account for missing data
            contact = crud.create_contact(user, fname, lname)
            occasion = crud.create_occasion(contact, "birthday", True, birthday)
            db.session.add(contact)
            db.session.add(occasion)
            db.session.commit() 
        contacts_service.close()
        flask.session["contacts_imported"] = 1
    occasions = crud.get_occasions_by_user(user)
    return flask.render_template("contacts.html", occasions = occasions)

@app.route('/get-calendar')
def calendar(): #rename
    #user = crud.get_user_by_id(flask.session["user_id"])
    credentials = Credentials(**flask.session['credentials'])
    calendar_service = build('calendar', 'v3', credentials = credentials)
    calendar_list = calendar_service.calendarList().list().execute()
    #results = calendar_service.events().list(calendarId='primary').execute()
    cals = calendar_list.get('items',[])
    print(f"your calendar_list is: {calendar_list}")
    # flash message for user selection of their calendar
    return flask.render_template("cal.html", cals = cals)

#@app.route('/select-cal-<cal_id>')
#def select_cal(cal_id):
#    user = crud.get_user_by_id(flask.session["user_id"])
#    crud.update_selected_cal(user, cal_id)
#    db.session.commit()
#    print(f"ur id is!!!! : {cal_id}")
#    flask.flash("Updated your selected calendar!")
#    return flask.redirect('/sync-events')

@app.route('/select-cal', methods = ['POST'])
def select_cal():
    cal_id = flask.request.form.get("cal_id")
    user = crud.get_user_by_id(flask.session["user_id"])
    crud.update_selected_cal(user, cal_id)
    db.session.commit()
    print(f"ur id is!!!! : {cal_id}")
    flask.flash("Updated your selected calendar!")
    return flask.redirect('/sync-events')

@app.route('/sync-events')
def sync_events():
    return flask.render_template('sync.html')

@app.route('/preview-changes')
def preview_changes():
    #https://developers.google.com/calendar/api/v3/reference/events/list
    user = crud.get_user_by_id(flask.session["user_id"])
    cal_id = crud.get_cal_id_by_user(user)
    print(f"your cal id is {cal_id}")
    credentials = Credentials(**flask.session['credentials']) #modularize building service 
    calendar_service = build('calendar', 'v3', credentials = credentials)
    events = calendar_service.events().list(calendarId=cal_id).execute()
    print(events)
    return flask.render_template('sync.html')

@app.route('/assign-tiers')
def assign_tiers():
    user = crud.get_user_by_id(flask.session["user_id"])
    occasions = crud.get_occasions_by_user(user)
    tiers = crud.get_tiers_by_user(user)
    return flask.render_template("contacts-and-tiers.html", occasions = occasions, tiers=tiers)

def application_user_login():
    """Parse user details from oauth and handle application database user login"""
    token = flask.session['credentials']['token']
    res = requests.get(f'https://www.googleapis.com/oauth2/v1/userinfo?access_token={token}')
    oauth_user_details = res.json()
    email = oauth_user_details.get('email',"")
    user = crud.get_user_by_email(email)
    if user:
        flask.session["user_id"] = user.user_id
        return
    name = oauth_user_details.get('name', " ")
    fname,lname = name.split(" ")
    user = crud.create_user(email, fname, lname)
    db.session.add(user)
    db.session.commit()
    flask.session["user_id"] = user.user_id
    return 

def credentials_to_dict(credentials): #https://developers.google.com/identity/protocols/oauth2/web-server#python
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}
    # TODO Store the credentials in the session.
    # ACTION ITEM for developers:
    #     Store user's access and refresh tokens in your data store if
    #     incorporating this code into your real app.

if __name__ == "__main__":
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' #TODO disable for prodution
    connect_to_db(app)
    app.run(host="0.0.0.0", port = 5050, debug=True)