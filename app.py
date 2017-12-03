from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField
import bs4 as bs
import urllib.request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'


class Form(FlaskForm):
	url = StringField('url')


class FormHTML(FlaskForm):
	url = StringField('url')


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/form', methods=['GET', 'POST'])
def form():
	form = Form()

	if form.validate_on_submit():
		sauce = urllib.request.urlopen(form.url.data).read()
		soup = bs.BeautifulSoup(sauce, 'lxml')

		paragraph_list = []

		for paragraph in soup.find_all('p'):
			paragraph_list.append(paragraph.get_text())

		return render_template('output.html', url_data=form.url.data, paragraph_list=paragraph_list)

	return render_template('form.html', form=form)

@app.route('/form-html', methods=['GET', 'POST'])
def form_html():
	form = FormHTML()

	if form.validate_on_submit():
		sauce = urllib.request.urlopen(form.url.data).read()
		soup = bs.BeautifulSoup(sauce, 'lxml')

		soup = soup.body

		return render_template('output-html.html', url_data=form.url.data, soup=soup)

	return render_template('form-html.html', form=form)


if __name__ == '__main__':
    app.run()
