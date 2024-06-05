from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from flask_mail import Mail
from flask_mail import Message
from flask_wtf.csrf import CSRFProtect  


app = Flask(__name__ , template_folder='templates')
app.secret_key = '876-105-169'

#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/medico'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://b8930d4e12b1e6:e55c1cfd@us-cluster-east-01.k8s.cleardb.net/heroku_e842630e704b3bc?reconnect=true'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


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


if __name__ == '__main__':  # Se tiene un condicional para verificar que si se esta en el archivo de ejecución y no un modulo
    with app.app_context():
        db.create_all()
        mail.init_app(app)
    app.run(debug=True)
