from flask_restplus import Namespace, Resource, fields, inputs
# from flask import current_app as app
from models import DB
from models.appointments import Appointment
from datetime import date, datetime
from sqlalchemy import cast, Date

ns = Namespace('appointments', description='Appointments related operations')

appointment = ns.model('Appointment', {
  'id': fields.Integer(readonly=True, description='appointment id'),
  'doctor_id': fields.Integer(required=True, description='doctor id'),
  'patient_first_name': fields.String(required=True, description='first name of patient'),
  'patient_last_name': fields.String(required=True, description='last name of patient'),
  'time': fields.DateTime(required=True, description='visit time', dt_format='iso8601', example='2020-09-08T05:02:39.077'),
  'kind': fields.String(required=True, description='kind'),
  'created_at': fields.DateTime(readonly=True, description='creation time of appointment record'),
  'updated_at': fields.DateTime(readonly=True, description='update time of appointment record'),
})

get_appointments_parser = ns.parser()
get_appointments_parser.add_argument('doctor_id', type=int, help='doctor id', location='args', required=False)
get_appointments_parser.add_argument('date', type=inputs.date_from_iso8601, help='date', location='args', required=False)

@ns.route('/')
class AppointmentListController(Resource):
  '''Shows a list of all appointments'''

  @ns.doc('list_appointments')
  @ns.marshal_list_with(appointment)
  @ns.expect(get_appointments_parser)
  def get(self):
    '''List all appointments'''
    args = get_appointments_parser.parse_args()
    # app.logger.info(args)
    result = Appointment.query
    if args['doctor_id'] is not None:
      result = result.filter_by(doctor_id=args['doctor_id'])

    if args['date'] is not None:
      result = result.filter(cast(Appointment.time, Date)==args['date'])

    return result.all()



  @ns.doc('create_appointment')
  @ns.expect(appointment)
  @ns.marshal_with(appointment, code=201)
  def post(self):
    '''Create a new appointment'''
    data = ns.payload
    appointment_time = datetime.fromisoformat(data['time']).replace(second=0, microsecond=0)

    appointment_minutes = appointment_time.minute
    if int(appointment_minutes) % 15 != 0:
      ns.abort(400, "minutes {} not at 15 min boundary".format(int(appointment_minutes)))

    if 3 <= Appointment.query.filter_by(time=appointment_time).count():
      ns.abort(400, "3 appointments for doctor {} already booked at {}".format(data['doctor_id'], data['time']))

    new_appointment = Appointment(doctor_id=data['doctor_id'],
                                  patient_first_name=data['patient_first_name'],
                                  patient_last_name=data['patient_last_name'],
                                  time=appointment_time,
                                  kind=data['kind'])
    DB.session.add(new_appointment)
    DB.session.commit()
    return new_appointment, 201

@ns.route('/<int:id>')
@ns.param('id', 'The appointment identifier')
@ns.response(404, 'Appointment not found')
class AppointmentController(Resource):
  '''Show a single appointment and allow delete on it'''

  @ns.doc('get_appointment')
  @ns.marshal_with(appointment)
  def get(self, id):
    '''Fetch a appointment given its identifier'''
    appointment = Appointment.query.filter_by(id=id).first()
    if appointment is None:
      ns.abort(404, "Appointment {} doesn't exist".format(id))

    return appointment


  @ns.doc('delete_appointment')
  @ns.response(204, 'Appointment deleted')
  def delete(self, id):
    '''Delete a appointment given its identifier'''
    # https://stackoverflow.com/questions/19243964/sqlalchemy-delete-doesnt-cascade
    Appointment.query.filter_by(id=id).delete()
    DB.session.commit()
    return '', 204
