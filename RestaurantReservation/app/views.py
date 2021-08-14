  
import datetime
import sys

from app import app, db
from flask import render_template, flash, redirect, session, g, request, jsonify,url_for,session

from .forms import ReservationForm, ShowReservationsOnDateForm, AddTableForm
from .controller import create_reservation
from .models import Mesa, Reservacion, User
from flask_login import (
    UserMixin,
    LoginManager,
    login_manager,
    login_user,
    login_required,
    logout_user,
    current_user,
)


# Time Display: book table in fixed hours when the restaurant operates.
RESTAURANT_OPEN_TIME = 10
RESTAURANT_CLOSE_TIME = 22


login_manager = LoginManager()
login_manager.login_view = "/users/login"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title="Reservacion para un restaurante")

@app.route('/users/create', methods=['POST','GET'])
def create_user():
    error1= False
    error2 = False
    error3 = False
    error = False
    response={}
    try:
        username = request.get_json()['user']#simula json.loads
        name = request.get_json()['nombres']
        lastname = request.get_json()['apellidos']
        email = request.get_json()['email']
        password = request.get_json()['password']

        user_data = User.query.filter_by(username=username).first()
        user_email = User.query.filter_by(email=email).first()
        
        
        #Determinando errores
        if(len(username)==0 or len(password)==0 or len(email)==0 or len(username)>20 or len(password)>8):
            raise Exception
        if (user_data is not None) or (user_email is not None):
            raise Exception
        #Determinando errores

        usuarios = User(username=username,name=name,lastname=lastname, email=email,password=password)
        db.session.add(usuarios)
        db.session.commit()

        response['user'] = usuarios.username
        response['nombres'] = usuarios.name
        response['apellidos'] = usuarios.email
        response['email'] = usuarios.email
        response['password'] = usuarios.password
        response['nombres']=usuarios.nombres
        response['apellidos']=usuarios.apellidos
    except Exception:
        if(len(username)==0):
            error1= True
            response['error_message1']= "Ingrese un usuario"
        if(len(password)==0):
            error2= True
            response['error_message2']= "Ingrese una contraseña"
        if(len(email)==0):
            error3= True
            response['error_message3']= "Ingrese un correo válido"
        
        if(len(username)>20):
            error1= True
            response['error_message1']= "El nombre del usuario debe tener un máximo de 20 caracteres"
        if(len(password)>8):
            error2 = True
            response['error_message2']= "La contraseña debe tener un máximo de 8 caracteres"

        if (user_data is not None) or (user_email is not None):
            error = True
            response['error_message'] = "El usuario o correo ya existe. Inicie sesion"

        print(sys.exc_info())
        db.session.rollback()
    finally:
        db.session.close()        

    response['error1'] = error1
    response['error2'] = error2
    response['error3'] = error3
    response['error'] = error
    return jsonify(response)


@app.route('/users/login', methods=['POST','GET'])
def login_user():
    exist = True
    response={}
    try:
        username = request.get_json()['user']
        password = request.get_json()['password']
        user_data = User.query.filter_by(username=username).first()   
        session['username']=username
        if user_data is None:
            raise Exception
        elif not (password==user_data.password):
            raise Exception
    except Exception:
        exist = False
    finally:
        db.session.close()
    if not exist:
        response['error_message']= "Usuario o contraseña incorrecta"
    
    
    response['exist'] = exist
    return jsonify(response)    


@app.route("/registration", methods=['GET', 'POST'])
def registration():
    return render_template("registration.html") 


@app.route("/login", methods=['GET', 'POST'])
def login():
    return render_template("login.html")




@app.route('/users/reservation_status', methods=['GET', 'POST'])
def reservation():
    response={}
    error=False
    
    try:
        usuario = session['username']   
        
        celular = request.get_json()['celular']

        num_person = request.get_json()['numberperson']

        objmesa = Mesa.query.filter_by(capacidad=num_person).filter_by(ocupado="NO").first()
        
        mesa_id = objmesa.id

        objmesa.ocupado="SI"

        date_reserv = request.get_json()['date']

        #Determinando errores
        if objmesa is None:
            raise Exception

        #Determinando errores

        reservaciones = Reservacion(usuario=usuario,celular=celular,mesa_id=mesa_id,num_personas=num_person,hora_reservacion=date_reserv)
        db.session.add(reservaciones)
        db.session.commit()
        response['error_message']="Reservación exitosa"

    except Exception:
        error=True
        if objmesa is None:
            response['error_message']='No hay mesas disponibles'
        if date_reserv < datetime.datetime.now():
            response['error_message']='Horario no permitido'
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()

    response['error']=error
    return jsonify(response)

@app.route("/reservation_status", methods=['GET', 'POST'])
def reservacion_user():
    return render_template("reservation_status.html") 


@app.route('/show_tables', methods=['GET', 'POST'])
def show_tables():
    form = AddTableForm()

    if form.validate_on_submit():
        mesa = Mesa(capacidad=int(form.mesa_capacidad.data))
        db.session.add(mesa)
        db.session.commit()
        flash("La mesa ha sido creada!")
        return redirect('/show_tables')

    mesas = Mesa.query.all()
    return render_template('show_tables.html', title="Mesas", mesas=mesas, form=form)



@app.route('/admin')
def admin():
    return render_template('admin.html', title="Admin")