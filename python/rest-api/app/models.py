from app import db


class Task(db.Model):
		id = db.Column(db.Integer, primary_key=True)
		title = db.Column(db.String(64), index=True, unique=True)
		description = db.Column(db.String(180))
		done = db.Column(db.Boolean, default=False)

		def __repr__(self):
				return '<Task %r>' % (self.title)
