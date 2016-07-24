from flask_wtf import Form
from wtforms import TextField, BooleanField, SelectField, TextAreaField
from wtforms.validators import Required, Length
from scrimme.consts import CHOICES_SKILLS, CHOICES_CLASSES, CHOICES_ZONES

class EditUserForm(Form):
    skill_level = SelectField('skill_level', choices=CHOICES_SKILLS)
    main_class  = SelectField('main_class', choices=CHOICES_CLASSES)
    is_merc = BooleanField(label='I am a merc')
    is_mentor = BooleanField(label='I am a mentor')
    region = SelectField('region', choices=CHOICES_ZONES)
