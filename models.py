from app import db

class Base(db.Model):
    __abstract__ = True

    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, self.id)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Quote(Base):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(50), nullable=False)

if __name__ == '__main__':
    print("Creating database tables...", end='')
    db.create_all()
    print(" Done!")

    print("Adding sample data...", end='')
    quote1 = Quote(content='Trouble is only opportunity in work clothes.', author='Henry J. Kaiser')
    quote2 = Quote(content='True happiness arises, in the first place, from the enjoyment of oneself, and in the next, from the friendship and conversation of a few select companions.', author='Joseph Addison')
    quote3 = Quote(content='The only way to have a friend is to be one.', author='Ralph Waldo Emerson')
    db.session.add_all([quote1, quote2, quote3])
    db.session.commit()
    print(" Done!")