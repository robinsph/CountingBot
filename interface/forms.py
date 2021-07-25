from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField, TextAreaField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, NoneOf
from interface.models import insult

class InsultForm(FlaskForm):
    INSULT_TEXT = TextAreaField('Insult Text', render_kw={"placeholder": ""})

    SUBMIT = SubmitField('Submit')