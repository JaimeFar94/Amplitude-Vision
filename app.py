from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from flask_mail import Mail
from flask_mail import Message
from flask_wtf.csrf import CSRFProtect  
from functools import wraps
import hashlib
from datetime import datetime
import pandas as pd
from flask import render_template, request, session, Response ,flash
import pandas as pd
from pandas_profiling import ProfileReport
from flask import render_template, request, send_file
import ydata_profiling


app = Flask(__name__ , template_folder='templates')
app.secret_key = '876-105-169'


#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/medico'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://b65dd86ce1e7f8:b7356d9d@us-cluster-east-01.k8s.cleardb.net/heroku_1c8a7aa3361979f?reconnect=true'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#configuración de las cookies 
app.config['SESSION_COOKIE_SECURE'] = True  # Usar solo en producción con HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'



db = SQLAlchemy(app)
ma = Marshmallow(app)


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



# Login
class signup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(40), unique=True)
    correo = db.Column(db.String(70))
    usuario = db.Column(db.String(40), unique=True)
    contrasena = db.Column(db.String(40))

    def __init__(self, nombre, correo, usuario, contrasena):
        self.nombre = nombre
        self.correo = correo
        self.usuario = usuario
        self.contrasena = contrasena


class TaskSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nombre', 'correo', 'usuario', 'contrasena')


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
    ducciones_od = db.Column(db.String(40))
    ducciones_oi = db.Column(db.String(40))
    ppc_od = db.Column(db.String(40))
    ppc_oi = db.Column(db.String(40))
    examen_externo = db.Column(db.String(300))

    paciente_documento = db.Column(db.Integer, db.ForeignKey(
        'paciente.documento', onupdate='CASCADE', ondelete='CASCADE'))
    paciente = db.relationship(
        'paciente', backref=db.backref('MovConsulta', lazy=True))

    def __init__(self, mov_consulta=None, ulti_consulta=None, vlsc_od=None, vlsc_oi=None, vlsc_ao=None,
                 vlsc_PH=None, vpsc_od=None, vpsc_oi=None, vpsc_ao=None, vpsc_PH=None, ducciones_od=None,
                 ducciones_oi=None, ppc_od=None, ppc_oi=None, examen_externo=None):
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
        self.ducciones_od = ducciones_od
        self.ducciones_oi = ducciones_oi
        self.ppc_od = ppc_od
        self.ppc_oi = ppc_oi
        self.examen_externo = examen_externo

class TaskSchema(ma.Schema):
    class Meta:
        fields = ('mov_consulta', 'ulti_consulta', 'vlsc_od', 'vlsc_oi', 'vlsc_ao', 'vlsc_PH', 'vpsc_od',
                  'vpsc_oi', 'vpsc_ao', 'vpsc_PH', 'ducciones_od', 'ducciones_oi', 'ppc_od', 'ppc_oi')

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

# Registro de Eliminar


