from flask import Flask, render_template, request, session, Response, flash, redirect, url_for, send_from_directory, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_mail import Mail, Message
from flask_wtf.csrf import CSRFProtect  
from functools import wraps
import hashlib
from datetime import datetime
import pandas as pd
from pandas_profiling import ProfileReport
import ydata_profiling
import xml.etree.ElementTree as ET
import tempfile
from flask_principal import Principal, Permission, RoleNeed, identity_loaded, UserNeed, Identity, AnonymousIdentity, identity_changed
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import logging
from logging.handlers import RotatingFileHandler
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from flask_migrate import Migrate
from datetime import datetime
from decimal import Decimal
from sqlalchemy.orm import joinedload


app = Flask(__name__, template_folder='templates')
app.secret_key = os.getenv('SECRET_KEY', '876-105-169')

# Obtener y corregir la URL de la base de datos
database_url = os.environ.get('DATABASE_URL')
if database_url and database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#configuración de las cookies 
app.config['SESSION_COOKIE_SECURE'] = True  # Usar solo en producción con HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Inicializaciones de Flask-Principal y Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'
principals = Principal(app)

#Definir los roles de administrador.
admin_permission = Permission(RoleNeed('admin'))
consulta_permission = Permission(RoleNeed('consulta'))

db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)


#Para envio de Correos 

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'farfanjaime05@gmail.com'
app.config['MAIL_PASSWORD'] = 'olgr ogmu tavn rfue'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


# proteccion en los formularios
csrf = CSRFProtect(app)


#Crear un directorio de los logs

if not os.path.exists('logs'):
    os.mkdir('logs')


#Manejador  de archivos

file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))

# Configurar el nivel de logging y añadir el manejador a la aplicación Flask
file_handler.setLevel(logging.INFO)

app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)
app.logger.info('Aplicación iniciada')

# Login
class signup(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(40), unique=True)
    correo = db.Column(db.String(70))
    usuario = db.Column(db.String(40), unique=True)
    contrasena = db.Column(db.String(40))
    role = db.Column(db.String(50))

    def __init__(self, nombre, correo, usuario, contrasena, role):
        self.nombre = nombre
        self.correo = correo
        self.usuario = usuario
        self.contrasena = contrasena
        self.role = role


class TaskSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nombre', 'correo', 'usuario', 'contrasena', 'role')


task_schema = TaskSchema()
task_schema = TaskSchema(many=True)


# Pacientes
class paciente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    documento = db.Column(db.Integer, unique=True, nullable=False)
    tipo = db.Column(db.String(10))
    nombre_paciente = db.Column(db.String(200))
    edad = db.Column(db.Integer)
    genero = db.Column(db.String(50))
    correo_electronico = db.Column(db.String(255))
    direccion = db.Column(db.Text)
    telefono = db.Column(db.String(40))
    eps = db.Column(db.String(50))
    cargo = db.Column(db.String(100))
    acompanante = db.Column(db.String(100), default='Sin acompañante')
    parentesco = db.Column(db.String(60))
    telefono_acompanante = db.Column(db.String(50))

    def __init__(self, documento=None, tipo=None, nombre_paciente=None, edad=None, genero=None, correo_electronico=None, direccion=None, telefono=None, eps=None, cargo=None, acompanante=None, parentesco=None, telefono_acompanante=None):
        self.documento = documento
        self.tipo = tipo
        self.nombre_paciente = nombre_paciente
        self.edad = edad
        self.genero = genero
        self.correo_electronico = correo_electronico
        self.direccion = direccion
        self.telefono = telefono
        self.eps = eps
        self.cargo = cargo
        self.acompanante = acompanante
        self.parentesco = parentesco
        self.telefono_acompanante = telefono_acompanante


class TaskSchema(ma.Schema):
    class Meta:
        fields = ('documento', 'tipo', 'nombre_paciente', 'edad', 'genero', 'correo_electronico',
                  'direccion', 'telefono', 'eps', 'cargo', 'acompanante', 'parentesco', 'telefono_acompanante')


task_schema = TaskSchema()
task_schema = TaskSchema(many=True)

# Antecedentes


class antecedentes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    diabetes = db.Column(db.String(20))
    hipertension = db.Column(db.String(20))
    artritis = db.Column(db.String(20))
    alergia = db.Column(db.String(20))
    catarata = db.Column(db.String(20))
    glaucoma = db.Column(db.String(20))
    estrabismo = db.Column(db.String(20))
    queratocono = db.Column(db.String(20))
    otros = db.Column(db.String(50))
    diabetes_per = db.Column(db.String(20))
    hipertension_per = db.Column(db.String(20))
    Artritis_per = db.Column(db.String(20))
    Alergia_per = db.Column(db.String(20))
    ulcera_per = db.Column(db.String(20))
    cirugia_per = db.Column(db.String(20))
    lentes_contacto_per = db.Column(db.String(20))
    otros1 = db.Column(db.String(20))
    descripcion = db.Column(db.String(80))
    paciente_documento = db.Column(db.Integer, db.ForeignKey(
        'paciente.documento', onupdate='CASCADE', ondelete='CASCADE'))

    paciente = db.relationship(
        'paciente', backref=db.backref('antecedentes', lazy=True))

    def __init__(self, diabetes=None, hipertension=None, artritis=None, alergia=None, catarata=None, glaucoma=None, estrabismo=None, queratocono=None, otros=None, diabetes_per=None, hipertension_per=None, Artritis_per=None, Alergia_per=None, ulcera_per=None, cirugia_per=None, lentes_contacto_per=None, otros1=None, descripcion=None):
        self.diabetes = diabetes
        self.hipertension = hipertension
        self.artritis = artritis
        self.alergia = alergia
        self.catarata = catarata
        self.glaucoma = glaucoma
        self.estrabismo = estrabismo
        self.queratocono = queratocono
        self.otros = otros
        self.diabetes_per = diabetes_per
        self.hipertension_per = hipertension_per
        self.Artritis_per = Artritis_per
        self.Alergia_per = Alergia_per
        self.ulcera_per = ulcera_per
        self.cirugia_per = cirugia_per
        self.lentes_contacto_per = lentes_contacto_per
        self.otros1 = otros1
        self.descripcion = descripcion


class TaskSchema(ma.Schema):
    class Meta:
        fields = ('diabetes', 'hipertension', 'artritis', 'alergia', 'catarata', 'glaucoma', 'estrabismo', 'queratocono', 'otros',
                  'diabetes_per', 'hipertension_per', 'Artritis_per', 'ulcera_per', 'cirugia_per', 'lentes_contacto_per', 'otros1',
                  'descripcion')


task_schema = TaskSchema()
task_schema = TaskSchema(many=True)


# Motivo de Consulta


