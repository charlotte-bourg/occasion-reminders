"""Server for occasion reminders app.""" 
#best practices for imports: https://peps.python.org/pep-0008/#imports, clean these up based on what you use 
import os

import flask
import requests
import json

from datetime import datetime,timedelta 

from google.auth.transport.requests import Request #from quickstart.py on people api quickstart page 
from google.oauth2.credentials import Credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import crud
from model import db, connect_to_db

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
    """Display pre-login page."""
    return flask.render_template('index.html')

@app.route('/login')
def login():
    return flask.render_template('login.html')

@app.route('/logout')
def clear_session_vars():
    """Log out."""
    flask.session.clear()
    return flask.redirect('/')

@app.route('/authenticate')
def google_authenticate():
    """Authenticate using oauth with user Google account."""
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
    """Callback for authentication."""
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
    return flask.redirect('/home')

@app.route('/import-occasions-from-contacts')
def display_import_contacts():
    """Display logged in homepage."""
    user = crud.get_user_by_id(flask.session["user_id"])
    occasions = crud.get_occasions_by_user(user)
    tiers = user.tiers 
    return flask.render_template('sidebar-import-contacts.html', 
                                 user=user,
                                 occasions=occasions, 
                                 tiers=tiers,
                                 has_imported = crud.user_has_local_contacts(user))

@app.route('/edit-notification-groups')
def display_edit_notification_groups():
    user = crud.get_user_by_id(flask.session["user_id"])
    occasions = crud.get_occasions_by_user(user)
    tiers = user.tiers 
    return flask.render_template('sidebar-edit-notification-groups.html', 
                                 user=user,
                                 occasions=occasions, 
                                 tiers=tiers,
                                 has_imported = crud.user_has_local_contacts(user))

@app.route('/apply-notification-groups')
def display_apply_notification_groups():
    user = crud.get_user_by_id(flask.session["user_id"])
    occasions = crud.get_occasions_by_user(user)
    tiers = user.tiers 
    return flask.render_template('sidebar-apply-notification-groups.html', 
                                 user=user,
                                 occasions=occasions, 
                                 tiers=tiers,
                                 has_imported = crud.user_has_local_contacts(user))

@app.route('/update-calendar-reminders')
def display_update_calendar_reminders():
    user = crud.get_user_by_id(flask.session["user_id"])
    occasions = crud.get_occasions_by_user(user)
    tiers = user.tiers 
    return flask.render_template('sidebar-update-calendar-reminders.html', 
                                 user=user,
                                 occasions=occasions, 
                                 tiers=tiers,
                                 has_imported = crud.user_has_local_contacts(user))

@app.route('/export-reminder-tags')
def display_export_reminder_tags():
    user = crud.get_user_by_id(flask.session["user_id"])
    occasions = crud.get_occasions_by_user(user)
    tiers = user.tiers 
    return flask.render_template('sidebar-export-reminder-tags.html', 
                                 user=user,
                                 occasions=occasions, 
                                 tiers=tiers,
                                 has_imported = crud.user_has_local_contacts(user))

@app.route('/update-tier', methods = ['POST']) 
def update_tier():
    """Update a tier on an occasion."""
    occasion_ids = flask.request.json["occasion_ids"]
    tier_id = int(flask.request.json["tier_id"])
    for occasion_id in occasion_ids:
        crud.update_tier(occasion_id, tier_id)
    db.session.commit()
    name = crud.get_tier_by_id(tier_id).name
    return {
        "success": True,
        "tier_name": name} #something weird hapening with sort order

@app.route('/tier-in-use') 
def check_tier_usage():
    """Check if tier is in use anywhere to allow user to confirm deletion."""
    tier_id = int(flask.request.args.get("tier_id"))
    if crud.occasions_with_tier(tier_id):
        return {"in_use": True}
    else:
        return {"in_use": False}

@app.route('/delete-tier', methods = ['POST']) 
def delete_tier():
    """Delete a tier."""
    tier_id = int(flask.request.json["tier_id"])
    occasions = crud.get_occasions_by_tier(tier_id)
    occasion_ids = []
    for occasion in occasions:
        crud.update_tier(occasion.occasion_id, None)
        occasion_ids.append(occasion.occasion_id)
    tier = crud.get_tier_by_id(tier_id)
    db.session.delete(tier)
    db.session.commit()
    return {
        "success": True, 
        "occasion_ids": occasion_ids,
        "tier_id": tier_id
    }

