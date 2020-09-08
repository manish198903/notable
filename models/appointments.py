from . import DB

class Appointment(DB.Model):
  __table__ = DB.Model.metadata.tables['appointments']

  def __repr__(self):
    return '<Appointment %r>' % self.id
