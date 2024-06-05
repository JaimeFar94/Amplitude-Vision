from flask import render_template, request, session, Response ,flash
from extension import app, db, ma , os , mail , Message  , csrf , Migrate
from functools import wraps
import hashlib
from datetime import datetime
from inventory import Inventory, recibo
import pandas as pd



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
    tipo_lente = db.Column(db.String(50))
    montura = db.Column(db.String(50))
    material = db.Column(db.String(50))
    filtro = db.Column(db.String(50))
    color = db.Column(db.String(50))
    observacion = db.Column(db.String(100))
    paciente_documento = db.Column(db.Integer, db.ForeignKey(
        'paciente.documento', onupdate='CASCADE', ondelete='CASCADE'))

    paciente = db.relationship(
        'paciente', backref=db.backref('MovConsulta', lazy=True))

    def __init__(self, mov_consulta=None, ulti_consulta=None, esfera=None, cilindro=None, eje=None, dp=None, vl20=None, vp20=None, add_0=None, esfera_1=None, cilindro_1=None, eje_1=None, dp_1=None, vl20_1=None,
                 vp20_1=None, add_1=None, tipo_lente=None, montura=None, material=None, filtro=None, color=None, observacion=None):
        self.mov_consulta = mov_consulta
        self.ulti_consulta = ulti_consulta
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
        self.tipo_lente = tipo_lente
        self.montura = montura
        self.material = material
        self.filtro = filtro
        self.color = color
        observacion = observacion


class TaskSchema(ma.Schema):
    class Meta:
        fields = ('mov_consulta', 'ulti_consulta', 'esfera', 'cilindro', 'eje', 'dp', 'vl20', 'vp20', 'add_0', 'esfera_1', 'cilindro_1', 'eje_1',
                  'dp_1', 'vl20_1', 'vp20_1', 'add_1', 'tipo_lente', 'montura', 'material', 'filtro', 'color', 'observacion')


task_schema = TaskSchema()
task_schema = TaskSchema(many=True)


# Vista

