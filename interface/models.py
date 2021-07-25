from interface import db

class state(db.Model):
    STATE_ID = db.Column(db.Integer, primary_key = True)
    CHANNEL_ID = db.Column(db.Integer)
    CURRENT_STATE = db.Column(db.Integer)
    CREATE_DATE = db.Column(db.DateTime)
    UPDATE_DATE = db.Column(db.DateTime)

class user(db.Model):
    USER_ID = db.Column(db.Integer, primary_key = True)
    CHANNEL_ID = db.Column(db.Integer)
    HASH_ID = db.Column(db.String)
    USER_NAME = db.Column(db.String)
    CREATE_DATE = db.Column(db.DateTime)
    UPDATE_DATE = db.Column(db.DateTime)

class input(db.Model):
    INPUT_ID = db.Column(db.Integer, primary_key = True)
    HASH_ID = db.Column(db.String)
    USER_INPUT = db.Column(db.String)
    CORRECT_INPUT = db.Column(db.Integer)
    CREATE_DATE = db.Column(db.DateTime)

class ban(db.Model):
    BAN_ID = db.Column(db.Integer, primary_key = True)
    HASH_ID = db.Column(db.String)
    BAN_DATE = db.Column(db.DateTime)
    UNBAN_DATE = db.Column(db.DateTime)
    INDEFINITE_BAN = db.Column(db.Integer)
    CURRENTLY_BANNED = db.Column(db.Integer)
    CREATE_DATE = db.Column(db.DateTime)
    UPDATE_DATE = db.Column(db.DateTime)

class insult(db.Model):
    INSULT_ID = db.Column(db.Integer, primary_key = True)
    INSULT_TEXT = db.Column(db.String)
    INSULT_FILE = db.Column(db.String)
    USER_REFERENCED = db.Column(db.Integer)
    ACTIVE = db.Column(db.Integer)
    INDEFINITE_BAN = db.Column(db.Integer)
    CREATE_DATE = db.Column(db.DateTime)
    UPDATE_DATE = db.Column(db.DateTime)
