from __main__ import app
from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy(app)
DB.Model.metadata.reflect(DB.engine)

