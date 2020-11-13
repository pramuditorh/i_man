from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from flask_wtf.file import FileAllowed, FileField, FileRequired
from app.models import User
from app import images
import phonenumbers

class PatchCordForm(FlaskForm):
    type = SelectField('Type', validators=[DataRequired()], choices=[('SC-SC', 'sc-sc'), ('SC-LC', 'sc-lc'), ('LC-LC', 'lc-lc')], default='SC-SC')
    length = StringField('Length', validators=[DataRequired()])
    note = StringField('Deskripsi/Status Produk', validators=[DataRequired()])
    in_record_of_transfer = FileField('Berita Acara Masuk', validators=[FileAllowed(images, 'Images only!')])
    out_record_of_transfer = FileField('Berita Acara Keluar', validators=[FileAllowed(images, 'Images only!')])
    submit = SubmitField('Simpan')

class SFPForm(FlaskForm):
    type = SelectField('Type', validators=[DataRequired()], choices=[('SFP', 'sfp'), ('XFP', 'xfp'), ('CFP', 'cfp')], default='SFP')
    length = StringField('Length', validators=[DataRequired()])
    capacity = StringField('Capacity', validators=[DataRequired()])
    serial_number = StringField('Serial Number', validators=[DataRequired()])
    product_number = StringField('Product Number', validators=[DataRequired()])
    note = StringField('Deskripsi/Status Produk', validators=[DataRequired()])
    in_record_of_transfer = FileField('Berita Acara Masuk', validators=[FileAllowed(images, 'Images only!')])
    out_record_of_transfer = FileField('Berita Acara Keluar', validators=[FileAllowed(images, 'Images only!')])
    submit = SubmitField('Simpan')

class IOMForm(FlaskForm):
    type = SelectField('Type', validators=[DataRequired()], choices=[('IOM', 'iom'), ('IMM', 'imm')], default='IOM')
    note = StringField('Deskripsi/Status Produk', validators=[DataRequired()])
    in_record_of_transfer = FileField('Berita Acara Masuk', validators=[FileAllowed(images, 'Images only!')])
    out_record_of_transfer = FileField('Berita Acara Keluar', validators=[FileAllowed(images, 'Images only!')])
    submit = SubmitField('Simpan')

class MDAForm(FlaskForm):
    type = SelectField('Type', validators=[DataRequired()], choices=[('M2O', 'm2o'), ('M2', 'm2')], default='M2O')
    capacity = StringField('Capacity', validators=[DataRequired()])
    note = StringField('Deskripsi/Status Produk', validators=[DataRequired()])
    in_record_of_transfer = FileField('Berita Acara Masuk', validators=[FileAllowed(images, 'Images only!')])
    out_record_of_transfer = FileField('Berita Acara Keluar', validators=[FileAllowed(images, 'Images only!')])
    submit = SubmitField('Simpan')