class delete(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    eliminado = db.Column(db.Boolean, default=False)
    fecha_eliminacion = db.Column(db.DateTime)
    nombre_eliminado = db.Column(db.String(100))
    documento_eliminado = db.Column(db.String(100))

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


@app.route("/")
def home():
        return render_template('home.html')


@app.route("/signup", methods=['GET', 'POST'])
@csrf.exempt
def signup_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        username = request.form['user']
        password = request.form['password']

        # Codificar la contraseña
        password_bytes = password.encode('utf-8')

        # Aplicar el modo MD5 dentro de la contraseña
        hashed_password = hashlib.md5(password_bytes).hexdigest()

        user = signup(
            nombre=name,
            correo=email,
            usuario=username,
            contrasena=hashed_password

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
                print('Bienvenido ' + username)
                return redirect(url_for('menu')) #Envia a menu.html
            else:
                print('Usuario o contraseña incorrectos')
                flash('Usuario o contraseña incorrectos', 'danger')
        else:
            print('Usuario o contraseña incorrectos')

    return render_template('login.html')

@app.route("/menu")
def menu():
    if 'user_authenticated' in session and session['user_authenticated']:
        username = session['usuario']
        return render_template('menu.html', username=username)
    else:
        return redirect(url_for('login'))

@app.route("/register", methods=['GET', 'POST'])
@csrf.exempt
@login_required
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
        ducciones_od = request.form['ducciones_od']
        ducciones_oi = request.form['ducciones_oi']
        ppc_od = request.form['ppc_od']
        ppc_oi = request.form['ppc_oi']
        examen_externo = request.form['examen_externo']

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
            ducciones_od=ducciones_od,
            ducciones_oi=ducciones_oi,
            ppc_od=ppc_od,
            ppc_oi=ppc_oi,
            examen_externo=examen_externo
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

@app.route("/consult", methods=['GET', 'POST'])
@csrf.exempt
@login_required
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
        editar_movconsulta.vpsc_ao = request.form['vpsc_PH']
        editar_movconsulta.vpsc_PH = request.form['vision_lejana']
        editar_movconsulta.ducciones_od = request.form['ducciones_od']
        editar_movconsulta.ducciones_oi = request.form['ducciones_oi']
        editar_movconsulta.ppc_od = request.form['ppc_od']
        editar_movconsulta.ppc_oi = request.form['ppc_oi']
        editar_movconsulta.examen_externo = request.form['examen_externo']



        # vista

        editar_vista.OFTALMOSCOPIA_ojo_derecho = request.form['OFTALMOSCOPIA_ojo_derecho']
        editar_vista.OFTALMOSCOPIA_ojo_izquierdo = request.form['OFTALMOSCOPIA_ojo_izquierdo']
        editar_vista.ojo_drc_querato = request.form['ojo_drc_querato']
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
        editar_vista.esfera = request.form['esfera ']
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
    
    
  #Inventory:
  
  
class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime)
    sede = db.Column(db.Integer)
    montura = db.Column(db.String(40))
    cantidad_montura = db.Column(db.Integer)
    marca = db.Column(db.String(40))
    referencia = db.Column(db.String(20))
    color = db.Column(db.String(20))
    cordones = db.Column(db.String(30))
    cantidad_cordones = db.Column(db.Integer)
    estuches = db.Column(db.String(30))
    cantidad_estuches = db.Column(db.Integer)
    stopper = db.Column(db.String(50))
    cantidad_stopper = db.Column(db.Integer)

    def __init__(self, fecha, sede, montura, cantidad_montura, marca, referencia, color, cordones, cantidad_cordones, estuches, cantidad_estuches, stopper, cantidad_stopper):
        self.fecha = fecha
        self.sede = sede
        self.montura = montura
        self.cantidad_montura = cantidad_montura
        self.marca = marca
        self.referencia = referencia
        self.color = color
        self.cordones = cordones
        self.cantidad_cordones = cantidad_cordones
        self.estuches = estuches
        self.cantidad_estuches = cantidad_estuches
        self.stopper = stopper
        self.cantidad_stopper = cantidad_stopper

    class TaskSchema(ma.Schema):
        class Meta:
            fields = ('id', 'fecha', 'sede', 'montura', 'cantidad_montura', 'marca', 'referencia', 'color', 'cordones',
                      'cantidad_cordones', 'estuches', 'cantidad_estuches',  'stopper', 'cantidad_stopper', 'numero_recibo')


class recibo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha_compra = db.Column(db.DateTime)
    numero_recibo = db.Column(db.Integer)
    documento = db.Column(db.Integer)
    nombre_paciente = db.Column(db.String(200))
    direccion = db.Column(db.String(200))
    telefono = db.Column(db.Integer)
    correo = db.Column(db.String(200))
    cantidad = db.Column(db.Integer)
    cantidad_1 = db.Column(db.Integer)
    cantidad_2 = db.Column(db.Integer)
    cantidad_3 = db.Column(db.Integer)
    cantidad_4 = db.Column(db.Integer)
    cantidad_5 = db.Column(db.Integer)
    cantidad_6 = db.Column(db.Integer)
    cantidad_7 = db.Column(db.Integer)
    detalle = db.Column(db.String(200))
    detalle_1 = db.Column(db.String(200))
    detalle_2 = db.Column(db.String(200))
    detalle_3 = db.Column(db.String(200))
    detalle_4 = db.Column(db.String(200))
    detalle_5 = db.Column(db.String(200))
    detalle_6 = db.Column(db.String(200))
    detalle_7 = db.Column(db.String(200))
    valor_unitario = db.Column(db.Float)
    valor_unitario_1 = db.Column(db.Float)
    valor_unitario_2 = db.Column(db.Float)
    valor_unitario_3 = db.Column(db.Float)
    valor_unitario_4 = db.Column(db.Float)
    valor_unitario_5 = db.Column(db.Float)
    valor_unitario_6 = db.Column(db.Float)
    valor_unitario_7 = db.Column(db.Float)
    valor_total = db.Column(db.Float)
    valor_total_1 = db.Column(db.Float)
    valor_total_2 = db.Column(db.Float)
    valor_total_3 = db.Column(db.Float)
    valor_total_4 = db.Column(db.Float)
    valor_total_5 = db.Column(db.Float)
    valor_total_6 = db.Column(db.Float)
    valor_total_7 = db.Column(db.Float)  
    total = db.Column(db.Float)

    def __init__(self, fecha_compra, numero_recibo, documento, nombre_paciente, direccion, telefono, correo, cantidad, cantidad_1, cantidad_2, cantidad_3, cantidad_4, cantidad_5, cantidad_6, cantidad_7, detalle, detalle_1, detalle_2, detalle_3, detalle_4, detalle_5, detalle_6, detalle_7, valor_unitario, valor_unitario_1, valor_unitario_2, valor_unitario_3, valor_unitario_4, valor_unitario_5, valor_unitario_6, valor_unitario_7, valor_total, valor_total_1, valor_total_2, valor_total_3, valor_total_4, valor_total_5, valor_total_6, valor_total_7, total):
        self.fecha_compra = fecha_compra
        self.numero_recibo = numero_recibo
        self.documento = documento
        self.nombre_paciente = nombre_paciente
        self.direccion = direccion
        self.telefono = telefono
        self.correo = correo
        self.cantidad = cantidad
        self.cantidad_1 = cantidad_1
        self.cantidad_2 = cantidad_2
        self.cantidad_3 = cantidad_3
        self.cantidad_4 = cantidad_4
        self.cantidad_5 = cantidad_5
        self.cantidad_6 = cantidad_6
        self.cantidad_7 = cantidad_7
        self.detalle = detalle
        self.detalle_1 = detalle_1
        self.detalle_2 = detalle_2
        self.detalle_3 = detalle_3
        self.detalle_4 = detalle_4
        self.detalle_5 = detalle_5
        self.detalle_6 = detalle_6
        self.detalle_7 = detalle_7
        self.valor_unitario = valor_unitario
        self.valor_unitario_1 = valor_unitario_1
        self.valor_unitario_2 = valor_unitario_2
        self.valor_unitario_3 = valor_unitario_3
        self.valor_unitario_4 = valor_unitario_4
        self.valor_unitario_5 = valor_unitario_5
        self.valor_unitario_6 = valor_unitario_6
        self.valor_unitario_7 = valor_unitario_7
        self.valor_total = valor_total
        self.valor_total_1 = valor_total_1
        self.valor_total_2 = valor_total_2
        self.valor_total_3 = valor_total_3
        self.valor_total_4 = valor_total_4
        self.valor_total_5 = valor_total_5
        self.valor_total_6 = valor_total_6
        self.valor_total_7 = valor_total_7
        self.total = total

    class TaskSchema(ma.Schema):
        class Meta:
            fields = ('id', 'fecha_compra', 'nombre_paciente', 'numero_recibo', 'documento', 'direccion', 'telefono', 'correo', 'cantidad', 'cantidad_1', 'cantidad_2', 'cantidad_3', 'cantidad_4', 'cantidad_5', 'cantidad_6', 'cantidad_7', 'detalle', 'detalle_1', 'detalle_2', 'detalle_3', 'detalle_4', 'detalle_5', 'detalle_6',
                      'detalle_7', 'valor_unitario', 'valor_unitario_1', 'valor_unitario_2', 'valor_unitario_3', 'valor_unitario_4', 'valor_unitario_5', 'valor_unitario_6', 'valor_unitario_7', 'valor_total', 'valor_total_1', 'valor_total_2', 'valor_total_3', 'valor_total_4', 'valor_total_5', 'valor_total_6', 'valor_total_7', 'total')


# Agregar los datos dentro del inventario
@app.route("/inventory", methods=['GET', 'POST'])
@login_required
@csrf.exempt
def inventario():
    if request.method == 'POST':
        fecha = request.form['day']
        sede = request.form['sede']
        montura = request.form['montura']
        cantidad_montura = request.form['cantidad_montura']
        marca = request.form['marca']
        referencia = request.form['referencia']
        color = request.form['color']
        cordones = request.form['cordones']
        cantidad_cordones = request.form['cantidad_cordones']
        estuches = request.form['estuches']
        cantidad_estuches = request.form['cantidad_estuches']
        stopper = request.form['stopper']
        cantidad_stopper = request.form['cantidad_stopper']

        inventario = Inventory(
            fecha=fecha,
            sede=sede,
            montura=montura,
            cantidad_montura=cantidad_montura,
            marca=marca,
            referencia=referencia,
            color=color,
            cordones=cordones,
            cantidad_cordones=cantidad_cordones,
            estuches=estuches,
            cantidad_estuches=cantidad_estuches,
            stopper=stopper,
            cantidad_stopper=cantidad_stopper,
        )
        db.session.add(inventario)
        db.session.commit()
        print('Inventario agregado correctamente')
        flash('Inventario agregado correctamente', 'success' )
        return render_template('inventory.html')
    else:
        print('Inventario no Disponible')
        return render_template('inventory.html')


@app.route('/export')
@login_required
@csrf.exempt
def export():
    data = Inventory.query.all()
    df = pd.DataFrame([[item.id, item.fecha, item.sede, item.montura, item.cantidad_montura, item.marca, item.referencia, item.color, item.cordones,
                        item.cantidad_cordones, item.estuches, item.cantidad_estuches, item.stopper, item.cantidad_stopper
                        ] for item in data],
                      columns=['ID', 'Fecha', 'Sede', 'Montura', 'Cantidad Montura', 'Marca', 'Referencia', 'Color', 'Cordones', 'Cantidad Cordones', 'Estuches', 'Cantidad Estuches', 'Stopper', 'Cantidad Stopper'])

    # Guardar CSV y se indica la carpeta donde se va a guardar la información
    output_dir = os.path.join(os.getcwd(), 'Informes')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    csv_path = os.path.join(output_dir, 'inventory.csv')
    df.to_csv(csv_path, index=False)

    # Generar perfil de datos
    profile = ProfileReport(df, title='Perfil de Datos')
    profile_html_path = os.path.join(output_dir, 'reporte.html')
    profile.to_file(profile_html_path)

    print('Se Genero Informe de Manera Correcta')
    flash('Se Genero Informe de Manera Correcta', 'success' )
    # Redirigir al usuario a la página de inventario con enlaces de descarga
    return render_template('inventory.html', csv_path='inventory.csv', report_path='reporte.html')


@app.route('/download/<filename>')
def download_file(filename):
    output_dir = os.path.join(os.getcwd(), 'Informes')
    return send_from_directory(output_dir, filename)


# Busqueda por # recibo

@app.route('/search', methods=['GET', 'POST'])
@login_required
@csrf.exempt
def search():
    if request.method == 'POST':
        numero_recibo = request.form['recibo']
        # Realiza la búsqueda en la base de datos usando el número de recibo
        inventory_data = recibo.query.filter_by(
            numero_recibo=numero_recibo).all()
        print("tu información", inventory_data)
        # Pasa 'recibo' como parte del contexto
        return render_template('search.html', inventory_data=inventory_data, recibo=numero_recibo)
    else:
        flash('Información no disponible', 'danger')
        print('Información no disponible')
    return render_template('search.html')

#Generar  archivo XML
def generar_xml_compra(compra):
    root = ET.Element("Recibo")  # Crear el elemento raíz del documento XML

    # Agregar los subelementos de la raíz
    ET.SubElement(root, "NumeroRecibo").text = str(compra.numero_recibo)
    ET.SubElement(root, "FechaCompra").text = str(compra.fecha_compra)
    ET.SubElement(root, "NombrePaciente").text = compra.nombre_paciente
    ET.SubElement(root, "Documento").text = str(compra.documento)
    ET.SubElement(root, "Direccion").text = str(compra.direccion)
    ET.SubElement(root, "Telefono").text = str(compra.telefono)
    ET.SubElement(root, "Correo").text = str(compra.correo)

    ET.SubElement(root, "Cantidad").text = str(compra.cantidad)
    ET.SubElement(root, "Cantidad_1").text = str(compra.cantidad_1)
    ET.SubElement(root, "Cantidad_2").text = str(compra.cantidad_2)
    ET.SubElement(root, "Cantidad_3").text = str(compra.cantidad_3)
    ET.SubElement(root, "Cantidad_4").text = str(compra.cantidad_4)
    ET.SubElement(root, "Cantidad_5").text = str(compra.cantidad_5)
    ET.SubElement(root, "Cantidad_6").text = str(compra.cantidad_6)
    ET.SubElement(root, "Cantidad_7").text = str(compra.cantidad_7)

    ET.SubElement(root, "Detalle").text = compra.detalle
    ET.SubElement(root, "Detalle_1").text = compra.detalle_1
    ET.SubElement(root, "Detalle_2").text = compra.detalle_2
    ET.SubElement(root, "Detalle_3").text = compra.detalle_3
    ET.SubElement(root, "Detalle_4").text = compra.detalle_4
    ET.SubElement(root, "Detalle_5").text = compra.detalle_5
    ET.SubElement(root, "Detalle_6").text = compra.detalle_6
    ET.SubElement(root, "Detalle_7").text = compra.detalle_7

    ET.SubElement(root, "ValorUnitario").text = str(compra.valor_unitario)
    ET.SubElement(root, "ValorUnitario_1").text = str(compra.valor_unitario_1)
    ET.SubElement(root, "ValorUnitario_2").text = str(compra.valor_unitario_2)
    ET.SubElement(root, "ValorUnitario_3").text = str(compra.valor_unitario_3)
    ET.SubElement(root, "ValorUnitario_4").text = str(compra.valor_unitario_4)
    ET.SubElement(root, "ValorUnitario_5").text = str(compra.valor_unitario_5)
    ET.SubElement(root, "ValorUnitario_6").text = str(compra.valor_unitario_6)
    ET.SubElement(root, "ValorUnitario_7").text = str(compra.valor_unitario_7)

    ET.SubElement(root, "ValorTotal").text = str(compra.valor_total)
    ET.SubElement(root, "ValorTotal_1").text = str(compra.valor_total_1)
    ET.SubElement(root, "ValorTotal_2").text = str(compra.valor_total_2)
    ET.SubElement(root, "ValorTotal_3").text = str(compra.valor_total_3)
    ET.SubElement(root, "ValorTotal_4").text = str(compra.valor_total_4)
    ET.SubElement(root, "ValorTotal_5").text = str(compra.valor_total_5)
    ET.SubElement(root, "ValorTotal_6").text = str(compra.valor_total_6)
    ET.SubElement(root, "ValorTotal_7").text = str(compra.valor_total_7)

    ET.SubElement(root, "Total").text = str(compra.total)

    items = ET.SubElement(root, "Items")
    for i in range(8):
        cantidad = str(getattr(compra, f'cantidad_{i}', ''))
        detalle = str(getattr(compra, f'detalle_{i}', ''))
        valor_unitario = str(getattr(compra, f'valor_unitario_{i}', ''))
        valor_total = str(getattr(compra, f'valor_total_{i}', ''))

        if cantidad and detalle and valor_unitario and valor_total:
            item = ET.SubElement(items, "Item")
            ET.SubElement(item, "Cantidad").text = cantidad
            ET.SubElement(item, "Detalle").text = detalle
            ET.SubElement(item, "ValorUnitario").text = valor_unitario
            ET.SubElement(item, "ValorTotal").text = valor_total

    ET.SubElement(root, "Total").text = str(compra.total)

    tree = ET.ElementTree(root)

    return ET.tostring(root, encoding='unicode')


@app.route('/recibo', methods=['GET', 'POST'])
@login_required
@csrf.exempt
def compra():
    if request.method == 'POST':
        fecha_compra = request.form['day']
        numero_recibo = request.form['numero-recibo']
        nombre_paciente = request.form['nombre_paciente']
        documento = request.form['cc']  
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        correo = request.form['correo']
        cantidad = request.form['cantidad']
        cantidad_1 = request.form['cantidad_1']
        cantidad_2 = request.form['cantidad_2']
        cantidad_3 = request.form['cantidad_3']
        cantidad_4 = request.form['cantidad_4']
        cantidad_5 = request.form['cantidad_5']
        cantidad_6 = request.form['cantidad_6']
        cantidad_7 = request.form['cantidad_7']
        detalle = request.form['detalle']
        detalle_1 = request.form['detalle_1']
        detalle_2 = request.form['detalle_2']
        detalle_3 = request.form['detalle_3']
        detalle_4 = request.form['detalle_4']
        detalle_5 = request.form['detalle_5']
        detalle_6 = request.form['detalle_6']
        detalle_7 = request.form['detalle_7']
        valor_unitario = request.form['v_unidad']
        valor_unitario_1 = request.form['v_unidad_1']
        valor_unitario_2 = request.form['v_unidad_2']
        valor_unitario_3 = request.form['v_unidad_3']
        valor_unitario_4 = request.form['v_unidad_4']
        valor_unitario_5 = request.form['v_unidad_5']
        valor_unitario_6 = request.form['v_unidad_6']
        valor_unitario_7 = request.form['v_unidad_7']
        valor_total = request.form['v_total']
        valor_total_1 = request.form['v_total_1']
        valor_total_2 = request.form['v_total_2']
        valor_total_3 = request.form['v_total_3']
        valor_total_4 = request.form['v_total_4']
        valor_total_5 = request.form['v_total_5']
        valor_total_6 = request.form['v_total_6']
        valor_total_7 = request.form['v_total_7']
        total = request.form['total']

        compra = recibo(
            fecha_compra=fecha_compra,
            numero_recibo=numero_recibo,
            documento=documento,
            nombre_paciente=nombre_paciente,
            direccion=direccion,
            telefono=telefono,
            correo=correo,
            cantidad=cantidad,
            cantidad_1=cantidad_1,
            cantidad_2=cantidad_2,
            cantidad_3=cantidad_3,
            cantidad_4=cantidad_4,
            cantidad_5=cantidad_5,
            cantidad_6=cantidad_6,
            cantidad_7=cantidad_7,
            detalle=detalle,
            detalle_1=detalle_1,
            detalle_2=detalle_2,
            detalle_3=detalle_3,
            detalle_4=detalle_4,
            detalle_5=detalle_5,
            detalle_6=detalle_6,
            detalle_7=detalle_7,
            valor_unitario=valor_unitario,
            valor_unitario_1=valor_unitario_1,
            valor_unitario_2=valor_unitario_2,
            valor_unitario_3=valor_unitario_3,
            valor_unitario_4=valor_unitario_4,
            valor_unitario_5=valor_unitario_5,
            valor_unitario_6=valor_unitario_6,
            valor_unitario_7=valor_unitario_7,
            valor_total=valor_total,
            valor_total_1=valor_total_1,
            valor_total_2=valor_total_2,
            valor_total_3=valor_total_3,
            valor_total_4=valor_total_4,
            valor_total_5=valor_total_5,
            valor_total_6=valor_total_6,
            valor_total_7=valor_total_7,
            total=total
        )
        db.session.add(compra)
        db.session.commit()
        # Generar el XML
        xml_compra = generar_xml_compra(compra)
        print(xml_compra)  # Imprimir o guardar el XML según sea necesario


        # Guardar el XML en un archivo temporal
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xml") as temp_xml:
            temp_xml.write(xml_compra.encode('utf-8'))
            temp_xml_path = temp_xml.name

        #Enviar el archivo adjunto

        msg = Message('Recibo de Compra',
                      sender=app.config['MAIL_PASSWORD'],
                      recipients=[compra.correo])
        msg.html = render_template('email_compra.html', compra=compra)

         # Adjuntar el archivo XML
        with open(temp_xml_path, 'rb') as f:
            msg.attach(f'{numero_recibo}.xml', 'application/xml', f.read())

  
        mail.send(msg)
        flash('El correo se envió con éxito', 'success')
        print('El correo se envió con éxito')
        return render_template('recibo.html')
    else:
        # Si la solicitud no es un POST, simplemente renderiza el template sin la variable compra
        print('Recibo no enviado')
        flash('Recibo no enviado', 'danger')
        return render_template('recibo.html')



if __name__ == '__main__':  # Se tiene un condicional para verificar que si se esta en el archivo de ejecución y no un modulo
    with app.app_context():
        db.create_all()
        mail.init_app(app)
    app.run(debug=True)