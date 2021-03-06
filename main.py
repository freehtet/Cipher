from flask import Flask, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv
from random import choice, randint, shuffle
import pyperclip
import sys


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class CafeForm(FlaskForm):
    type = SelectField("Please select", choices=["EncodeοΈ", "Decode"], validators=[DataRequired()])
    rating = SelectField("Rating", choices=["ποΈ", "π₯", "π¦", "π", "π¦"], validators=[DataRequired()])
    cafe = StringField('Enter Text', validators=[DataRequired()])
    submit = SubmitField('Go!')

class PasswordForm(FlaskForm):
    # type = SelectField("Please select", choices=["EncodeοΈ", "Decode"], validators=[DataRequired()])
    # rating = SelectField("Rating", choices=["ποΈ", "π₯", "π¦", "π", "π¦"], validators=[DataRequired()])
    # cafe = StringField('Enter Text', validators=[DataRequired()])
    submit = SubmitField('Get Me New Password!')

# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis βοΈ/πͺ/β/π
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


def caesar(start_text, shift_amount, cipher_direction):
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', ' ',
                '*', ':', '.', '%', '$', 'Β·', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', ' ',
                '*', ':', '.', '%', '$', 'Β·']
    end_text = ""
    if cipher_direction == "decode":
        shift_amount *= -1
    for char in start_text:
        # TODO-3: What happens if the user enters a number/symbol/space?
        # Can you fix the code to keep the number/symbol/space when the text is encoded/decoded?
        # e.g. start_text = "meet me at 3"
        # end_text = "β’β’β’β’ β’β’ β’β’ 3"
        if char != "_":
            position = alphabet.index(char)
            new_position = position + shift_amount
            end_text += alphabet[new_position]
        elif char == "_":
            end_text += " "

    return end_text


def password_generator():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)
    shuffle(password_list)
    shuffle(password_list)
    password = "".join(password_list)

    return password


# all Flask routes below
@app.route("/")
def home():
    logo = """
    ,adPPYba, ,adPPYYba,  ,adPPYba, ,adPPYba, ,adPPYYba, 8b,dPPYba,
a8"     "" ""     `Y8 a8P_____88 I8[    "" ""     `Y8 88P'   "Y8
8b         ,adPPPPP88 8PP"""""""  `"Y8ba,  ,adPPPPP88 88
"8a,   ,aa 88,    ,88 "8b,   ,aa aa    ]8I 88,    ,88 88
 `"Ybbd8"' `"8bbdP"Y8  `"Ybbd8"' `"YbbdP"' `"8bbdP"Y8 88
            88             88
           ""             88
                          88
 ,adPPYba, 88 8b,dPPYba,  88,dPPYba,   ,adPPYba, 8b,dPPYba,
a8"     "" 88 88P'    "8a 88P'    "8a a8P_____88 88P'   "Y8
8b         88 88       d8 88       88 8PP""""""" 88
"8a,   ,aa 88 88b,   ,a8" 88       88 "8b,   ,aa 88
 `"Ybbd8"' 88 88`YbbdP"'  88       88  `"Ybbd8"' 88
              88
              88
    """
    return render_template("index.html", logo=logo)


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    message = ""
    if form.validate_on_submit():
        text = (form.cafe.data).lower()
        if text != "":
            type = (form.type.data).lower()
            rate = 1
            rate_raw = form.rating.data

            if rate_raw == "π¦":
                rate = 5
            elif rate_raw == "π":
                rate = 4
            elif rate_raw == "π¦":
                rate = 3
            elif rate_raw == "π₯":
                rate = 2
            else:
                rate = 1

            message = caesar(start_text=text, shift_amount=rate, cipher_direction=type)

            flash(f"{message}")
            # pyperclip.copy(message)
            # pyperclip.paste()

        return redirect(url_for('add_cafe'))
    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()
    return render_template('add.html', form=form)

@app.route('/password', methods=["GET", "POST"])
def generate_password():
    form = PasswordForm()
    if form.validate_on_submit():
        password = password_generator()

        flash(f"{password}")
        # pyperclip.copy(password)
        # pyperclip.paste()

        return redirect(url_for('generate_password'))
    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()
    return render_template('password.html', form=form)



@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
