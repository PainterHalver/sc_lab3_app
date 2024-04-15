from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Base(db.Model):
    __abstract__ = True

    def __repr__(self):
        return "<%s %r>" % (self.__class__.__name__, self.id)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def save(self):
        db.session.add(self)
        db.session.commit()


class Quote(Base):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(50), nullable=False)


class CSV(Base):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)
    generated_at = db.Column(db.DateTime, nullable=False)
