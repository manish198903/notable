from flask_restplus import Namespace, Resource, fields
from models import DB
from models.doctors import Doctor
ns = Namespace('doctors', description='Doctors related operations')

doctor = ns.model('Doctor', {
  'id': fields.Integer(readonly=True, description='id of doctor'),
  'first_name': fields.String(required=True, description='first name of doctor'),
  'last_name': fields.String(required=True, description='last name of doctor'),
  'created_at': fields.DateTime(readonly=True, description='creation time of doctor record'),
  'updated_at': fields.DateTime(readonly=True, description='update time of doctor record'),
})

@ns.route('/')
class DoctorListController(Resource):
  '''Shows a list of all doctors, and lets you POST to add a new doctor'''
  
  @ns.doc('list_doctors')
  @ns.marshal_list_with(doctor)
  def get(self):
    '''List all doctors'''
    return Doctor.query.all()

  @ns.doc('create_doctor')
  @ns.expect(doctor)
  @ns.marshal_with(doctor, code=201)
  def post(self):
    '''Create a new doctor'''
    data = ns.payload
    new_doctor = Doctor(first_name=data['first_name'], last_name=data['last_name'])
    DB.session.add(new_doctor)
    DB.session.commit()
    return new_doctor, 201


@ns.route('/<int:id>')
@ns.param('id', 'The doctor identifier')
@ns.response(404, 'Doctor not found')
class DoctorController(Resource):
  '''Show a single doctor and allow delete on it'''

  @ns.doc('get_doctor')
  @ns.marshal_with(doctor)
  def get(self, id):
    '''Fetch a doctor given its identifier'''
    doctor = Doctor.query.filter_by(id=id).first()
    if doctor is None:
      ns.abort(404, "Doctor {} doesn't exist".format(id))

    return doctor


  @ns.doc('delete_doctor')
  @ns.response(204, 'Doctor deleted')
  def delete(self, id):
    '''Delete a doctor given its identifier'''
    # https://stackoverflow.com/questions/19243964/sqlalchemy-delete-doesnt-cascade
    Doctor.query.filter_by(id=id).delete()
    DB.session.commit()
    return '', 204
