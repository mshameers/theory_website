from flask import redirect, url_for, session, flash, render_template, request
from models import Book, Category, Author, Publisher
from app import app, db
from forms import BookForm, CategoryForm, AuthorForm, PublisherForm


@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/books', defaults={'page': 1, 'cat': None})
@app.route('/books/<int:page>/cat/<int:cat>')
def books(page, cat):
	if cat:
		category = Category.query.get(cat)
		print category.books, 'category'
		books = category.books.filter_by(isActive=True).all()
		# books = books.filter_by(category=category)
	else:
		books = Book.query.filter_by(isActive=True)
	
	pagination = books.order_by(Book.enteredDate.desc()) \
	                   .paginate(page, Book.PER_PAGE_POST, False)
	return render_template('books.html', pagination=pagination)

@app.route('/book/', methods=['GET', 'POST'])
# @login_required
def newBook():
	form = BookForm(formdata=request.form or None)
	print form.category.data, form.publisher.data, form.author.data
	if request.method == 'POST':
		if request.form and form.validate():
			category = Category.query.get(form.category.data)
			publisher = Publisher.query.get(form.publisher.data)
			author = Author.query.get(form.author.data)
			number = len(category.books.all()) + 1
			categoryShortName = category.shortName
			print number, categoryShortName, '###number###', form.category.data
			b = Book(number=number,
					title=form.title.data,
					author=[author],
					category=[category],
					publisher=[publisher],
					edition=form.edition.data,
					price=form.price.data,
					)
			#db.session.add(b)
			db.session.commit()
			return redirect(url_for('books', page=1))
		else:
		    flash('There was an error with your input: %s' % form.errors)
		    return redirect(url_for('newBook'))
		return redirect(redirectUrl)
	else:
		return render_template('newBook.html', form=form)


@app.route('/category/', methods=['GET', 'POST'])
# @login_required
def category():
	form = CategoryForm(formdata=request.form or None)
	if request.method == 'POST':
		if request.form and form.validate():
			c = Category(name=form.name.data, shortName=form.shortName.data)
			db.session.add(c)
			db.session.commit()
			return redirect(url_for('category'))
		else:
		    flash('There was an error with your input: %s' % form.errors)
		    return redirect(url_for('category'))
		
	else:
		categories = Category.query.all()
		return render_template('category.html', categories=categories, form=form)


@app.route('/author/', methods=['GET', 'POST'])
# @login_required
def author():
	form = AuthorForm(formdata=request.form or None)
	if request.method == 'POST':
		if request.form and form.validate():
			a = Author(name=form.name.data)
			db.session.add(a)
			db.session.commit()
			return redirect(url_for('author'))
		else:
		    flash('There was an error with your input: %s' % form.errors)
		    return redirect(url_for('author'))
		
	else:
		authors = Author.query.all()
		return render_template('author.html', authors=authors, form=form)


@app.route('/publisher/', methods=['GET', 'POST'])
# @login_required
def publisher():
	form = PublisherForm(formdata=request.form or None)
	if request.method == 'POST':
		if request.form and form.validate():
			p = Publisher(name=form.name.data, address=form.address.data)
			db.session.add(p)
			db.session.commit()
			return redirect(url_for('publisher'))
		else:
		    flash('There was an error with your input: %s' % form.errors)
		    return redirect(url_for('publisher'))
		
	else:
		publishers = Publisher.query.all()
		return render_template('publisher.html', publishers=publishers, form=form)