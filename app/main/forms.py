from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Regexp

class GroupIdsForm(FlaskForm):

    group_id1 = StringField('Group ID', validators=[DataRequired(), Regexp('^[0-9]+$', message='Only numbers')])
    group_id2 = StringField('Group ID', validators=[DataRequired(), Regexp('^[0-9]+$', message='Only numbers')])
    group_id3 = StringField('Group ID', validators=[DataRequired(), Regexp('^[0-9]+$', message='Only numbers')])
    group_id4 = StringField('Group ID', validators=[DataRequired(), Regexp('^[0-9]+$', message='Only numbers')])
    group_id5 = StringField('Group ID', validators=[DataRequired(), Regexp('^[0-9]+$', message='Only numbers')])
    group_id6 = StringField('Group ID', validators=[DataRequired(), Regexp('^[0-9]+$', message='Only numbers')])
    submit = SubmitField('Go')
