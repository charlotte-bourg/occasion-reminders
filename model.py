"""Models for occasion reminders app."""

from  flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()    

class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, 
                        autoincrement = True,
                        primary_key = True)
    email = db.Column(db.String, unique = True)
    fname = db.Column(db.String, nullable = True)
    lname = db.Column(db.String, nullable = True)
    contact_group_prefix = db.Column(db.String, nullable = True)
    selected_cal = db.Column(db.String, nullable=True) #by etag? 
    contacts = db.relationship("Contact", back_populates = "user")
    tiers = db.relationship("Tier", back_populates = "user")

    def __repr__(self):
        return f'<User user_id = {self.user_id} email = {self.email}>'
    

class Contact(db.Model):
    """A contact."""

    __tablename__ = "contacts"

    contact_id = db.Column(db.Integer, 
                        autoincrement = True,
                        primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    fname = db.Column(db.String) #review which attributes should be nullable (default to false)
    lname = db.Column(db.String)

    occasions = db.relationship("Occasion", back_populates = "contact")
    user = db.relationship("User", back_populates = "contacts")

    def __repr__(self):
        return f'<Contact contact_id = {self.contact_id} name = {self.fname} {self.lname}>'
    
class Occasion(db.Model):
    """An occasion."""

    __tablename__ = "occasions"

    occasion_id = db.Column(db.Integer, 
                        autoincrement = True,
                        primary_key = True)
    contact_id = db.Column(db.Integer, 
                        db.ForeignKey("contacts.contact_id")) 
    occasion_type = db.Column(db.String)
    recurring = db.Column(db.Boolean)
    tier_id = db.Column(db.Integer,
                     db.ForeignKey("tiers.tier_id"), nullable = True) 
    date = db.Column(db.DateTime)

    contact = db.relationship("Contact", back_populates = "occasions")
    tier = db.relationship("Tier", back_populates = "occasions")

    def __repr__(self):
        return f'<Occasion occasion_id = {self.occasion_id} type = {self.occasion_type}>'
    
class Tier(db.Model):
    """A tier."""

    __tablename__ = "tiers"

    tier_id = db.Column(db.Integer, 
                        autoincrement = True,
                        primary_key = True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.user_id"))
    name = db.Column(db.String)
    description = db.Column(db.String)
    reminder_days_ahead = db.Column(db.Integer)
    reminder_type = db.Column(db.String)
    contact_group_id = db.Column(db.String)
    contact_group_status = db.Column(db.String)

    user = db.relationship("User", back_populates = "tiers")
    occasions = db.relationship("Occasion", back_populates = "tier")

    def __repr__(self):
        return f'<Tier tier_id = {self.tier_id} name = {self.name}>'
    
def connect_to_db(flask_app, db_uri="postgresql:///occasiondb", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app
    connect_to_db(app)
    app.app_context().push()