@app.route('/add-tier', methods = ['POST']) 
def add_tier():
    """Add a tier."""
    user = crud.get_user_by_id(flask.session["user_id"])
    name = flask.request.json["tier-name"]
    description = flask.request.json["tier-desc"]
    days_ahead = flask.request.json["tier-days-ahead"]
    reminder_type = flask.request.json["tier-reminder-type"]
    tier = crud.create_tier(user, name, description, days_ahead, reminder_type,"tbd") #handle tbd
    db.session.add(tier)
    db.session.commit()
    return { #better way to do this than sending back and forth? might simplify out if i change to react
        "success": True,
        "tier-name": name,
        "tier-desc": description,
        "tier-days-ahead": days_ahead,
        "tier-reminder-type": reminder_type}

@app.route('/clear-contacts') 
def clear_occasions_and_contacts():
    """Clear the user's contacts & occasions in the application database to prepare for a refresh."""
    user = crud.get_user_by_id(flask.session["user_id"])
    occasions = crud.get_occasions_by_user(user)
    contacts = crud.get_contacts_by_user(user)
    for occasion in occasions:
        db.session.delete(occasion)
    for contact in contacts:
        db.session.delete(contact)
    db.session.commit()
    return flask.redirect('/import-contacts-helper')

@app.route('/update-contacts') 
def update_contacts():
    """"WIP"""

    user = crud.get_user_by_id(flask.session["user_id"])
    
    # occasions = crud.get_occasions_by_user(user)
    # contacts = crud.get_contacts_by_user(user)
    # for occasion in occasions:
    #     db.session.delete(occasion)
    # for contact in contacts:
    #     db.session.delete(contact)
    # db.session.commit()
    return flask.redirect('/import-contacts-helper')

@app.route('/import-contacts-helper') # fix refreshing this page when you land on contacts 
def import_contacts():
    """Import contacts from user's Google contacts."""
    if "user_id" not in flask.session:
        flask.flash("Please log in to access this page!")
        return flask.redirect('/')
    user = crud.get_user_by_id(flask.session["user_id"])
    credentials = Credentials(**flask.session['credentials'])
    contacts_service = build('people', 'v1', credentials = credentials)
    results = contacts_service.people().connections().list(
        resourceName='people/me',
        pageSize=1000,
        personFields='names,birthdays,events,memberships,events',
        requestSyncToken=True).execute()
    connections = results.get('connections', [])
    sync_token = results.get('nextSyncToken', "")
    user.last_sync_token = sync_token
    for person in connections:
        fname = person["names"][0]["givenName"] #todo can there be multiple names? 
        lname = person["names"][0]["familyName"] #handle null case 
        contact = crud.create_contact(user, fname, lname)
        db.session.add(contact)
        resource_name = person["resourceName"]
        contact.resource_name = resource_name 
        birthday_json = person["birthdays"][0]["date"] #todo can there be multiple birthdays
        birthday = datetime(birthday_json["year"], birthday_json["month"], birthday_json["day"]) #todo account for missing data
        bday = crud.create_occasion(contact, "birthday", True, birthday)
        db.session.add(bday)
        events_json = person.get("events","")
        if events_json:
            for event in events_json:
                if event['type'] == 'anniversary':
                    anni_date = event['date']
                    anniversary = datetime(anni_date["year"], anni_date["month"], anni_date["day"])
                    anni = crud.create_occasion(contact, "anniversary", True, anniversary)
                    print(f"hey I added {fname}'s anni, {anni}")
                    db.session.add(anni)
    db.session.commit() 
    contacts_service.close() 
    user.last_contact_import = datetime.now()
    flask.flash("Successfully reimported your contacts!")
    return flask.redirect('/import-occasions-from-contacts')
    
# @app.route('/update-calendar-reminders')
# def display_update_calendar_reminders():
#     return flask.render_template('sidebar_update_calendar_reminders.html')

