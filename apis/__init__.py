from flask_restplus import Api

from .doctors import ns as doctors
from .appointments import ns as appointments

api = Api(
    title='Notable Health API',
    version='1.0',
    description='API to manage doctors and their appointments',
    prefix='/api/v1'
)

api.add_namespace(doctors, path='/doctors')
api.add_namespace(appointments, path='/appointments')
