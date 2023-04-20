"""CRUD operations."""

from model import db, User, Contact, Occasion, Tier, connect_to_db

def create_user(email, password):
    """Create and return a new user."""

    user = User(email = email, password = password)
    return user

    #user by email 

def create_contact(user, fname, lname):
    """Create and return a new contact."""

    contact = Contact(user = user, fname = fname, lname = lname)
    return contact

def create_occasion(contact, occasion_type, recurring, tier, date):
    """Create and return a new occasion."""
    occasion = Occasion(contact = contact, 
                        occasion_type = occasion_type,
                        recurring = recurring,
                        tier = tier,
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

if __name__ == '__main__':
    from server import app
    connect_to_db(app)