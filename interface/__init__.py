from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'e4fd2314b7d8e52744874483bb147046'
db = SQLAlchemy(app)

from interface import routes

if __name__ == "__main__":
  app.run(host='0.0.0.0')
