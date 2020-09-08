from . import DB

class Doctor(DB.Model):
  __table__ = DB.Model.metadata.tables['doctors']

  def __repr__(self):
    return '<Doctor %r>' % self.id
