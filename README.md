## Occasion Reminders

Developer: Charlotte Bourg ([LinkedIn](https://www.linkedin.com/in/charlottebourg/), [GitHub](https://github.com/charlotte-bourg))

Occasion Reminders is a full stack web application helps users bulk manage reminders for important dates in their loved ones' lives, and integrates with the Google contacts and Google calendar tools that they already use. Users can import contacts to create trackable occasions from all of the birthdays and anniversaries they have stored. They can then create groups based on the type of notifications they want to receive and apply those groups to their occasions in bulk. Finally, they can sync all of those events to their Google calendar with appropriate reminders.  

#### Technologies
Python, Flask, SQLAlchemy, Postgres, HTML/CSS, Bootstrap, Javascript, AJAX, Google  People API, Google Calendar API

#### Features
##### V.1 (current)
- Log in with Oauth2 with Google account
- Import occasions from Google contacts to local database
- Reimport occasions to reflect any changes in Google contacts
- Create notification groups in local database with a name, description, reminder type, and reminder timeline
- Bulk apply notification groups to occasions
- Preview events before creating on calendar
- Create all events on calendar with 1 click

##### V.2 (in development)
- Transition to React
- Allow exporting notification groups as labels on Google contacts
- Allow updating events that were created by Occasion Reminders
- Allow tracking gift ideas in event body

##### Import occasions from contacts
![Img](/static/import%20contacts.png)
##### Edit notification groups
![img](/static/notification%20groups.png)
##### Apply notification Groups
![img](/static/apply%20groups.png)
##### Update calendar reminders
![Img](/static/saved%20to%20cal.png)
