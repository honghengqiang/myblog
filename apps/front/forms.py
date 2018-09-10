from wtforms import Form, FileField, StringField
from wtforms.validators import InputRequired
from flask_wtf.file import FileAllowed, FileRequired


class UpLoadForm(Form):
    avatar = FileField(validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg', 'gif'])])
    # desc = StringField(validators=[InputRequired()])
