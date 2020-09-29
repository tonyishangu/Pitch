from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField, SelectField
from wtforms.validators import Required

class PitchForm(FlaskForm):

    title = StringField('Pitch title',validators=[Required()])
    category = SelectField('Pitch category', choices=[('Motivational', 'Motivational'), ('Famous', 'Famous'), ('Despair', 'Despair')], validators=[Required()])
    description = TextAreaField('Pitch description', validators=[Required()])
    submit = SubmitField('Submit')

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')

class Commentform(FlaskForm):
    description = TextAreaField('Comment description', validators=[Required()])
    submit = SubmitField('Submit')

class Upvoteform(FlaskForm):
    submit1 = SubmitField('Upvote (+)')

class Downvoteform(FlaskForm):
    submit2 = SubmitField('Downvote (-)')