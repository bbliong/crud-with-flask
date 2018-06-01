from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,BooleanField, RadioField, SelectField,HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegisForm(FlaskForm):
    username = StringField('Username',
                            validators = [DataRequired(), Length(min=2,max=20)],render_kw={"placeholder": "Username"})
    name = StringField('Name',
                            validators = [DataRequired(), Length(min=2,max=20)],render_kw={"placeholder": "Name"})
    password = PasswordField('Password',
                            validators = [DataRequired()],render_kw={"placeholder": "Password"})
    con_password = PasswordField('Confirm Pass',
                            validators = [DataRequired(), EqualTo('password')],render_kw={"placeholder": "Confirm Password"})
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    name = StringField('Name',
                            validators = [DataRequired(), Length(min=2,max=20)],render_kw={"placeholder": "Name"})
    password = PasswordField('Password',
                            validators = [DataRequired()], render_kw={"placeholder": "Password"})
    submit = SubmitField('Sign In')



class PasienForm(FlaskForm):
    nama = StringField('nama',
                            validators = [DataRequired(), Length(min=2,max=20)],render_kw={"placeholder": "nama"})
    umur = StringField('umur',
                            validators = [DataRequired(), Length(min=2,max=20)],render_kw={"placeholder": "umur"})
    jk   = RadioField('Jenis Kelamin',validators = [], choices = [('Laki-Laki', 'Laki-Laki'), ('Perempuan', 'Perempuan')])
    editJK   = RadioField('Jenis Kelamin',validators = [], choices = [('Laki-Laki', 'Laki-Laki'), ('Perempuan', 'Perempuan')])
    
    alamat = StringField('alamat',
                        validators = [DataRequired(), Length(min=2,max=20)],render_kw={"placeholder": "alamat"})
    submit = SubmitField('Save')

class RawatForm(FlaskForm):
    pasien = StringField('Kode Pasien',
                            validators = [DataRequired(), Length(min=2,max=20)],render_kw={"placeholder": "Kode Pasien"})
    kamar = StringField('Kode Kamar',
                            validators = [DataRequired(), Length(min=2,max=20)],render_kw={"placeholder": "Nama Kamar"})
    dokter = StringField('Kode Dokter',
                            validators = [DataRequired(), Length(min=2,max=20)],render_kw={"placeholder": "Nama Dokter"})
    dokter_hidden = HiddenField('Kode Dokter',
                            validators = [DataRequired(), Length(min=2,max=20)],render_kw={"placeholder": "Kode Dokter"})
    pasien_hidden = HiddenField('Kode Pasien',
                            validators = [DataRequired(), Length(min=2,max=20)],render_kw={"placeholder": "Kode Pasien"})
    kamar_hidden = HiddenField('Kode Kamar',
                            validators = [DataRequired(), Length(min=2,max=20)],render_kw={"placeholder": "Kode Kamar"})
    submit = SubmitField('Save')

