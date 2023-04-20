"""CRUD operations."""

from model import db, User, Contact, Occasion, Tier, connect_to_db

def create_user(email, fname, lname):
    """Create and return a new user."""

    user = User(email = email, fname = fname, lname = lname)
    return user

def get_user_by_email(email):
    """Retrieve user by email"""
    return User.query.filter(User.email == email).first()

def get_user_by_id(id):
    """Retrieve user by email"""
    return User.query.get(id)

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

def get_contacts():
    """Return all contacts."""
    return Contact.query.all()

if __name__ == '__main__':
    from server import app
    connect_to_db(app)