from flask_wtf import Form
from wtforms import StringField, PasswordField, IntegerField, DecimalField
from wtforms.validators import DataRequired, Email

class AddIncidentForm(Form):
	#date = DateField('Date',format='%Y-%m-%d')
	description = StringField('Description', validators=[DataRequired()])
	latitude = DecimalField('Latitude', places=2, rounding=None, validators=[DataRequired()])
	longitude = DecimalField('Longitude', places=2, rounding=None, validators=[DataRequired()])
   