import os
import secrets
from tkinter import Image

import pymysql
from flask import Flask, render_template, url_for, redirect, session, request
from flask import Response
from flask_wtf import FlaskForm, file
from werkzeug.utils import secure_filename
from wtforms import StringField,SubmitField,RadioField,TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired

UPLOAD_FOLDER = 'static/assets/blog-pics'
app = Flask(__name__)
app.config['SECRET_KEY']='some_random_secret'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

class BlogForm(FlaskForm):
    name=StringField('Enter your Name',validators=[InputRequired()])
    blog=TextAreaField('Anything else you want to tell us ?')

    submit=SubmitField('Submit')

connection = pymysql.connect(host="localhost", user="root", password="", database="travel")
cursor = connection.cursor()

@app.route('/',methods=['GET','POST'])
@app.route('/index', methods=['GET','POST'])
def home():

    return render_template('index.html')



@app.route('/blog_page', methods=['GET','POST'])
def blogs():
    form = BlogForm()

    if form.validate_on_submit():
        session['name'] = form.name.data
        session['blog'] = form.blog.data
        #save_picture(form_picture=)
        f = request.files['file']
        pic1 = f.save(f.filename)
        #filename = secure_filename(f.filename)
        #f.save(os.path.join(app.config[filename]))
        #f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # f.save(secure_filename(f.filename))
        #filename = 'UPLOAD_FOLDER' + filename
        #return redirect(url_for("blogs", filename=filename))
    return render_template('travel_blogs.html', form=form)

# @app.route('/about/<filename>')
# def uploaded_file(filename):
#     filename = 'http://127.0.0.1:5000/about/' + filename
#     return render_template('travel_blogs.html', filename = filename)

# def save_picture(form_picture):
#     random_hex = secrets.token_hex(8)
#     _, f_ext = os.path.splitext(form_picture.filename)
#     picture_fn = random_hex + f_ext
#     picture_path = os.path.join(app.root_path, 'static/assets/blog_pics', picture_fn)
#
#     output_size = (125, 125)
#     i = Image.open(form_picture)
#     i.thumbnail(output_size)
#     i.save(picture_path)
#
#     return picture_fn

@app.route('/about', methods=['GET', 'POST'])
def about():
    if request.method == 'POST':
        f = request.files['file']
        #f.save(f.filename)
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #f.save(secure_filename(f.filename))
        return render_template("about.html", name=f.filename)
    return render_template('about.html')


@app.route('/signup', methods =['GET', 'POST'])
def signup():
    return render_template('signup.html')

@app.route('/login', methods =['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        data = request.form['data']

        cursor.execute("INSERT INTO contacts (name,email,phone,data) VALUES (%s,%s,%s,%s)", (name,email,phone,data))
        connection.commit()

        return "success"
        return redirect(url_for('contact'))
    return render_template('contact.html')

if __name__ == '__main__':
   app.run(debug = True, port=5051)