class MovConsulta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mov_consulta = db.Column(db.String(200))
    ulti_consulta = db.Column(db.String(100))
    vlsc_od = db.Column(db.String(50))
    vlsc_oi = db.Column(db.String(50))
    vlsc_ao = db.Column(db.String(50))
    vlsc_PH = db.Column(db.String(50))
    vpsc_od = db.Column(db.String(50))
    vpsc_oi = db.Column(db.String(50))
    vpsc_ao = db.Column(db.String(50))
    vpsc_PH = db.Column(db.String(50))
    vlcc_od = db.Column(db.String(50))
    vlcc_oi = db.Column(db.String(50))
    vlcc_ao = db.Column(db.String(50))
    vlcc_PH = db.Column(db.String(50))
    vpcc_od = db.Column(db.String(50))
    vpcc_oi = db.Column(db.String(50))
    vpcc_ao = db.Column(db.String(50))
    vpcc_PH = db.Column(db.String(50))
    lensometria_od = db.Column(db.String(50))
    lensometria_oi = db.Column(db.String(50))
    lensometria_add = db.Column(db.String(50))
    lensometria_tipo_lente = db.Column(db.String(50))
    examen_externo = db.Column(db.String(300))
    examen_ppc = db.Column(db.String(50))
    examen_ducciones =  db.Column(db.String(50))
    examen_cover_test =  db.Column(db.String(50))
    paciente_documento = db.Column(db.Integer, db.ForeignKey(
        'paciente.documento', onupdate='CASCADE', ondelete='CASCADE'))
    paciente = db.relationship(
        'paciente', backref=db.backref('MovConsulta', lazy=True))

    def __init__(self, mov_consulta=None, ulti_consulta=None, vlsc_od=None, vlsc_oi=None, vlsc_ao=None,
                 vlsc_PH=None, vpsc_od=None, vpsc_oi=None, vpsc_ao=None, vpsc_PH=None,vlcc_od=None, vlcc_oi=None, vlcc_ao=None,
                 vlcc_PH=None, vpcc_od=None, vpcc_oi=None, vpcc_ao=None, vpcc_PH=None, lensometria_od = None, 
                  lensometria_oi = None, lensometria_add =None,lensometria_tipo_lente =None, examen_externo=None,
                  examen_ppc = None,examen_ducciones= None, examen_cover_test= None,):
        
        self.mov_consulta = mov_consulta
        self.ulti_consulta = ulti_consulta
        self.vlsc_od = vlsc_od
        self.vlsc_oi = vlsc_oi
        self.vlsc_ao = vlsc_ao
        self.vlsc_PH = vlsc_PH
        self.vpsc_od = vpsc_od
        self.vpsc_oi = vpsc_oi
        self.vpsc_ao = vpsc_ao
        self.vpsc_PH = vpsc_PH
        self.vlcc_od = vlcc_od
        self.vlcc_oi = vlcc_oi
        self.vlcc_ao = vlcc_ao
        self.vlcc_PH = vlcc_PH
        self.vpcc_od = vpcc_od
        self.vpcc_oi = vpcc_oi
        self.vpcc_ao = vpcc_ao
        self.vpcc_PH = vpcc_PH
        self.lensometria_od = lensometria_od
        self.lensometria_oi = lensometria_oi
        self.lensometria_add = lensometria_add
        self.lensometria_tipo_lente = lensometria_tipo_lente
        self.examen_externo = examen_externo
        examen_ppc = examen_ppc
        examen_ducciones = examen_ducciones
        examen_cover_test=examen_cover_test

class TaskSchema(ma.Schema):
    class Meta:
        fields = ('mov_consulta', 'ulti_consulta', 'vlsc_od', 'vlsc_oi', 'vlsc_ao', 'vlsc_PH', 'vpsc_od',
                  'vpsc_oi', 'vpsc_ao', 'vpsc_PH','vlcc_od', 'vlcc_oi', 'vlcc_ao', 'vlcc_PH', 'vpcc_od',
                  'vpcc_oi', 'vpcc_ao', 'vpcc_PH', 'lensometria_od','lensometria_oi','lensometria_add',
                   'lensometria_tipo_lente','examen_externo', 'examen_ppc', 'examen_ducciones','examen_cover_test')

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

# vista

