"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

os.system("dropdb occasiondb")
os.system("createdb occasiondb")

model.connect_to_db(server.app)
server.app.app_context().push()
model.db.create_all()


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