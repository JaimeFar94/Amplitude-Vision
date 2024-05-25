import pandas as pd
from pandas_profiling import ProfileReport
from flask import render_template, request, send_file
from extension import app, db, ma ,  csrf , mail , Message 
import ydata_profiling

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
    

    def __init__(self, fecha ,sede, montura, cantidad_montura, marca, referencia, color, cordones,cantidad_cordones ,estuches,cantidad_estuches, stopper,cantidad_stopper ):
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
        self.cantidad_stopper  = cantidad_stopper 
        

    class TaskSchema(ma.Schema):
        class Meta:
            fields = ('id','fecha' , 'sede', 'montura','cantidad_montura' , 'marca', 'referencia', 'color', 'cordones', 'cantidad_cordones' , 'estuches', 'cantidad_estuches' ,  'stopper', 'cantidad_stopper' ,'numero_recibo')
class recibo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha_compra = db.Column(db.DateTime)
    numero_recibo = db.Column(db.Integer)
    documento = db.Column(db.Integer)
    nombre_paciente = db.Column(db.String(200))
    direccion= db.Column(db.String(200))
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
    valor_unitario = db.Column(db.Integer)
    valor_unitario_1 = db.Column(db.Integer)
    valor_unitario_2 = db.Column(db.Integer)
    valor_unitario_3 = db.Column(db.Integer)
    valor_unitario_4 = db.Column(db.Integer)
    valor_unitario_5 = db.Column(db.Integer)
    valor_unitario_6 = db.Column(db.Integer)
    valor_unitario_7 = db.Column(db.Integer)
    valor_total = db.Column(db.Integer) 
    valor_total_1 = db.Column(db.Integer)
    valor_total_2 = db.Column(db.Integer)
    valor_total_3 = db.Column(db.Integer)
    valor_total_4 = db.Column(db.Integer)
    valor_total_5 = db.Column(db.Integer)
    valor_total_6 = db.Column(db.Integer)
    valor_total_7 = db.Column(db.Integer) # Corregido aquí
    total = db.Column(db.Integer)

    def __init__(self, fecha_compra, numero_recibo, documento, nombre_paciente, direccion, telefono, correo, cantidad, cantidad_1, cantidad_2, cantidad_3, cantidad_4, cantidad_5, cantidad_6, cantidad_7, detalle,detalle_1,detalle_2,detalle_3,detalle_4,detalle_5,detalle_6,detalle_7, valor_unitario, valor_unitario_1, valor_unitario_2, valor_unitario_3, valor_unitario_4, valor_unitario_5, valor_unitario_6, valor_unitario_7, valor_total, valor_total_1, valor_total_2, valor_total_3, valor_total_4, valor_total_5, valor_total_6, valor_total_7, total):
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
         fields = ('id', 'fecha_compra', 'nombre_paciente', 'numero_recibo', 'documento', 'direccion', 'telefono', 'correo', 'cantidad', 'cantidad_1', 'cantidad_2', 'cantidad_3', 'cantidad_4', 'cantidad_5', 'cantidad_6', 'cantidad_7', 'detalle','detalle_1','detalle_2','detalle_3','detalle_4','detalle_5','detalle_6','detalle_7', 'valor_unitario', 'valor_unitario_1', 'valor_unitario_2', 'valor_unitario_3', 'valor_unitario_4', 'valor_unitario_5', 'valor_unitario_6', 'valor_unitario_7', 'valor_total', 'valor_total_1', 'valor_total_2', 'valor_total_3', 'valor_total_4', 'valor_total_5', 'valor_total_6', 'valor_total_7', 'total')
#Agregar los datos dentro del inventario
@app.route("/inventory", methods=['GET' ,'POST'])
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
                fecha = fecha,
                sede=sede,
                montura=montura,
                cantidad_montura=cantidad_montura,
                marca=marca,
                referencia=referencia,
                color=color,
                cordones=cordones,
                cantidad_cordones = cantidad_cordones,
                estuches=estuches,
                cantidad_estuches = cantidad_estuches,
                stopper=stopper,
                cantidad_stopper= cantidad_stopper,
            )
            db.session.add(inventario)
            db.session.commit()
            print('Inventario agregado correctamente')
            
            return render_template('inventory.html')
    else:
        print('Inventario no Disponible')
        return render_template('inventory.html')

#Export del inventario
@app.route('/export')
def export():
    data = Inventory.query.all()
    df = pd.DataFrame([[item.id, item.fecha ,item.sede, item.montura, item.cantidad_montura, item.marca, item.referencia, item.color, item.cordones,
                        item.cantidad_cordones, item.estuches, item.cantidad_estuches, item.stopper, item.cantidad_stopper
                        ] for item in data],
                      columns=['ID', 'Fecha' ,'Sede', 'Montura', 'Cantidad Montura', 'Marca', 'Referencia', 'Color', 'Cordones', 'Cantidad Cordones', 'Estuches', 'Cantidad Estuches', 'Stopper', 'Cantidad Stopper'])

    # Guardar CSV
    csv_path = 'C:/Users/J-far/Desktop/Proyecto Ocampo/src/informes/inventory.csv'  
    df.to_csv(csv_path, index=False)

    # Generar perfil de datos
    profile = ProfileReport(df, title='Perfil de Datos')
    profile_html_path = 'C:/Users/J-far/Desktop/Proyecto Ocampo/src/informes/reporte.html'  
    profile.to_file(profile_html_path)

    # Redireccionar a inventory.html después de la exportación
    print('Se Genero Informe de Manera Correcta')
    return render_template('inventory.html')


#Busqueda por # recibo

@app.route('/search', methods=['GET' ,'POST'])
def search():
    if request.method == 'POST':
        numero_recibo = request.form['recibo']
        # Realiza la búsqueda en la base de datos usando el número de recibo
        inventory_data = recibo.query.filter_by(numero_recibo=numero_recibo).all()
        print("tu información" , inventory_data)
        # Pasa 'recibo' como parte del contexto
        return render_template('search.html', inventory_data=inventory_data, recibo=numero_recibo) 
    else:
        print('Información no disponible')
    return render_template('search.html')



@app.route('/recibo', methods=['GET', 'POST'])
@csrf.exempt
def compra():
    if request.method == 'POST':
        # Aquí va el código para manejar el formulario POST
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

        msg = Message('El recibo ha sido enviado satisfactoriamente',
                      sender=app.config['MAIL_PASSWORD'],
                      recipients=[compra.correo])
        msg.html = render_template('email_compra.html', compra=compra)
        mail.send(msg)
        print('El correo se envió con éxito')
        return render_template('recibo.html')
    else:
        # Si la solicitud no es un POST, simplemente renderiza el template sin la variable compra
        print('Recibo no enviado')
        return render_template('recibo.html')