class Vista(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    OFTALMOSCOPIA_ojo_derecho = db.Column(db.String(50))
    OFTALMOSCOPIA_ojo_izquierdo = db.Column(db.String(50))
    ojo_drc_querato = db.Column(db.String(30))
    ojo_izq_querato = db.Column(db.String(30))
    esfera_retino = db.Column(db.String(30))
    cilindro_retino = db.Column(db.String(30))
    eje_retino = db.Column(db.String(30))
    dp_retino = db.Column(db.String(30))
    vl20_retino = db.Column(db.String(30))
    vp20_retino = db.Column(db.String(30))
    add_retino = db.Column(db.String(30))
    esfera_retino_1 = db.Column(db.String(30))
    cilindro_retino_1 = db.Column(db.String(30))
    eje_retino_1 = db.Column(db.String(30))
    dp_retino_1 = db.Column(db.String(30))
    vl20_retino_1 = db.Column(db.String(30))
    vp20_retino_1 = db.Column(db.String(30))
    add_retino_1 = db.Column(db.String(30))
    esfera = db.Column(db.String(50))
    cilindro = db.Column(db.String(50))
    eje = db.Column(db.String(50))
    dp = db.Column(db.String(50))
    vl20 = db.Column(db.String(50))
    vp20 = db.Column(db.String(50))
    add_0 = db.Column(db.String(50))
    esfera_1 = db.Column(db.String(50))
    cilindro_1 = db.Column(db.String(50))
    eje_1 = db.Column(db.String(50))
    dp_1 = db.Column(db.String(50))
    vl20_1 = db.Column(db.String(50))
    vp20_1 = db.Column(db.String(50))
    add_1 = db.Column(db.String(50))
    recomendación = db.Column(db.String(300))
    diagnostico = db.Column(db.String(300))
    observación = db.Column(db.String(300))
    tipo_lente = db.Column(db.String(50))
    montura = db.Column(db.String(50))
    material = db.Column(db.String(50))
    filtro = db.Column(db.String(50))
    color = db.Column(db.String(50))
    observacion = db.Column(db.String(100))
    paciente_documento = db.Column(db.Integer, db.ForeignKey(
        'paciente.documento', onupdate='CASCADE', ondelete='CASCADE'))

    paciente = db.relationship(
        'paciente', backref=db.backref('vista', lazy=True))

    def __init__(self, OFTALMOSCOPIA_ojo_derecho=None, OFTALMOSCOPIA_ojo_izquierdo=None, ojo_drc_querato=None, ojo_izq_querato=None,
                 esfera_retino=None, cilindro_retino=None, eje_retino=None, dp_retino=None, vl20_retino=None, vp20_retino=None,
                 add_retino=None, esfera_retino_1=None, cilindro_retino_1=None, eje_retino_1=None, dp_retino_1=None, vl20_retino_1=None,
                 vp20_retino_1=None, add_retino_1=None, esfera=None, cilindro=None,  eje=None, dp=None, vl20=None, vp20=None,
                 add_0=None, esfera_1=None, cilindro_1=None,  eje_1=None, dp_1=None, vl20_1=None, vp20_1=None,
                 add_1=None, recomendación=None, diagnostico=None, observación=None, tipo_lente=None, montura=None,  material=None,
                 filtro=None, color=None, observacion=None):

        self.OFTALMOSCOPIA_ojo_derecho = OFTALMOSCOPIA_ojo_derecho
        self.OFTALMOSCOPIA_ojo_izquierdo = OFTALMOSCOPIA_ojo_izquierdo
        self.ojo_drc_querato = ojo_drc_querato
        self.ojo_izq_querato = ojo_izq_querato
        self.esfera_retino = esfera_retino
        self.cilindro_retino = cilindro_retino
        self.eje_retino = eje_retino
        self.dp_retino = dp_retino
        self.vl20_retino = vl20_retino
        self.vp20_retino = vp20_retino
        self.add_retino = add_retino
        self.esfera_retino_1 = esfera_retino_1
        self.cilindro_retino_1 = cilindro_retino_1
        self.eje_retino_1 = eje_retino_1
        self.dp_retino_1 = dp_retino_1
        self.vl20_retino_1 = vl20_retino_1
        self.vp20_retino_1 = vp20_retino_1
        self.add_retino_1 = add_retino_1
        self.esfera = esfera
        self.cilindro = cilindro
        self.eje = eje
        self.dp = dp
        self.vl20 = vl20
        self.vp20 = vp20
        self.add_0 = add_0
        self.esfera_1 = esfera_1
        self.cilindro_1 = cilindro_1
        self.eje_1 = eje_1
        self.dp_1 = dp_1
        self.vl20_1 = vl20_1
        self.vp20_1 = vp20_1
        self.add_1 = add_1
        self.recomendación = recomendación
        self.diagnostico = diagnostico
        self.observación = observación
        self.tipo_lente = tipo_lente
        self.montura = montura
        self.material = material
        self.filtro = filtro
        self.color = color
        self.observacion = observacion


class TaskSchema(ma.Schema):
    class Meta:
        flieds = ('OFTALMOSCOPIA_ojo_derecho', 'OFTALMOSCOPIA_ojo_izquierdo', 'ojo_drc_querato', 'ojo_izq_querato', 'esfera_retino', 'cilindro_retino', 'eje_retino',
                  'dp_retino', 'vl20_retino', 'vp20_retino', 'add_retino', 'esfera_retino_1', 'cilindro_retino_1', 'eje_retino_1', 'dp_retino_1', 'vl20_retino_1',
                  'vp20_retino_1', 'add_retino_1', 'esfera', 'cilindro', 'eje', 'dp', 'vl20', 'vp20', 'add_0', 'esfera_1', 'cilindro_1', 'eje_1', 'dp_1', 'vl20_1', 'vp20_1', 'add_1',
                  'recomendación', 'diagnostico', 'observación', 'tipo_lente', 'montura', 'material', 'filtro', 'color', 'observacion')


task_schema = TaskSchema()
task_schema = TaskSchema(many=True)

# Registro de Agendamiento de Cita Medica
class generar_cita(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    calendar = db.Column(db.DateTime)
    time = db.Column(db.Time)
    note = db.Column(db.String(500))
    paciente_documento = db.Column(db.Integer, db.ForeignKey(
        'paciente.documento', onupdate='CASCADE', ondelete='CASCADE'))
    
    def __init__(self, calendar=None, time=None, note=None, paciente_documento=None):
        self.calendar = calendar
        self.time = time
        self.note = note
        self.paciente_documento = paciente_documento

    class TaskSchema(ma.Schema):
        class Meta:
            fields = ('calendar', 'time', 'note')

# Registro de Eliminar
class delete(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    eliminado = db.Column(db.Boolean, default=False)
    fecha_eliminacion = db.Column(db.DateTime)
    nombre_eliminado = db.Column(db.String(100))
    documento_eliminado = db.Column(db.String(100))

    def __init__(self, eliminado= None, fecha_eliminacion = None, nombre_eliminado = None,documento_eliminado = None ):
        self.eliminado = eliminado 
        self.fecha_eliminacion = fecha_eliminacion
        nombre_eliminado = nombre_eliminado
        documento_eliminado = documento_eliminado

    class TaskSchema(ma.Schema):
        class Meta:
            flieds = ('eliminado', 'fecha_eliminacion',
                      'nombre_eliminado', 'documento_eliminado')

# Autenticación del usuario

def get_user_authenticated():  # se crea la funcion para la autenticación
    user_authenticated = False
    if 'user_authenticated' in session:
        user_authenticated = session['user_authenticated']
    return user_authenticated


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not get_user_authenticated():
            return render_template('login.html')
        return f(*args, **kwargs)
    return decorated_function

#Asignacion de los roles de los usuarios:

def role_required(*allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'role' not in session or session['role'] not in allowed_roles:
                flash('No tienes permiso para acceder a esta página', 'danger')
                return redirect(url_for('home'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Decoradores específicos para admin y consulta
def admin_required(f):
    return role_required('admin')(f)

def consulta_required(f):
    return role_required('consulta', 'admin')(f)


# Define la función user_loader
@login_manager.user_loader
def load_user(user_id):
    return signup.query.get(int(user_id))

@app.route("/")
@csrf.exempt
def home():
        return render_template('home.html')

@app.route("/privacy")
@csrf.exempt
def privacy():
    return render_template('privacy.html')

@app.route("/terms")
@csrf.exempt
def terms():
    return render_template('terms.html')


@app.route("/signup", methods=['GET', 'POST'])
@csrf.exempt
def signup_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        username = request.form['user']
        password = request.form['password']
        role = request.form['role']

        # Codificar la contraseña
        password_bytes = password.encode('utf-8')

        # Aplicar el modo MD5 dentro de la contraseña
        hashed_password = hashlib.md5(password_bytes).hexdigest()

        #Verificar si un usuario ya esta registrado

        existing_user = signup.query.filter((signup.usuario == username )| (signup.correo == email)).first()
        if existing_user:
            flash('El usuario o el Correo electronico ya se encuentra registrado', 'danger')
            return render_template('signup.html')
        else:
            user = signup(
                nombre=name,
                correo=email,
                usuario=username,
                contrasena=hashed_password,
                role = role

            )
            db.session.add(user)
            db.session.commit()

            msg = Message('El registro del Usuario ha sido satisfactoriamente' ,
                        sender = app.config['MAIL_PASSWORD'],
                        recipients=[user.correo])
            msg.html = render_template('email.html' , user = user.usuario )
            mail.send(msg)
            flash('Usuario registrado correctamente, Verifique su correo', 'success')
            print('El correo se envio con exito')
            return render_template('home.html')

    return render_template('signup.html')


@app.route("/login", methods=['GET', 'POST'])
@csrf.exempt
def login():
    if request.method == 'POST':
        username = request.form['user']
        password = request.form['password']

        user = signup.query.filter_by(usuario=username).first()

        if user:
            # Obtener la contraseña encriptada almacenada en la base de datos
            stored_password = user.contrasena

            # Aplicar el hashing MD5 a la contraseña ingresada - Compara la contraseñas.
            hashed_password = hashlib.md5(password.encode('utf-8')).hexdigest()

            if hashed_password == stored_password:
                session['user_authenticated'] = True
                session['usuario'] = username  # Guarda el usuario en la sesión
                session['role'] = user.role #Guarda el rol del usuario
                print('Bienvenido ' + username)
                return redirect(url_for('menu')) #Envia a menu.html
            else:
                print('Usuario o contraseña incorrectos')
                flash('Usuario o contraseña incorrectos', 'danger')
        else:
            print('Usuario o contraseña incorrectos')

    return render_template('login.html')

@app.route("/menu")
@login_required
@csrf.exempt
def menu():
    if 'user_authenticated' in session and session['user_authenticated']:
        username = session['usuario']
        return render_template('menu.html', username=username)
    else:
        return redirect(url_for('login'))
    
#Registrar un paciente

@app.route("/register", methods=['GET', 'POST'])
@csrf.exempt
@login_required
@role_required('admin')
def register():
    user_authenticated = get_user_authenticated()
    if request.method == 'POST':
        documento = request.form['document']
        tipo = request.form['tdocument']
        nombre_paciente = request.form['name']
        edad = request.form['yearold']
        genero = request.form['gender']
        correo_electronico = request.form['email']
        direccion = request.form['direcction']
        telefono = request.form['phone']
        eps = request.form['eps']
        cargo = request.form['charge']
        acompanante = request.form['companion']
        parentesco = request.form['relationship']
        telefono_acompanante = request.form['phonerelationship']

        # Antecedentes
        diabetes = request.form['dia']
        hipertension = request.form['hiper']
        artritis = request.form['artr']
        alergia = request.form['aler']
        catarata = request.form['cata']
        glaucoma = request.form['glau']
        estrabismo = request.form['estra']
        queratocono = request.form['quera']
        otros = request.form['otros']
        diabetes1 = request.form['diabetes']
        hipertension1 = request.form['hipertension']
        artritis1 = request.form['artritis']
        alergia1 = request.form['alergia']
        ulcera1 = request.form['ulcera']
        cirugia = request.form['cirugia']
        lentes = request.form['lentes']
        otros1 = request.form['otros_1']
        descripcion = request.form['descripcion']

        # Motivo de Consulta

        mov_consulta = request.form['mov_consulta']
        ulti_consulta = request.form['ulti_consulta']
        vlsc_od = request.form['vlsc_od']
        vlsc_oi = request.form['vlsc_oi']
        vlsc_ao = request.form['vlsc_ao']
        vlsc_PH = request.form['vlsc_PH']
        vpsc_od = request.form['vpsc_od']
        vpsc_oi = request.form['vpsc_oi']
        vpsc_ao = request.form['vpsc_ao']
        vpsc_PH = request.form['vpsc_PH']
        vlcc_od = request.form['vlcc_od']
        vlcc_oi = request.form['vlcc_oi']
        vlcc_ao = request.form['vlcc_ao']
        vlcc_PH = request.form['vlcc_PH']
        vpcc_od = request.form['vpcc_od']
        vpcc_oi = request.form['vpcc_oi']
        vpcc_ao = request.form['vpcc_ao']
        vpcc_PH = request.form['vpcc_PH']
        lensometria_od = request.form['lensometria_od']
        lensometria_oi = request.form['lensometria_oi']
        lensometria_add = request.form['lensometria_add']
        lensometria_tipo_lente = request.form['lensometria_tipo_lente']
        examen_externo = request.form['examen_externo']
        examen_ppc = request.form['ppc']
        examen_ducciones = request.form['ducciones']
        examen_cover_test = request.form['cover_test']

        # vista

        OFTALMOSCOPIA_ojo_derecho = request.form['OFTALMOSCOPIA_ojo_derecho']
        OFTALMOSCOPIA_ojo_izquierdo = request.form['OFTALMOSCOPIA_ojo_izquierdo']
        ojo_drc_querato = request.form['ojo_drc_querato']
        ojo_izq_querato = request.form['ojo_izq_querato']
        esfera_retino = request.form['esfera_retino']
        cilindro_retino = request.form['cilindro_retino']
        eje_retino = request.form['eje_retino']
        dp_retino = request.form['dp_retino']
        vl20_retino = request.form['vl20_retino']
        vp20_retino = request.form['vp20_retino']
        add_retino = request.form['add_retino']
        esfera_retino_1 = request.form['esfera_retino_1']
        cilindro_retino_1 = request.form['cilindro_retino_1']
        eje_retino_1 = request.form['eje_retino_1']
        dp_retino_1 = request.form['dp_retino_1']
        vl20_retino_1 = request.form['vl20_retino_1']
        vp20_retino_1 = request.form['vp20_retino_1']
        add_retino_1 = request.form['add_retino_1']
        esfera = request.form['esfera']
        cilindro = request.form['cilindro']
        eje = request.form['eje']
        dp = request.form['dp']
        vl20 = request.form['vl20']
        vp20 = request.form['vp20']
        add_0 = request.form['add_0']
        esfera_1 = request.form['esfera_1']
        cilindro_1 = request.form['cilindro_1']
        eje_1 = request.form['eje_1']
        dp_1 = request.form['dp_1']
        vl20_1 = request.form['vl20_1']
        vp20_1 = request.form['vp20_1']
        add_1 = request.form['add_1']
        recomendación = request.form['recomendación']
        diagnostico = request.form['diagnostico']
        observación = request.form['observación']
        tipo_lente = request.form['tipo_lente']
        montura = request.form['montura']
        material = request.form['material']
        filtro = request.form['filtro']
        color = request.form['color']
        observacion = request.form['obs']

        user = paciente(
            documento=documento,
            tipo=tipo,
            nombre_paciente=nombre_paciente,
            edad=edad,
            genero=genero,
            correo_electronico=correo_electronico,
            direccion=direccion,
            telefono=telefono,
            eps=eps,
            cargo=cargo,
            acompanante=acompanante,
            parentesco=parentesco,
            telefono_acompanante=telefono_acompanante
        )
        db.session.add(user)
        db.session.commit()

        nuevos_antecedentes = antecedentes(
            diabetes=diabetes,
            hipertension=hipertension,
            artritis=artritis,
            alergia=alergia,
            catarata=catarata,
            glaucoma=glaucoma,
            estrabismo=estrabismo,
            queratocono=queratocono,
            otros=otros,
            diabetes_per=diabetes1,
            hipertension_per=hipertension1,
            Artritis_per=artritis1,
            Alergia_per=alergia1,
            ulcera_per=ulcera1,
            cirugia_per=cirugia,
            lentes_contacto_per=lentes,
            otros1=otros1,
            descripcion=descripcion
        )

        nuevos_antecedentes.paciente = user  # Relacion con llave Foranea
        db.session.add(nuevos_antecedentes)
        db.session.commit()

        nueva_consulta = MovConsulta(
            mov_consulta=mov_consulta,
            ulti_consulta=ulti_consulta,
  	        vlsc_od = vlsc_od,
            vlsc_oi = vlsc_oi,
            vlsc_ao = vlsc_ao,
            vlsc_PH = vlsc_PH,
            vpsc_od = vpsc_od,
            vpsc_oi = vpsc_oi,
            vpsc_ao = vpsc_ao ,
            vpsc_PH = vpsc_PH ,   
            vlcc_od = vlcc_od,
            vlcc_oi = vlcc_oi,
            vlcc_ao = vlcc_ao,
            vlcc_PH = vlcc_PH,
            vpcc_od = vpcc_od,
            vpcc_oi = vpcc_oi,
            vpcc_ao = vpcc_ao ,
            vpcc_PH = vpcc_PH ,      
            lensometria_od=lensometria_od,
            lensometria_oi=lensometria_oi,
            lensometria_add=lensometria_add,
            lensometria_tipo_lente=lensometria_tipo_lente,
            examen_externo=examen_externo,
            examen_ppc = examen_ppc,
            examen_ducciones = examen_ducciones,
            examen_cover_test = examen_cover_test


        )
        nueva_consulta.paciente = user
        db.session.add(nueva_consulta)
        db.session.commit()

        nueva_vista = Vista(
            OFTALMOSCOPIA_ojo_derecho=OFTALMOSCOPIA_ojo_derecho,
            OFTALMOSCOPIA_ojo_izquierdo=OFTALMOSCOPIA_ojo_izquierdo,
            ojo_drc_querato=ojo_drc_querato,
            ojo_izq_querato=ojo_izq_querato,
            esfera_retino=esfera_retino,
            cilindro_retino=cilindro_retino,
            eje_retino=eje_retino,
            dp_retino=dp_retino,
            vl20_retino=vl20_retino,
            vp20_retino=vp20_retino,
            add_retino=add_retino,
            esfera_retino_1=esfera_retino_1,
            cilindro_retino_1=cilindro_retino_1,
            eje_retino_1=eje_retino_1,
            dp_retino_1=dp_retino_1,
            vl20_retino_1=vl20_retino_1,
            vp20_retino_1=vp20_retino_1,
            add_retino_1=add_retino_1,
            esfera=esfera,
            cilindro=cilindro,
            eje=eje,
            dp=dp,
            vl20=vl20,
            vp20=vp20,
            add_0=add_0,
            esfera_1=esfera_1,
            cilindro_1=cilindro_1,
            eje_1=eje_1,
            dp_1=dp_1,
            vl20_1=vl20_1,
            vp20_1=vp20_1,
            add_1=add_1,
            recomendación=recomendación,
            diagnostico=diagnostico,
            observación=observación,
            tipo_lente=tipo_lente,
            montura=montura,
            material=material,
            filtro=filtro,
            color=color,
            observacion=observacion
        )
        nueva_vista.paciente = user
        db.session.add(nueva_vista)
        db.session.commit()

        print('Paciente Registrado Correctamente')
        flash('Paciente Registrado Correctamente', 'success')
        return render_template('menu.html', user_authenticated=user_authenticated)
    else:
        print('Registre un paciente o regrese a la pagina anterior')

    return render_template('register.html', user_authenticated=user_authenticated)

#Consultar pacienteS
@app.route("/consult", methods=['GET', 'POST'])
@csrf.exempt
@login_required
@role_required('admin', 'consulta')
def consult():
    user_authenticated = get_user_authenticated()
    pacientes = None
    antecedentes_dict = {}
    mov_consulta_dic = {}
    vista_dict = {}
    
    if request.method == 'POST':
        documento = request.form['consult']
        pacientes = paciente.query.filter_by(documento=documento).all()
        
        if pacientes:
            for p in pacientes:
                antecedente = antecedentes.query.filter_by(paciente_documento=p.documento).first()
                antecedentes_dict[p.documento] = antecedente
                mov_consulta = MovConsulta.query.filter_by(paciente_documento=p.documento).first()
                mov_consulta_dic[p.documento] = mov_consulta
                vista = Vista.query.filter_by(paciente_documento=p.documento).first()
                vista_dict[p.documento] = vista
    
    return render_template('consult.html', pacientes=pacientes, antecedentes=antecedentes_dict, mov_consulta=mov_consulta_dic, vista=vista_dict, user_authenticated=user_authenticated)

@app.route("/edit/<int:id>/update", methods=['GET', 'POST'])
@csrf.exempt
@login_required
@role_required('admin')
def edit(id):
    user_authenticated = get_user_authenticated()
    editar_paciente = paciente.query.filter_by(documento= paciente.documento).first()
    editar_antecedentes = antecedentes.query.filter_by(
        paciente_documento=editar_paciente.documento).first()
    editar_movconsulta = MovConsulta.query.filter_by(
        paciente_documento=editar_paciente.documento).first()
    editar_vista = Vista.query.filter_by(
        paciente_documento=editar_paciente.documento).first()

    if request.method == 'POST':
        editar_paciente.documento = request.form['document']
        editar_paciente.tipo = request.form['tdocument']
        editar_paciente.nombre_paciente = request.form['name']
        editar_paciente.edad = request.form['yearold']
        editar_paciente.genero = request.form['gender']
        editar_paciente.correo_electronico = request.form['email']
        editar_paciente.direccion = request.form['direcction']
        editar_paciente.telefono = request.form['phone']
        editar_paciente.eps = request.form['eps']
        editar_paciente.cargo = request.form['charge']
        editar_paciente.acompanante = request.form['companion']
        editar_paciente.parentesco = request.form['relationship']
        editar_paciente.telefono_acompanante = request.form['phonerelationship']
        # Antecedentes
        editar_antecedentes.diabetes = request.form['dia']
        editar_antecedentes.hipertension = request.form['hiper']
        editar_antecedentes.artritis = request.form['artr']
        editar_antecedentes.alergia = request.form['aler']
        editar_antecedentes.catarata = request.form['cata']
        editar_antecedentes.glaucoma = request.form['glau']
        editar_antecedentes.estrabismo = request.form['estra']
        editar_antecedentes.queratocono = request.form['quera']
        editar_antecedentes.otros = request.form['otros']
        editar_antecedentes.diabetes1 = request.form['diabetes']
        editar_antecedentes.hipertension1 = request.form['hipertension']
        editar_antecedentes.artritis1 = request.form['artritis']
        editar_antecedentes.alergia1 = request.form['alergia']
        editar_antecedentes.ulcera1 = request.form['ulcera']
        editar_antecedentes.cirugia = request.form['cirugia']
        editar_antecedentes.lentes = request.form['lentes']
        editar_antecedentes.otros1 = request.form['otros_1']
        editar_antecedentes.descripcion = request.form['descripcion']

         # Motivo de Consulta

        editar_movconsulta.mov_consulta = request.form['mov_consulta']
        editar_movconsulta.ulti_consulta = request.form['ulti_consulta']
        editar_movconsulta.vlsc_od = request.form['vlsc_od']
        editar_movconsulta.vlsc_oi = request.form['vlsc_oi']
        editar_movconsulta.vlsc_ao = request.form['vlsc_ao']
        editar_movconsulta.vlsc_PH = request.form['vlsc_PH']
        editar_movconsulta.vpsc_od = request.form['vpsc_od']
        editar_movconsulta.vpsc_oi = request.form['vpsc_oi']
        editar_movconsulta.vpsc_ao = request.form['vpsc_ao']
        editar_movconsulta.vpsc_PH = request.form['vpsc_PH']
        editar_movconsulta.vlcc_od = request.form['vlcc_od']
        editar_movconsulta.vlcc_oi = request.form['vlcc_oi']
        editar_movconsulta.vlcc_ao = request.form['vlcc_ao']
        editar_movconsulta.vlcc_PH = request.form['vlcc_PH']
        editar_movconsulta.vpcc_od = request.form['vpcc_od']
        editar_movconsulta.vpcc_oi = request.form['vpcc_oi']
        editar_movconsulta.vpcc_ao = request.form['vpcc_ao']
        editar_movconsulta.vpcc_PH = request.form['vpcc_PH']
        editar_movconsulta.lensometria_od = request.form['lensometria_od']
        editar_movconsulta.lensometria_oi = request.form['lensometria_oi']
        editar_movconsulta.lensometria_add = request.form['lensometria_add']
        editar_movconsulta.lensometria_tipo_lente = request.form['lensometria_tipo_lente']
        editar_movconsulta.examen_externo = request.form['examen_externo']
        editar_movconsulta.examen_ppc = request.form['ppc']
        editar_movconsulta.examen_ducciones = request.form['ducciones']
        editar_movconsulta.examen_cover_test = request.form['cover_test']



        # vista

        editar_vista.OFTALMOSCOPIA_ojo_derecho = request.form['OFTALMOSCOPIA_ojo_derecho']
        editar_vista.OFTALMOSCOPIA_ojo_izquierdo = request.form['OFTALMOSCOPIA_ojo_izquierdo']
        editar_vista.ojo_izq_querato = request.form['ojo_izq_querato']
        editar_vista.ojo_izq_querato = request.form['ojo_izq_querato']
        editar_vista.esfera_retino = request.form['esfera_retino']
        editar_vista.cilindro_retino = request.form['cilindro_retino']
        editar_vista.eje_retino = request.form['eje_retino']
        editar_vista.dp_retino = request.form['dp_retino']
        editar_vista.vl20_retino = request.form['vl20_retino']
        editar_vista.vp20_retino = request.form['vp20_retino']
        editar_vista.add_retino = request.form['add_retino']
        editar_vista.esfera_retino_1 = request.form['esfera_retino_1']
        editar_vista.cilindro_retino_1 = request.form['cilindro_retino_1']
        editar_vista.eje_retino_1 = request.form['eje_retino_1']
        editar_vista.dp_retino_1 = request.form['dp_retino_1']
        editar_vista.vl20_retino_1 = request.form['vl20_retino_1']
        editar_vista.vp20_retino_1 = request.form['vp20_retino_1']
        editar_vista.add_retino_1 = request.form['add_retino_1']
        editar_vista.esfera = request.form['esfera']
        editar_vista.cilindro = request.form['cilindro']
        editar_vista.eje = request.form['eje']
        editar_vista.dp = request.form['dp']
        editar_vista.vl20 = request.form['vl20']
        editar_vista.vp20 = request.form['vp20']
        editar_vista.add_0 = request.form['add_0']
        editar_vista.esfera_1 = request.form['esfera_1']
        editar_vista.cilindro_1 = request.form['cilindro_1']
        editar_vista.eje_1 = request.form['eje_1']
        editar_vista.dp_1 = request.form['dp_1']
        editar_vista.vl20_1 = request.form['vl20_1']
        editar_vista.vp20_1 = request.form['vp20_1']
        editar_vista.add_1 = request.form['add_1']
        editar_vista.recomendación = request.form['recomendación']
        editar_vista.diagnostico = request.form['diagnostico']
        editar_vista.observación = request.form['observación']
        editar_vista.tipo_lente = request.form['tipo_lente']
        editar_vista.montura = request.form['montura']
        editar_vista.material = request.form['material']
        editar_vista.filtro = request.form['filtro']
        editar_vista.color = request.form['color']
        editar_vista.observacion = request.form['obs']

        db.session.commit()
        print('El usuario se ha editado correctamente')
        flash('El paciente se ha editado correctamente', 'success')
        return render_template('menu.html')
    else:
        print('Paciente no encontrado')
        return render_template('edit.html', paciente=editar_paciente, antecedentes=editar_antecedentes, mov_consulta=editar_movconsulta, vista=editar_vista, user_authenticated=user_authenticated)


@app.route('/logout')
@login_required
def logout():
    user_authenticated = get_user_authenticated()
    session['user_authenticated'] = False
    session.pop('usuario', None)
    return render_template('login.html', user_authenticated=user_authenticated)

@app.route('/delete/<int:documento>')
@csrf.exempt
@login_required
@role_required('admin')
def eliminar_paciente(documento):
    user_authenticated = get_user_authenticated()

    # Busca el paciente por su documento
    paciente_a_eliminar = paciente.query.filter_by(documento=documento).first()

    if paciente_a_eliminar:
        #Elimina los Registros
        antecedentes.query.filter_by(paciente_documento=paciente_a_eliminar.documento).delete()
        MovConsulta.query.filter_by(paciente_documento=paciente_a_eliminar.documento).delete()
        Vista.query.filter_by(paciente_documento=paciente_a_eliminar.documento).delete()
     
        db.session.delete(paciente_a_eliminar)
        db.session.commit()
        flash('El paciente ha sido eliminado correctamente', 'success')
        print('El paciente ha sido eliminado correctamente')
    else:
        print('No se encontró al paciente')
        flash('No se encontró al paciente', 'danger')

    return render_template('consult.html', user_authenticated=user_authenticated)

@app.route('/Generar_cita', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def Generar_cita():
    pacientes = None

    if request.method == 'POST':
        action = request.form.get('action')

        # Búsqueda del paciente por documento
        if action == 'buscar':
            documento = request.form.get('consult')
            if documento:
                pacientes = paciente.query.filter_by(documento=documento).all()
                if not pacientes:
                    flash('Paciente no encontrado', 'danger')
            else:
                flash('Debe ingresar un número de documento', 'danger')

        # Agendar la cita para el paciente encontrado
        elif action == 'agendar_cita':
            documento = request.form.get('consult')
            calendar = request.form.get('calendar')
            time = request.form.get('reloj')
            note = request.form.get('note')

            if documento and calendar and time:
                pacientes = paciente.query.filter_by(documento=documento).all()
                if pacientes:
                    p = pacientes[0]

                    # Guardar los registros.
                    gen_cita = generar_cita(
                        calendar=calendar,
                        time=time,
                        note=note,
                        paciente_documento=p.documento
                    )
                    db.session.add(gen_cita)
                    db.session.commit()
                    flash('Cita médica registrada con éxito.', 'success')

                    # Enviar el correo (si se requiere)
                    msg = Message(
                        subject="Recordatorio de Cita Médica",
                        sender=app.config['MAIL_USERNAME'],
                        recipients=[p.correo_electronico]
                    )
                    msg.body = (f"Estimado/a {p.nombre_paciente},\n\n"
                                f"Este es un recordatorio de su próxima cita el {calendar} a las {time}.\n\n"
                                "Gracias por confiar en nosotros.\n\nAtentamente,\nAmplitud Visión")
                    
                    mail.send(msg)
                    flash('Se ha enviado un correo con los detalles de la cita médica, verifique su correo.', 'success')
                    print("Se ha enviado un correo con los detalles de la cita médica, verifique su correo.")
                else:
                    flash('Paciente no encontrado', 'danger')
                    print("Paciente no encontrado")
            else:
                flash('Datos incompletos para agendar la cita', 'danger')
                print("Datos incompletos para agendar la cita")

    return render_template('Generar_cita.html', pacientes=pacientes)


@app.route('/Consultar_cita', methods=['GET', 'POST'])
@login_required
@role_required('admin', 'consulta')
def consultar_cita():

    pacientes = None
    gen_consulta = None
    
    if request.method == 'POST':
        documento = request.form['consult']
        if documento:
            pacientes = paciente.query.filter_by(documento=documento).all()

            if pacientes:
                # Usa .all() para obtener todas las citas
                gen_consulta = generar_cita.query.filter_by(paciente_documento=pacientes[0].documento).all()
            else:
                flash('Paciente no encontrado', 'danger')
                print("Paciente no encontrado")
        else:
            flash('Por favor ingrese el documento del paciente', 'danger')
            print("Por favor ingrese el documento del paciente")
    
    return render_template('Consultar_cita.html', pacientes=pacientes, citas=gen_consulta)
    
    
  #Inventory:
  
class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime)
    sede = db.Column(db.String(40))
    montura = db.Column(db.String(40))
    cantidad_montura = db.Column(db.Integer)
    marca = db.Column(db.String(40))
    referencia = db.Column(db.String(20))
    color = db.Column(db.String(20))
    precio_montura = db.Column(db.Float, nullable=False)
    cordones = db.Column(db.String(30))
    cantidad_cordones = db.Column(db.Integer)
    precio_cordones = db.Column(db.Float, nullable=False)
    estuches = db.Column(db.String(30))
    cantidad_estuches = db.Column(db.Integer)
    precio_estuches = db.Column(db.Float, nullable=False)
    stopper = db.Column(db.String(50))
    cantidad_stopper = db.Column(db.Integer)
    precio_venta = db.Column(db.Float, nullable=False)


def __init__(self, fecha,sede, montura, cantidad_montura, marca, referencia, color, precio_montura, cordones, cantidad_cordones, precio_cordones, estuches, cantidad_estuches, precio_estuches, stopper, cantidad_stopper, precio_venta):
    self.fecha = fecha
    self.sede = sede
    self.montura = montura
    self.cantidad_montura = cantidad_montura
    self.marca = marca
    self.referencia = referencia
    self.color = color
    self.precio_montura = precio_montura
    self.cordones = cordones
    self.cantidad_cordones = cantidad_cordones
    self.precio_cordones = precio_cordones
    self.estuches = estuches
    self.cantidad_estuches = cantidad_estuches
    self.precio_estuches = precio_estuches
    self.stopper = stopper
    self.cantidad_stopper = cantidad_stopper
    self.precio_venta = precio_venta

class TaskSchema(ma.Schema):
        class Meta:
            fields = ('id','fecha','sede','montura','cantidad_montura','marca','referencia','color','precio_montura',
           'cordones', 'cantidad_cordones','precio_cordones','estuches','cantidad_estuches','precio_estuches','stopper',
           'cantidad_stopper', 'precio_venta')
            
task_schema = TaskSchema()
task_schema = TaskSchema(many=True)

class Venta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero_recibo = db.Column(db.String(50), nullable=False, unique=True)
    fecha_venta = db.Column(db.String(50))
    estado = db.Column(db.String(20), default='completada')
    cliente_id = db.Column(db.Integer, nullable=False)  
    nombre = db.Column(db.String(50))
    email = db.Column(db.String(120), nullable=False)
    telefono = db.Column(db.String(20))
    direccion = db.Column(db.String(200))
    total = db.Column(db.Float, nullable=False)
    detalles = db.relationship('VentaDetalle', backref='venta', lazy=True)


def __init__(self, numero_recibo, fecha_venta, estado, cliente_id, nombre, email, telefono, direccion):
    self.numero_recibo = numero_recibo
    self.fecha_venta = fecha_venta
    self.estado = estado
    self.cliente_id = cliente_id
    self.nombre = nombre
    self.email = email
    self.telefono = telefono
    self.direccion = direccion

class TaskSchema(ma.Schema):
        class Meta:('id','numero_recibo','fecha_venta','estado','cliente_id','nombre' ,'email','telefono','direccion')

task_schema = TaskSchema()
task_schema = TaskSchema(many=True)


class VentaDetalle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    venta_id = db.Column(db.Integer, db.ForeignKey('venta.id'), nullable=False)  # Relación con la tabla venta
    producto_id = db.Column(db.Integer, db.ForeignKey('inventory.id'), nullable=False)  # Relación con inventario
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
    producto = db.relationship('Inventory', backref='ventas_detalle', lazy=True)

def __init__(self, venta_id, producto_id, cantidad, precio_unitario):
    self.venta_id = venta_id
    self.producto_id = producto_id
    self.cantidad = cantidad
    self.precio_unitario = precio_unitario
    self.subtotal = cantidad * precio_unitario

class TaskSchema(ma.Schema):
        class Meta:('id','venta_id','producto_id','cantidad','precio_unitario','subtotal')

task_schema = TaskSchema()
task_schema = TaskSchema(many=True)


# Agregar los datos dentro del inventario
@app.route("/inventory", methods=['GET', 'POST'])
@login_required
@csrf.exempt
@role_required('admin')
def inventario():
    if request.method == 'POST':
        fecha = request.form['day']
        sede = request.form['sede']
        montura = request.form['montura']
        cantidad_montura = request.form['cantidad_montura']
        marca = request.form['marca']
        referencia = request.form['referencia']
        precio_montura = float(request.form['precio_montura']) 
        color = request.form['color']
        cordones = request.form['cordones']
        cantidad_cordones = request.form['cantidad_cordones']
        precio_cordones = float(request.form['precio_cordones']) 
        estuches = request.form['estuches']
        cantidad_estuches = request.form['cantidad_estuches']
        precio_estuches = float(request.form['precio_estuches']) 
        stopper = request.form['stopper']
        cantidad_stopper = request.form['cantidad_stopper']
        precio_venta = float(request.form['precio_venta'])

        inventario = Inventory(
            fecha=fecha,
            sede=sede,
            montura=montura,
            cantidad_montura=cantidad_montura,
            marca=marca,
            referencia=referencia,
            precio_montura = precio_montura,
            color=color,
            cordones=cordones,
            cantidad_cordones=cantidad_cordones,
            precio_cordones = precio_cordones,
            estuches=estuches,
            cantidad_estuches=cantidad_estuches,
            precio_estuches = precio_estuches,
            stopper=stopper,
            cantidad_stopper=cantidad_stopper,
            precio_venta = precio_venta
        )
        db.session.add(inventario)
        db.session.commit()
        print('Inventario agregado correctamente')
        flash('Inventario agregado correctamente', 'success' )
        return render_template('inventory.html')
    else:
        print('Inventario no Disponible')
        flash('Inventario no Disponible', 'danger')
        return render_template('inventory.html')
    

#Generar archivo de export del inventario
@app.route('/export')
@login_required
@role_required('admin')
@csrf.exempt
def export():
    try:
        data = Inventory.query.all()
        df = pd.DataFrame([[item.id, item.fecha, item.sede, item.montura, item.cantidad_montura, item.marca, item.referencia, item.precio_montura, item.color, item.cordones,
                            item.cantidad_cordones,item.precio_cordones, item.estuches, item.cantidad_estuches, item.precio_estuches, item.stopper, item.cantidad_stopper, item.precio_venta
                            ] for item in data],
                          columns=['ID', 'Fecha', 'Sede', 'Montura', 'Cantidad Montura', 'Marca', 'Referencia', 'Precio de Montura' , 'Color', 'Cordones', 'Cantidad Cordones', 'Precio de Cordones' ,'Estuches', 'Cantidad Estuches', 'Precio de Estuches' , 'Stopper', 'Cantidad Stopper','precio_venta'])
        
        # Crear directorio para informes si no existe
        reports_dir = os.path.join(app.root_path, 'static', 'reports')
        os.makedirs(reports_dir, exist_ok=True)
        
        # Generar archivo csv
        csv_filename = f'inventory_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        csv_path = os.path.join(reports_dir, csv_filename)
        df.to_csv(csv_path, index=False, sep=';')

        # Generar perfil de datos
        profile = ProfileReport(df, title='Perfil de Datos')
        report_filename = f'report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html'
        profile_html_path = os.path.join(reports_dir, report_filename)
        profile.to_file(profile_html_path)

        print('Se generó informe de manera correcta')
        flash('Se generó informe de manera correcta', 'success')
        
        # Redirigir al usuario a la página de inventario con enlaces de descarga
        return render_template('inventory.html', csv_filename=csv_filename, report_filename=report_filename)
    
    except Exception as e:
        print(f'Error al generar el informe: {str(e)}')
        flash('Error al generar el informe', 'error')
        return render_template('inventory.html')

#Generar la descarga del archivo.
@app.route('/download/<filename>')
@login_required
@role_required('admin')
def download_file(filename):
    reports_dir = os.path.join(app.root_path, 'static', 'reports')
    return send_from_directory(reports_dir, filename, as_attachment=True)



#Busqueda de Inventario
@app.route('/consultinventory')
@csrf.exempt
@login_required
@role_required('admin', 'consulta')
def consultinventory():
    inventory = Inventory.query.all()  # Obtener todos los registros de la tabla Inventory
    return render_template('consultinventory.html', inventory=inventory)


# Realizar una venta
@app.route('/venta', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def realizar_venta():
    nueva_venta = None  # Inicializamos 'nueva_venta' antes del bloque try
    
    if request.method == 'GET':
        productos = Inventory.query.all()
        return render_template('venta.html', productos=productos)
    
    elif request.method == 'POST':
        try:
            # Datos de la venta
            fecha_venta = request.form['fecha_venta']
            numero_recibo = request.form['numero-recibo']
            productos = request.form.getlist('productos[]')
            cantidades = request.form.getlist('cantidades[]')
            precios = request.form.getlist('precios[]')

            # Datos del cliente
            cliente_id = request.form['cliente_id']
            nombre = request.form['nombre']
            email = request.form['email']
            telefono = request.form['telefono']
            direccion = request.form['direccion']

            # Validación de datos
            if not productos or not cantidades or not precios:
                flash('Debe seleccionar al menos un producto y cantidad', 'danger')
                print("Debe seleccionar al menos un producto y cantidad")
                return redirect(url_for('realizar_venta'))

            # Iniciar transacción
            db.session.begin_nested()

            # Crear objeto de venta
            nueva_venta = Venta(
                numero_recibo=numero_recibo,
                fecha_venta=fecha_venta,
                cliente_id=cliente_id,
                nombre=nombre,
                email=email,
                telefono=telefono,
                direccion=direccion,
                total=0  # Inicializamos el total
            )

            db.session.add(nueva_venta)
            db.session.flush()  # Asigna un ID a la venta sin confirmar la transacción

            # Crear los detalles de la venta
            for i in range(len(productos)):
                # Obtener el valor del producto (e.g., "montura-1")
                producto_value = productos[i]
                cantidad = int(cantidades[i])
                precio_unitario = float(precios[i])

                # Separar el tipo de producto y el ID
                tipo_producto, producto_id = producto_value.split('-')

                # Buscar el producto en el inventario
                producto = Inventory.query.get(producto_id)

                if not producto:
                    db.session.rollback()
                    flash(f"El producto con ID {producto_id} no existe.", 'danger')
                    print(f"El producto con ID {producto_id} no existe.")
                    return redirect(url_for('realizar_venta'))

                # Validar la cantidad disponible en el inventario
                if tipo_producto == "montura" and producto.cantidad_montura < cantidad:
                    flash(f"No hay suficiente stock de monturas para el producto {producto.montura}.", 'danger')
                    print(f"No hay suficiente stock de monturas para el producto {producto.montura}.")
                    db.session.rollback()
                    return redirect(url_for('realizar_venta'))  # Este return debe estar correctamente indentado

                # Calcular el subtotal
                subtotal = cantidad * precio_unitario

                # Crear el detalle de la venta
                detalle = VentaDetalle(
                    venta_id=nueva_venta.id,
                    producto_id=producto_id,
                    cantidad=cantidad,
                    precio_unitario=precio_unitario,
                    subtotal=subtotal
                )

                db.session.add(detalle)

                # Actualizar el inventario
                if tipo_producto == "montura":
                    producto.cantidad_montura -= cantidad
                elif tipo_producto == "cordones":
                    producto.cantidad_cordones -= cantidad
                elif tipo_producto == "estuches":
                    producto.cantidad_estuches -= cantidad
                elif tipo_producto == "stopper":
                    producto.cantidad_stopper -= cantidad

                # Actualizar el total de la venta
                nueva_venta.total += subtotal

            # Confirmar la transacción
            db.session.commit()

            # Generar el XML y PDF
            xml_compra = generar_xml_compra(nueva_venta)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".xml") as temp_xml:
                temp_xml.write(xml_compra.encode('utf-8'))
                temp_xml_path = temp_xml.name

            pdf_path = generar_pdf_compra(nueva_venta)

            # Enviar el correo con los archivos adjuntos
            try:
                msg = Message('Recibo de Compra',
                              sender=app.config['MAIL_USERNAME'],  # Cambia MAIL_PASSWORD a MAIL_USERNAME
                              recipients=[nueva_venta.email])

                # Renderizar plantilla HTML del correo
                msg.html = render_template('email_compra.html', venta=nueva_venta)

                # Adjuntar el archivo XML
                with open(temp_xml_path, 'rb') as f:
                    msg.attach(f'{nueva_venta.numero_recibo}.xml', 'application/xml', f.read())

                # Adjuntar el archivo PDF
                with open(pdf_path, 'rb') as f:
                    msg.attach(f'{nueva_venta.numero_recibo}.pdf', 'application/pdf', f.read())

                # Enviar el correo
                mail.send(msg)
                flash('Correo enviado con éxito', 'success')
                print('Correo enviado con éxito')

            except Exception as e:
                flash(f'Error al enviar el correo: {str(e)}', 'danger')
                print(f'Error al enviar el correo: {str(e)}')

            # Limpiar archivos temporales
            os.unlink(temp_xml_path)
            os.unlink(pdf_path)

            flash('Venta realizada con éxito', 'success')
            print('Venta realizada con éxito')
            return redirect(url_for('realizar_venta'))  # Asumiendo que tienes una vista para listar ventas

        except Exception as e:
            db.session.rollback()
            flash(f'Error al procesar la venta: {str(e)}', 'danger')
            print(f'Error al procesar la venta: {str(e)}')
            return redirect(url_for('realizar_venta'))
        
# Función para actualizar el inventario
def actualizar_inventario(producto_id, cantidad_vendida):
    inventario = Inventory.query.get(producto_id)
    if inventario:
        if inventario.cantidad_montura < cantidad_vendida:
            flash(f"No hay suficiente stock para el producto {inventario.montura}", 'danger')
            print(f"No hay suficiente stock para el producto {inventario.montura}")
            return False
        inventario.cantidad_montura -= cantidad_vendida
        db.session.commit()
        flash(f"Inventario de {inventario.montura} actualizado correctamente", 'success')
        print(f"Inventario de {inventario.montura} actualizado correctamente")

# Búsqueda de recibo
@app.route('/search', methods=['GET', 'POST'])
@csrf.exempt
@login_required
@role_required('admin', 'consulta')
def search():
    if request.method == 'POST':
        numero_recibo = request.form['recibo']
        venta_data = Venta.query.options(joinedload(Venta.detalles).joinedload(VentaDetalle.producto)).filter_by(numero_recibo=numero_recibo).first()

        if venta_data:
            return render_template('search.html', venta=venta_data)
        else:
            flash('Información no disponible', 'danger')
            print("Información no disponible")
    return render_template('search.html')

def generar_xml_compra(compra):
    root = ET.Element("Recibo")  # Crear el elemento raíz del documento XML
    
    # Información de la venta
    ET.SubElement(root, "NumeroRecibo").text = str(compra.numero_recibo)
    ET.SubElement(root, "FechaCompra").text = str(compra.fecha_venta)
    
    # Información del cliente (Ajustar para usar los atributos correctos)
    ET.SubElement(root, "NombreCliente").text = compra.nombre
    ET.SubElement(root, "Direccion").text = compra.direccion
    ET.SubElement(root, "Telefono").text = compra.telefono
    ET.SubElement(root, "Email").text = compra.email

    # Información de los productos vendidos
    items = ET.SubElement(root, "Items")
    for detalle in compra.detalles:  # Acceder a los detalles correctamente
        item = ET.SubElement(items, "Item")
        ET.SubElement(item, "ProductoID").text = str(detalle.producto_id)
        ET.SubElement(item, "Cantidad").text = str(detalle.cantidad)
        ET.SubElement(item, "PrecioUnitario").text = str(detalle.precio_unitario)
        ET.SubElement(item, "Subtotal").text = str(detalle.cantidad * detalle.precio_unitario)

    # Total de la venta
    ET.SubElement(root, "Total").text = str(compra.total)

    # Convertir a XML
    return ET.tostring(root, encoding='utf-8').decode('utf-8')

def generar_pdf_compra(compra):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
        pdf_path = temp_pdf.name

    # Configurar el documento
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Título
    elements.append(Paragraph(f"Recibo de Compra: {compra.numero_recibo}", styles['Title']))
    elements.append(Paragraph(f"Fecha: {compra.fecha_venta}", styles['Normal']))

    # Información del cliente
    cliente_data = [
        ["Cliente", compra.nombre],
        ["Dirección", compra.direccion],
        ["Teléfono", compra.telefono],
        ["Correo", compra.email]
    ]
    cliente_table = Table(cliente_data, colWidths=[100, 300])
    cliente_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ]))
    elements.append(cliente_table)

    # Detalles de la compra
    detalles_data = [["Producto", "Cantidad", "Valor Unitario", "Valor Total"]]
    for detalle in compra.detalles:  # Ajustar para usar 'detalles'
        detalles_data.append([detalle.producto_id, detalle.cantidad, detalle.precio_unitario, detalle.cantidad * detalle.precio_unitario])

    detalles_table = Table(detalles_data, colWidths=[200, 100, 100, 100])
    detalles_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(detalles_table)

    # Total de la venta
    total_data = [["Total", compra.total]]
    total_table = Table(total_data, colWidths=[300, 100])
    elements.append(total_table)

    # Generar PDF
    doc.build(elements)
    return pdf_path



if __name__ == '__main__':  # Se tiene un condicional para verificar que si se esta en el archivo de ejecución y no un modulo
    with app.app_context():
        db.create_all()
        mail.init_app(app)
    app.run(debug=True)