@app.route('/edit-method')
def select_method():
    method = flask.request.args.get("method")
    if method == "add":
        return flask.redirect('/add-preview')
    else: 
        return flask.redirect('/update-preview')

@app.route('/approve-deny')
def approve_deny():
    if flask.request.args.get("approve") == "Send to calendar":
        return flask.redirect('/add-events')
    else: 
        flask.flash("Make more edits!")
        return flask.redirect('/homepage')

@app.route('/add-preview') 
def events_preview():
    user = crud.get_user_by_id(flask.session["user_id"])
    tiered_occasions = crud.get_tiered_occasions_by_user(user) 
    events = []
    for occasion in tiered_occasions: 
        events.append(create_event(occasion))
    return flask.render_template('preview.html', events = events)

@app.route('/add-events') 
def add_events():
    user = crud.get_user_by_id(flask.session["user_id"])
    tiered_occasions = crud.get_tiered_occasions_by_user(user) # need to add user feedback 
    credentials = Credentials(**flask.session['credentials']) #todo modularize building service 
    calendar_service = build('calendar', 'v3', credentials = credentials)
    added_events = []
    for occasion in tiered_occasions:
        event = create_event(occasion)
        event = calendar_service.events().insert(calendarId='primary', body=event).execute()
        print(event)
        added_events.append({'summary':event['summary'], 'link': event['htmlLink']})
    calendar_service.close()
    return flask.render_template('events.html', added_events=added_events)

@app.route('/export-contacts')
def export_preview():
    user = crud.get_user_by_id(flask.session["user_id"])
    tiered_occasions = crud.get_tiered_occasions_by_user(user) 
    sync_token = user.last_sync_token
    credentials = Credentials(**flask.session['credentials'])
    contacts_service = build('people', 'v1', credentials = credentials)

    results = contacts_service.people().connections().list(
        syncToken=sync_token,
        resourceName='people/me',
        pageSize=1000,
        personFields='names,birthdays,events,memberships',
        requestSyncToken=True).execute()
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
    nextSyncToken=results.get('nextSyncToken',"")
    print(nextSyncToken)

def create_event(occasion):
    tier = occasion.tier
    if occasion.recurring: 
        recurrence_rule = 'RRULE:FREQ=YEARLY'
    occasion_date_curr_yr = occasion.date.replace(year = datetime.now().year)
    event = {
        'summary': f'{occasion.contact.fname} {occasion.contact.lname}\'s {occasion.occasion_type}',
        'description': f'Added by Hackbright Occasion Reminders! Notification group: {occasion.tier.name}',
        'start': {
            'date': occasion_date_curr_yr.strftime('%Y-%m-%d'),
            'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'date': (occasion_date_curr_yr + timedelta(days=1)).strftime('%Y-%m-%d'),
            'timeZone': 'America/Los_Angeles', #need to handle time zone 
        },
        'recurrence': [
            recurrence_rule
        ],
        'reminders': {
            'useDefault': False,
            'overrides': [
            {'method': tier.reminder_type, 'minutes': 24 * 60 * tier.reminder_days_ahead},
            ],
        },
    }
    return event 

@app.route('/update-events') 
def update_events():
    flask.flash("this feature isn't available yet")
    return flask.redirect('/homepage')

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

@app.route('/home')
def sidebar_page():
    user = crud.get_user_by_id(flask.session["user_id"])
    return flask.render_template("sidebar-homepage.html", user=user)

def credentials_to_dict(credentials): #https://developers.google.com/identity/protocols/oauth2/web-server#python
    """Parse credentials into dictionary format for session"""
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}
    
@app.route('/revoke')
def revoke_permissions():
    #check if credentials in session 
    credentials = Credentials(**flask.session['credentials'])
    revoke = requests.post('https://oauth2.googleapis.com/revoke',
        params={'token': credentials.token},
        headers = {'content-type': 'application/x-www-form-urlencoded'})

    status_code = getattr(revoke, 'status_code')
    if status_code == 200:
        flask.flash("Credentials successfully revoked.")
        flask.redirect('/')
    else:
        flask.flash("An error occurred.")
        return flask.redirect('/')

if __name__ == "__main__":
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    connect_to_db(app)
    app.run(host="0.0.0.0", port = 5050)
    app.app_context().push()