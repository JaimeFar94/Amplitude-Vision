from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from flask_mail import Mail
from flask_mail import Message
from flask_wtf.csrf import CSRFProtect  
from flask_migrate import Migrate

app = Flask(__name__ , template_folder='templates')
app.secret_key = '876-105-169'

#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/medico'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://u3dchap7tdasok:p71f99aced8d869c27dc376cea7ce457648713c7f898a4c518c9263c625f6ccdb@c9uss87s9bdb8n.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d9ccqs8833erdf'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
ma = Marshmallow(app)


migrate = Migrate(ma, db)

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
