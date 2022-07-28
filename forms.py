from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, StringField, DateTimeField, TextAreaField
from wtforms.validators import InputRequired


class Car_details(FlaskForm):
    make = SelectField(
        "Select Make",
        choices=[
            ("Acura", "Acura"),
            ("Audi", "Audi"),
            ("BMW", "BMW"),
            ("Buick", "Buick"),
            ("Cadillac", "Cadillac"),
            ("Chevrolet", "Chevrolet"),
            ("Chrysler", "Chrysler"),
            ("Dodge", "Dodge"),
            ("Ford", "Ford"),
        ],
    )
    model = SelectField(
        "Select Model",
        choices=[
            ("RDX", "RDX"),
            ("A3", "A3"),
            ("230I", "230I"),
            ("Enclave Essence", "Enclave Essence"),
            ("ATS", "ATS"),
            ("Bolt", "Bolt"),
            ("300", "300"),
            ("300C", "300C"),
            ("Challenger GT", "Challenger GT"),
            ("Escape", "Escape"),
        ],
    )
    year = SelectField(
        "Select Year",
        choices=[
            ("2006", "2006"),
            ("2014", "2014"),
            ("2016", "2016"),
            ("2017", "2017"),
            ("2018", "2018"),
            ("2019", "2019"),
            ("2020", "2020"),
        ],
    )
    state = SelectField(
        "Select State",
        choices=[
            ("California", "California"),
            ("Florida", "Florida"),
            ("New York", "New York"),
        ],
    )
    city = SelectField(
        "Select City",
        choices=[
            ("San Fransisco", "San Fransisco"),
            ("Miami", "Miami"),
            ("Manhattan", "Manhattan"),
        ],
    )
    submit = SubmitField("Submit")


class Contact_info(FlaskForm):
    fname = StringField("First Name", validators=[InputRequired()])
    lname = StringField("last Name", validators=[InputRequired()])
    date = DateTimeField("Date", format="%m-%d-%Y", validators=[InputRequired()])
    time = DateTimeField("Time", format="%H:%M", validators=[InputRequired()])
    phone = StringField("Phone", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired()])
    submit = SubmitField("Submit")


class Confirm(FlaskForm):
    submit = SubmitField("Submit")


class Contact_us(FlaskForm):
    name = StringField(
        "Name", render_kw={"rows": 1, "cols": 10}, validators=[InputRequired()]
    )
    email = StringField("Email", validators=[InputRequired()])
    message = TextAreaField(
        "Message", render_kw={"rows": 10, "cols": 70}, validators=[InputRequired()]
    )
    submit = submit = SubmitField("Submit")


class Quick_search(FlaskForm):
    make = SelectField(
        "Select Make",
        choices=[
            ("Any", "Any"),
            ("Acura", "Acura"),
            ("Audi", "Audi"),
            ("BMW", "BMW"),
            ("Buick", "Buick"),
            ("Cadillac", "Cadillac"),
            ("Chevrolet", "Chevrolet"),
            ("Chrysler", "Chrysler"),
            ("Dodge", "Dodge"),
            ("Ford", "Ford"),
        ],
    )
    min_price = SelectField(
        "Select Min Price",
        choices=[
            ("Any", "Any"),
            ("$8,566", "$8,566"),
            ("$10,000", "$10,000"),
            ("$15,000", "$15,000"),
            ("$20,000", "$20,000"),
            ("$25,000", "$25,000"),
            ("$30,000+", "$30,000+"),
        ],
    )
    max_price = SelectField(
        "Select Max Price",
        choices=[
            ("Any", "Any"),
            ("$8,566", "$8,566"),
            ("$10,000", "$10,000"),
            ("$15,000", "$15,000"),
            ("$20,000", "$20,000"),
            ("$25,000", "$25,000"),
            ("$30,000+", "$30,000+"),
        ],
    )
    cylinders = SelectField(
        "Select Cylinders",
        choices=[
            ("Any", "Any"),
            ("4 Cylinders", "4 Cylinders"),
            ("6 Cylinders", "6 Cylinders"),
            ("8 Cylinders", "8 Cylinders"),
        ],
    )
    mileage = SelectField(
        "Select Mileage",
        choices=[
            ("Any", "Any"),
            ("Below 20,000", "Below 20,000"),
            ("20,001-30,000", "20,001-30,000"),
            ("30,001-40,000", "30,001-40,000"),
            ("40,001-50,000", "40,001-50,000"),
            ("50,001-60,000", "50,001-60,000"),
            ("Above 60,000", "Above 60,000"),
        ],
    )
    submit = submit = SubmitField("Submit")
