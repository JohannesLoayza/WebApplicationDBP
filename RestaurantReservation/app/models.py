  
from app import db
from datetime import datetime
from sqlalchemy.sql import expression

DEFAULT_RESERVATION_LENGTH = 2 # 2 horas
MAX_TABLE_CAPACITY = 8 # 8 personas

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(20),nullable=False)
    lastname=db.Column(db.String(20),nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(8),nullable=False)
    reservaciones = db.relationship('Reservacion', backref='user_reservacion',lazy='dynamic')

    def __repr__(self):
        return f'<User: {self.id},{self.username},{self.name},{self.lastname},{self.email},{self.password}>'
    
class Mesa(db.Model):
    __tablename__ = 'mesa'
    id = db.Column(db.Integer, primary_key=True)
    capacidad = db.Column(db.Integer, index=True)
    ocupado = db.Column(db.String(2), default='NO', nullable=False)
    reser_mesa = db.relationship('Reservacion', backref='mesaid',lazy='joined')
    def __repr__(self):
        return f'<Mesa: {self.id},{self.capacidad},{self.ocupado}>'

class Reservacion(db.Model):
    __tablename__ = 'reservacion'
    id = db.Column(db.Integer, primary_key=True)
    usuario= db.Column(db.String(20), db.ForeignKey('users.username'))
    celular = db.Column(db.String(9),nullable=False)
    mesa_id = db.Column(db.Integer, db.ForeignKey('mesa.id'))
    num_personas = db.Column(db.Integer, index=True)
    hora_reservacion = db.Column(db.DateTime, index=True)
    
    def __repr__(self):
        return f'<Reservacion: {self.id}, {self.user_id},{self.mesa_id},{self.num_personas},{self.hora_reservacion}>'

db.create_all()