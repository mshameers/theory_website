from flask.ext.wtf import Form
from wtforms.fields import TextField, TextAreaField, \
    HiddenField, PasswordField, SelectField, IntegerField, StringField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import Required, Length
from app.utils import is_name
from app import db
from models import Author, Publisher, Category

class BookForm(Form):

	title = TextField('Title', [
	    Required(),
	    Length(min=2, max=150),
	    is_name,
	])
	author = SelectField('Author', coerce=int, choices=[(i.id, i.name) for i in Author.query.all()])
	publisher = SelectField('Publisher', coerce=int, choices=[(i.id, i.name) for i in Publisher.query.all()])
	category = SelectField('Category', coerce=int, choices=[(i.id, i.name) for i in Category.query.all()])
	# author = QuerySelectField(query_factory=Author.query.all,
 #                            get_pk=lambda a: a.id,
 #                            get_label=lambda a: a.name)
	# publisher = QuerySelectField(query_factory=lambda: db.session.query(Publisher),#Publisher.query.all,
 #                            get_pk=lambda a: a.id,
 #                            get_label=lambda a: a.name)
	edition = IntegerField('Edition')
	price = IntegerField('Price')
	# category =  QuerySelectField('category', query_factory=lambda: db.session.query(Category),#Category.query.all,
 #                            get_pk=lambda a: a.id,
 #                            get_label=lambda a: a.name)

class CategoryForm(Form):

	name = StringField('Name', [
	    Required(),
	    Length(min=2, max=150),
	    is_name,
	])
	shortName = StringField('Short Name', [
	    Required(),
	    Length(min=2, max=5),
	    is_name,
	])


class AuthorForm(Form):

	name = StringField('Name', [
	    Required(),
	    Length(min=2, max=150),
	    is_name,
	])


class PublisherForm(Form):

	name = StringField('Name', [
	    Required(),
	    Length(min=2, max=150),
	    is_name,
	])
	address = TextAreaField('Address', [
	    Required(),
	    Length(min=2)
	])