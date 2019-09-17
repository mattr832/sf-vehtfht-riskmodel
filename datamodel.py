from dbapp import db
 
 
class Response(db.Model):
    __tablename__ = "responses"
 
    id = db.Column(db.Integer, primary_key=True)
    riskscore = db.Column(db.Integer)
 
    def __repr__(self):
        return "<Response: {}>".format(self.name)