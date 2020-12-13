from flask_wtf import FlaskForm
from flask_wtf import Form
from wtforms import StringField, TextField, SubmitField, IntegerField,TextAreaField,RadioField,SelectField, DecimalField
from wtforms.validators import DataRequired
from wtforms.validators import Length
from wtforms.validators import ValidationError

class PredictForm(FlaskForm):
	Pregnancies = IntegerField('Pregnancies')
	Glucose = IntegerField('Glucose')
	BloodPressure = IntegerField('BloodPressure')
	SkinThickness = IntegerField('SkinThickness')
	Insulin = IntegerField('Insulin')
	BMI = DecimalField('BMI')
	DiabetesPedigreeFunction = DecimalField('DiabetesPedigreeFunction')
	Age = IntegerField('Age')
	submit = SubmitField('Predict')
	abc = "" 