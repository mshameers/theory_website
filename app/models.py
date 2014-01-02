from app import db
import datetime

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(180), unique=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))

    def __init__(self, name):
        self.name = name

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return '<Author %r>' % self.name

class Publisher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(180), unique=True)
    address = db.Column(db.Text)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))

    def __init__(self, name, address):
        self.name = name
        self.address = address

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return '<Publisher %r>' % self.name
        
categories = db.Table('categories',
    db.Column('category_id', db.Integer, db.ForeignKey('category.id')),
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'))
)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    shortName = db.Column(db.String(5)) 

    def __init__(self, name, shortName=None):
        self.name = name
        if not shortName:
            self.shortName = self.name[:3]
        else:
            self.shortName = shortName

    def __unicode__(self):
        return self.name, self.shortName

    def __repr__(self):
        return '<Category %r: %s>' % (self.name, self.shortName)


class Book(db.Model):
    PER_PAGE_POST = 30

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, unique=True)
    title = db.Column(db.String, nullable=True)
    author = db.relationship('Author', backref='books',
        lazy='dynamic')
    publisher = db.relationship('Publisher', backref='books',
        lazy='dynamic')
    edition = db.Column(db.Integer)
    price = db.Column(db.Integer)
    enteredDate = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    endDate = db.Column(db.DateTime)
    category = db.relationship('Category', secondary=categories,
        backref=db.backref('books', lazy='dynamic'))
    isActive = db.Column(db.Boolean)

    def __init__(self, number, title, author, publisher, edition, price, category, 
        isActive=True):

        self.number = number
        self.title = title
        self.author = author
        self.publisher = publisher
        self.edition = edition
        self.price = price
        self.enteredDate = datetime.datetime.utcnow()
        self.endDate = self.enteredDate + datetime.timedelta(6*365/12)
        self.category = category
        self.isActive = isActive

    def __repr__(self):
        return u'<Book(%s,%s,Category %r)>' % (self.id, self.name, self.category)

    def to_json(self):
        return {
            'id': self.id,
            'number': self.number,
            'title': self.title,
            'author': self.author,
            'publisher': self.publisher,
            'category': self.category,
            'isActive': self.isActive,
            'endDate': self.endDate.isoformat()
        }
