"""CRUD operations."""

from model import db, User, Contact, Occasion, Tier, connect_to_db

def create_user(email, fname, lname):
    """Create and return a new user."""

    user = User(email = email, fname = fname, lname = lname)
    return user

def create_contact(user, fname, lname):
    """Create and return a new contact."""

    contact = Contact(user = user, fname = fname, lname = lname)
    return contact

def create_occasion(contact, occasion_type, recurring, date):
    """Create and return a new occasion."""
    occasion = Occasion(contact = contact, 
                        occasion_type = occasion_type,
                        recurring = recurring,
                        date = date)
    return occasion

def create_tier(user, name, description, reminder_days_ahead, reminder_type, contact_group_id):
    """Create and return a new tier."""
    tier = Tier(user = user,
                name = name,
                description = description,
                reminder_days_ahead = reminder_days_ahead,
                reminder_type = reminder_type,
                contact_group_id = contact_group_id)
    return tier

def get_user_by_email(email):
    """Retrieve user by email."""
    return User.query.filter(User.email == email).first()

def get_user_by_id(id):
    """Retrieve user by email."""
    return User.query.get(id)

def user_has_local_contacts(user):
    """Return boolean value for whether user has any contacts in application database."""
    return bool(Contact.query.filter(Contact.user == user).first())

def get_contacts_by_user(user):
    """Return all of a user's contacts."""
    return Contact.query.filter(Contact.user == user).all()

def get_occasions_by_user(user):
    """Return all of a user's occasions."""
    return db.session.query(Occasion).join(Contact).filter(Contact.user == user).all()

def get_occasions_by_tier(tier_id):
    """Return all occasions with a given tier."""
    #return db.session.query(Occasion).join(Contact).filter(Contact.user == user).all()
    return Occasion.query.filter(Occasion.tier_id == tier_id).all()

def get_tiered_occasions_by_user(user):
    """Return all of a user's occasions that have tiers."""
    return db.session.query(Occasion).join(Contact).filter(Contact.user == user, Occasion.tier != None).all()

def occasions_with_tier(tier_id):
    return bool(Occasion.query.filter(Occasion.tier_id == tier_id).first())

def get_tier_by_id(tier_id):
    """Return tier."""
    return Tier.query.get(tier_id)

def update_tier(occasion_id, tier_id):
    """Update tier value on an occasion."""
    occasion = Occasion.query.get(occasion_id)
    occasion.tier_id = tier_id

def delete_tier(tier_id):
    """Delete a tier and references to it from the database.""" #consider changing to soft delete
    

if __name__ == '__main__':
    from server import app
    connect_to_db(app)
    app.app_context().push()