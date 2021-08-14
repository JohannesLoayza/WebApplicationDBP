from flask_wtf import Form
from flask_wtf import FlaskForm as BaseForm #
from wtforms import StringField, DateTimeField, IntegerField, DateField, SelectField
from wtforms.validators import DataRequired
from .models import MAX_TABLE_CAPACITY

from datetime import datetime


class ReservationForm(Form):
    nombre_persona = StringField('nombre_persona', validators=[DataRequired()])
    telefono_persona = StringField('telefono_persona', validators=[DataRequired()])
    num_personas = SelectField('num_personas', coerce=int, choices = [(x, x) for x in range(1, MAX_TABLE_CAPACITY)])
    reservacion_datetime = DateTimeField('reservacion_datetime', default=datetime.now(),
                                         validators=[DataRequired()])

class ShowReservationsOnDateForm(Form):
    fecha_reservacion = DateField('fecha_reservacion', default=datetime.now())

class AddTableForm(Form):
    capacidad_mesa = SelectField('capacidad_mesa', coerce=int, choices = [(x, x) for x in range(1, MAX_TABLE_CAPACITY)])