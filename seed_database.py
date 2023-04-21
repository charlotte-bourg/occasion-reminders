"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

#os.system("dropdb occasiondb")
#os.system("createdb occasiondb")

model.connect_to_db(server.app)
server.app.app_context().push()
#model.db.create_all()

#just seeding tiers for now for testing
user = crud.get_user_by_email("hackbright.charlotte@gmail.com")
tier1 = crud.create_tier(user, "Far away besties' bdays", "need 3 weeks to find and ship a gift!!",21,"push","tbd")
tier2 = crud.create_tier(user, "Non materialistic homies' bdays", "Gifting is not everyone's love language <3",7,"push","tbd")
tier3 = crud.create_tier(user, "Abroad????", "How am I supposed to get something to the Netherlands...",28,"push","tbd")
tier4 = crud.create_tier(user, "Call me beep me", "",1,"email","tbd")
tier4 = crud.create_tier(user, "Party planning committee", "start thinkin!",30,"email","tbd")
model.db.session.add(tier1)
model.db.session.add(tier2)
model.db.session.add(tier3)
model.db.session.add(tier4)
model.db.session.commit()
#user = crud.create_user("hackbright.charlotte@gmail.com","test")
#model.db.session.add(user)
#tier = crud.create_tier(user, "bday_3weeks", "enough time to buy a gift!", 21, "push",123)
#model.db.session.add(tier)
#contact = crud.create_contact(user, "Jane", "Doe")
#model.db.session.add(contact)
#birthday = datetime(year = 1990, month = 12, day = 1)
#occasion = crud.create_occasion(contact, "birthday", True, tier, birthday)
#model.db.session.add(occasion)

#model.db.session.commit()