# @app.route('/get-calendar')
# def calendar(): #rename
#     #user = crud.get_user_by_id(flask.session["user_id"])
#     credentials = Credentials(**flask.session['credentials'])
#     calendar_service = build('calendar', 'v3', credentials = credentials)
#     calendar_list = calendar_service.calendarList().list().execute()
#     #results = calendar_service.events().list(calendarId='primary').execute()
#     cals = calendar_list.get('items',[])
#     # flash message for user selection of their calendar?
#     return flask.render_template("cal.html", cals = cals)

# @app.route('/select-cal', methods = ['POST'])
# def select_cal():
#     cal_id = flask.request.form.get("cal_id")
#     user = crud.get_user_by_id(flask.session["user_id"])
#     crud.update_selected_cal(user, cal_id)
#     db.session.commit()
#     print(f"ur id is!!!! : {cal_id}")
#     flask.flash("Updated your selected calendar!")
#     return flask.redirect('/sync-events')