class Vista(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vision_lejana = db.Column(db.String(40))
    vision_proxima = db.Column(db.String(40))
    ducciones_od = db.Column(db.String(40))
    ducciones_oi = db.Column(db.String(40))
    ppc_od = db.Column(db.String(40))
    ppc_oi = db.Column(db.String(40))
    ojo_derecho = db.Column(db.String(30))
    ojo_izquierdo = db.Column(db.String(30))
    ojo_drc_querato = db.Column(db.String(30))
    ojo_izq_querato = db.Column(db.String(30))
    ojo_drc_refac = db.Column(db.String(30))
    ojo_izq_refac = db.Column(db.String(30))
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
    paciente_documento = db.Column(db.Integer, db.ForeignKey(
        'paciente.documento', onupdate='CASCADE', ondelete='CASCADE'))

    paciente = db.relationship(
        'paciente', backref=db.backref('vista', lazy=True))


class TaskSchema(ma.Schema):
    class Meta:
        fields = ('vision_lejana', 'vision_proxima', 'ducciones_od', 'ducciones_oi', 'ppc_od', 'ppc_oi', 'ojo_derecho', 'ojo_izquierdo', 'ojo_drc_querato',
                  'ojo_izq_querato', 'ojo_drc_refac', 'ojo_izq_refac', 'esfera_retino', 'cilindro_retino', 'eje_retino_1', 'dp_retino_1', 'vl20_retino_1',
                  'vp20_retino_1', 'add_retino_1')


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
                return render_template('menu.html', username=username)
            else:
                print('Usuario o contraseña incorrectos')
        else:
            print('Usuario o contraseña incorrectos')

    return render_template('login.html')


@app.route("/menu")
@login_required
def menu():
    user_authenticated = get_user_authenticated()
    username = request.args.get('username', '')
    return render_template('menu.html', username=username, user_authenticated=user_authenticated)


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
        tipo_lente = request.form['tipo_lente']
        montura = request.form['montura']
        material = request.form['material']
        filtro = request.form['filtro']
        color = request.form['color']
        observacion = request.form['obs']

        # vista

        vision_lejana = request.form['vision_lejos']
        vision_proxima = request.form['vision_proxima']
        ducciones_od = request.form['ducciones_od']
        ducciones_oi = request.form['ducciones_oi']
        ppc_od = request.form['ppc_od']
        ppc_oi = request.form['ppc_oi']
        ojo_derecho = request.form['ojo_derecho']
        ojo_izquierdo = request.form['ojo_izquierdo']
        ojo_drc_querato = request.form['ojo_dere']
        ojo_izq_querato = request.form['ojo_izqui']
        ojo_drc_refac = request.form['ojo_derch']
        ojo_izq_refac = request.form['ojo_izquier']
        esfera_retino = request.form['esfera']
        cilindro_retino = request.form['cilindro']
        eje_retino = request.form['eje']
        dp_retino = request.form['dp']
        vl20_retino = request.form['vl20']
        vp20_retino = request.form['vp20']
        add_retino = request.form['add']
        esfera_retino_1 = request.form['esfera_1']
        cilindro_retino_1 = request.form['cilindro_1']
        eje_retino_1 = request.form['eje_1']
        dp_retino_1 = request.form['dp_1']
        vl20_retino_1 = request.form['vl20_1']
        vp20_retino_1 = request.form['vp20_1']
        add_retino_1 = request.form['add_1']

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
            tipo_lente=tipo_lente,
            montura=montura,
            material=material,
            filtro=filtro,
            color=color,
            observacion=observacion,
        )
        nueva_consulta.paciente = user
        db.session.add(nueva_consulta)
        db.session.commit()

        nueva_vista = Vista(
            vision_lejana=vision_lejana,
            vision_proxima=vision_proxima,
            ducciones_od=ducciones_od,
            ducciones_oi=ducciones_oi,
            ppc_od=ppc_od,
            ppc_oi=ppc_oi,
            ojo_derecho=ojo_derecho,
            ojo_izquierdo=ojo_izquierdo,
            ojo_drc_querato=ojo_drc_querato,
            ojo_izq_querato=ojo_izq_querato,
            ojo_drc_refac=ojo_drc_refac,
            ojo_izq_refac=ojo_izq_refac,
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
            add_retino_1=add_retino_1
        )
        nueva_vista.paciente = user
        db.session.add(nueva_vista)
        db.session.commit()

        print('Paciente Registrado Correctamente')
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
        # Mov-Consulta
        editar_movconsulta.mov_consulta = request.form['mov_consulta']
        editar_movconsulta.ulti_consulta = request.form['ulti_consulta']
        editar_movconsulta.esfera = request.form['esfera']
        editar_movconsulta.cilindro = request.form['cilindro']
        editar_movconsulta.eje = request.form['eje']
        editar_movconsulta.dp = request.form['dp']
        editar_movconsulta.vl20 = request.form['vl20']
        editar_movconsulta.vp20 = request.form['vp20']
        editar_movconsulta.add_0 = request.form['add_0']
        editar_movconsulta.esfera_1 = request.form['esfera_1']
        editar_movconsulta.cilindro_1 = request.form['cilindro_1']
        editar_movconsulta.eje_1 = request.form['eje_1']
        editar_movconsulta.dp_1 = request.form['dp_1']
        editar_movconsulta.vl20_1 = request.form['vl20_1']
        editar_movconsulta.vp20_1 = request.form['vp20_1']
        editar_movconsulta.tipo_lente = request.form['tipo_lente']
        editar_movconsulta.montura = request.form['montura']
        editar_movconsulta.material = request.form['material']
        editar_movconsulta.filtro = request.form['filtro']
        editar_movconsulta.color = request.form['color']

        # vista

        editar_vista.vision_lejana = request.form['vision_lejos']
        editar_vista.vision_proxima = request.form['vision_proxima']
        editar_vista.duccion_od = request.form['ducciones_od']
        editar_vista.duccion_oi = request.form['ducciones_oi']
        editar_vista.ppc_od = request.form['ppc_od']
        editar_vista.ppc_oi = request.form['ppc_oi']
        editar_vista.ojo_derecho = request.form['ojo_derecho']
        editar_vista.ojo_izquierdo = request.form['ojo_izquierdo']
        editar_vista.ojo_drc_querato = request.form['ojo_dere']
        editar_vista.ojo_izq_querato = request.form['ojo_izqui']
        editar_vista.ojo_drc_refac = request.form['ojo_derch']
        editar_vista.ojo_izq_refac = request.form['ojo_izquier']
        editar_vista.esfera_retino = request.form['esfera']
        editar_vista.cilindro_retino = request.form['cilindro']
        editar_vista.eje_retino = request.form['eje']
        editar_vista.dp_retino = request.form['dp']
        editar_vista.vl20_retino = request.form['vl20']
        editar_vista.vp20_retino = request.form['vp20']
        editar_vista.add_retino = request.form['add']
        editar_vista.esfera_retino_1 = request.form['esfera_1']
        editar_vista.cilindro_retino_1 = request.form['cilindro_1']
        editar_vista.eje_retino_1 = request.form['eje_1']
        editar_vista.dp_retino_1 = request.form['dp_1']
        editar_vista.vl20_retino_1 = request.form['vl20_1']
        editar_vista.vp20_retino_1 = request.form['vp20_1']
        editar_vista.add_retino_1 = request.form['add_1']

        db.session.commit()
        print('El usuario se ha editado correctamente')
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

            # Guardar registro de eliminación
        registro_eliminacion = delete(
             id = paciente_a_eliminar.id,
	         eliminado = paciente_a_eliminar.eliminado,
	        fecha_eliminacion = datetime.now(),
	        nombre_eliminado = paciente_a_eliminar.nombre_eliminado,
            documento_eliminado = paciente_a_eliminar.documento_eliminado,
            usuario=user_authenticated
        )
        db.session.add(registro_eliminacion)
        db.session.commit()

        print('El paciente ha sido eliminado correctamente')
    else:
        print('No se encontró al paciente')

    
    return render_template('consult.html', user_authenticated=user_authenticated)


if __name__ == '__main__':  # Se tiene un condicional para verificar que si se esta en el archivo de ejecución y no un modulo
    with app.app_context():
        db.create_all()
        mail.init_app(app)
    app.run(debug=True)
