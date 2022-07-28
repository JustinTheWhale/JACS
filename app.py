from flask import Flask, render_template, request, url_for, redirect
import sqlalchemy
from forms import Car_details, Confirm, Contact_info, Confirm, Contact_us, Quick_search
from car import Car_info, Car_media, Car_specs, Query_container
import random
import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret'
db = None


def timestamp():
    date = str(datetime.datetime.now())
    date = date[:-7]
    return date


def init_connection_engine():
    db_config = {
        "pool_size": 5,
        "max_overflow": 2,
        "pool_timeout": 30,  # 30 seconds
        # [END cloud_sql_postgres_sqlalchemy_timeout]
        "pool_recycle": 1800,  # 30 minutes
        # [END cloud_sql_postgres_sqlalchemy_lifetime]
    }

    return init_unix_connection_engine(db_config)



def init_unix_connection_engine(db_config):
    db_user = "postgres"
    db_pass = "xyz"
    db_name = "xyz"
    db_socket_dir = "/cloudsql"
    cloud_sql_connection_name = "xyz"

    pool = sqlalchemy.create_engine(

        # Equivalent URL:
        # postgres+pg8000://<db_user>:<db_pass>@/<db_name>
        #                         ?unix_sock=<socket_path>/<cloud_sql_instance_name>/.s.PGSQL.5432
        sqlalchemy.engine.url.URL(
            drivername="postgresql+pg8000",
            username=db_user,  # e.g. "my-database-user"
            password=db_pass,  # e.g. "my-database-password"
            database=db_name,  # e.g. "my-database-name"
            query={
                "unix_sock": "{}/{}/.s.PGSQL.5432".format(
                    db_socket_dir,  # e.g. "/cloudsql"
                    cloud_sql_connection_name)  # i.e "<PROJECT-NAME>:<INSTANCE-REGION>:<INSTANCE-NAME>"
            }
        ),
        **db_config
    )
    # [END cloud_sql_postgres_sqlalchemy_create_socket]
    pool.dialect.description_encoding = None
    return pool


def create_car_listings(params):
    global db
    db = init_connection_engine()
    try:
        with db.connect() as conn:
            container = create_search_query(params)
            if container.params == []:
                result = conn.execute(container.query)

            else:
                result = conn.execute(container.query, tuple(container.params))

            rows = []
            for i in result:
                rows.append(create_car_object(i))
            conn.close()
            return rows
    except Exception as e:
        print(e)
        return []

def create_search_query(params):
    query = """SELECT car_info.car_id, car_info.make, car_info.model, car_info.price, car_info.mileage, 
            car_info.year, car_info.owners, car_info.loc_state, car_info.loc_city, car_specs.description, 
            car_specs.body_type, car_specs.cylinders, car_specs.engine, car_specs.trans, car_specs.fuel,
            car_media.main_thumbnail, car_media.product_img_1, car_media.product_img_2, car_media.product_img_3,
            car_media.product_img_4, car_media.product_img_5, car_media.yt_link, car_media.product_link
            FROM car_info 
            FULL OUTER JOIN car_specs
            ON car_info.car_id = car_specs.car_id
            FULL OUTER JOIN car_media
            ON car_media.car_id = car_specs.car_id"""

    base = ' WHERE '
    triggered = []

    if params[0] != 'Any':
        triggered.append(0)
        base = base + 'make = %s AND '

    if params[1] != 'Any':
        triggered.append(1)
        params[1] = fix_string(params[1])
        base = base + 'price >= %s AND '

    if params[2] != 'Any':
        triggered.append(2)
        params[2] = fix_string(params[2])
        base = base + 'price <= %s AND '

    if params[3] != 'Any':
        triggered.append(3)
        base = base + 'car_specs.cylinders = %s' + ' AND '

    if params[4] != 'Any':
        triggered.append(4)
        if 'Below' in params[4]:
            miles = params[4].split(' ')[1]
            miles = fix_string(miles)
            params[4] = miles
            base = base + 'mileage <= %s'

        elif 'Above' in params[4]:
            miles = params[4].split(' ')[1]
            miles = fix_string(miles)
            params[4] = miles
            base = base + 'mileage >= %s'

        else:
            mileage = params[4].split('-')
            params[4] = fix_string(mileage[0])
            params.append(fix_string(mileage[1]))
            triggered.append(5)
            base = base + 'mileage >= %s AND mileage <= %s'

    container = Query_container()
    container.params = []
    for i in range(len(triggered)):
        container.params.append(params[triggered[i]])
    if base == ' WHERE ':
        container.query = query
        return container
    if base[-5:] == ' AND ':
        container.query = query + base[:-5]
        return container
    else:
        container.query = query + base
        return container
    

def fix_string(my_string):
    return int( my_string.replace('$', '').replace(',', '').replace('+', '') )

        
def create_car_object(row):
    car_object = Car_info()
    car_object.car_id = row[0]
    car_object.make = row[1]
    car_object.model = row[2]
    car_object.price = row[3]
    car_object.mileage = row[4]
    car_object.year = row[5]   
    car_object.owners = row[6]
    car_object.loc_state = row[7]
    car_object.loc_city = row[8]
    car_object.specs = Car_specs()
    car_object.specs.description = row[9]
    car_object.specs.body_type = row[10]
    car_object.specs.cylinders = row[11]
    car_object.specs.engine = row[12]
    car_object.specs.trans = row[13]
    car_object.specs.fuel = row[14]
    car_object.media = Car_media()
    car_object.media.main_thumbnail = row[15]
    car_object.media.product_img_1 = row[16]
    car_object.media.product_img_2 = row[17]
    car_object.media.product_img_3 = row[18]
    car_object.media.product_img_4 = row[19]
    car_object.media.product_img_5 = row[20]
    car_object.media.yt_link = row[21]
    car_object.media.product_link = row[22]
    return car_object



@app.route('/', methods=['GET', 'POST'])
def home():
    #Quick Search form


    form = Quick_search()
    if form.is_submitted():
        info = request.form
        search_params = list(dict(info).values())
        listings = create_car_listings(search_params)
        for i in range(len(listings)):
            listings[i].price = '{:,}'.format(listings[i].price)
            listings[i].mileage = '{:,}'.format(listings[i].mileage)
        return render_template('search-results.html', listings=listings, len=len(listings))


    #Dynamically loads all cars from DB     
    listings = create_car_listings(['Any'] * 5) #Creates listings by quering all
    for i in range(len(listings)):
            listings[i].price = '{:,}'.format(listings[i].price)
            listings[i].mileage = '{:,}'.format(listings[i].mileage)

            if listings[i].model == 'Enclave Essence':
                listings[i].model = 'EE'
            if 'GT' in listings[i].model:
                listings[i].model = listings[i].model[:-3]

    return render_template('index.html', form=form, listings=listings, len=len(listings))


@app.route('/all-listings.html')
def browse_by():
    #Dynamically loads all cars from DB     
    listings = create_car_listings(['Any'] * 5) #Creates listings by quering all
    for i in range(len(listings)):
        listings[i].price = '{:,}'.format(listings[i].price)
        listings[i].mileage = '{:,}'.format(listings[i].mileage)
    return render_template('all-listings.html', listings=listings, len=len(listings))


@app.route('/search-results.html', methods=['GET', 'POST'])
def search():
    return render_template('search-results.html')


@app.route('/contact.html', methods=['GET', 'POST'])
def contact():
    form = Contact_us()
    if form.is_submitted():
        global db
        db = init_connection_engine()
        try:
            with db.connect() as conn:
                date_and_time = timestamp()
                info = request.form
                email = info['email']
                name = info['name']
                message = info['message']
                conn.execute("INSERT INTO contact_inquiries (email, name, message, timestamp)" +
                             "VALUES (%s,%s,%s,%s)",
                             (email, name, message, date_and_time))
                conn.commit()
                conn.close()
                return redirect(url_for('contact'))
        except:
            return redirect(url_for('contact'))
    return render_template('contact.html', form=form)


@app.route('/one-products.html', methods=['GET', 'POST'])
def one_product():
    form = Contact_us()
    if form.is_submitted():
        global db
        db = init_connection_engine()
        try:
            with db.connect() as conn:
                date_and_time = timestamp()
                info = request.form
                email = info['email']
                name = info['name']
                message = info['message']
                conn.execute("INSERT INTO contact_inquiries (email, name, message, timestamp)" +
                             "VALUES (%s,%s,%s,%s)",
                             (email, name, message, date_and_time))
                conn.commit()
                conn.close()
                return redirect(url_for('one_product'))
        except:
            return redirect(url_for('one_product'))
    return render_template('one-products.html', form=form)


@app.route('/two-products.html', methods=['GET', 'POST'])
def two_product():
    form = Contact_us()
    if form.is_submitted():
        global db
        db = init_connection_engine()
        try:
            with db.connect() as conn:
                date_and_time = timestamp()
                info = request.form
                email = info['email']
                name = info['name']
                message = info['message']
                conn.execute("INSERT INTO contact_inquiries (email, name, message, timestamp)" +
                             "VALUES (%s,%s,%s,%s)",
                             (email, name, message, date_and_time))
                conn.commit()
                conn.close()
                return redirect(url_for('two_product'))
        except:
            return redirect(url_for('two_product'))
    return render_template('two-products.html', form=form)


@app.route('/three-products.html', methods=['GET', 'POST'])
def three_product():
    form = Contact_us()
    if form.is_submitted():
        global db
        db = init_connection_engine()
        try:
            with db.connect() as conn:
                date_and_time = timestamp()
                info = request.form
                email = info['email']
                name = info['name']
                message = info['message']
                conn.execute("INSERT INTO contact_inquiries (email, name, message, timestamp)" +
                             "VALUES (%s,%s,%s,%s)",
                             (email, name, message, date_and_time))
                conn.commit()
                conn.close()
                return redirect(url_for('three_product'))
        except:
            return redirect(url_for('three_product'))
    return render_template('three-products.html', form=form)


@app.route('/four-products.html', methods=['GET', 'POST'])
def four_product():
    form = Contact_us()
    if form.is_submitted():
        global db
        db = init_connection_engine()
        try:
            with db.connect() as conn:
                date_and_time = timestamp()
                info = request.form
                email = info['email']
                name = info['name']
                message = info['message']
                conn.execute("INSERT INTO contact_inquiries (email, name, message, timestamp)" +
                             "VALUES (%s,%s,%s,%s)",
                             (email, name, message, date_and_time))
                conn.commit()
                conn.close()
                return redirect(url_for('four_product'))
        except:
            return redirect(url_for('four_product'))
    return render_template('four-products.html', form=form)


@app.route('/five-products.html', methods=['GET', 'POST'])
def five_product():
    form = Contact_us()
    if form.is_submitted():
        global db
        db = init_connection_engine()
        try:
            with db.connect() as conn:
                date_and_time = timestamp()
                info = request.form
                email = info['email']
                name = info['name']
                message = info['message']
                conn.execute("INSERT INTO contact_inquiries (email, name, message, timestamp)" +
                             "VALUES (%s,%s,%s,%s)",
                             (email, name, message, date_and_time))
                conn.commit()
                conn.close()
                return redirect(url_for('five_product'))
        except:
            return redirect(url_for('five_product'))
    return render_template('five-products.html', form=form)


@app.route('/six-products.html', methods=['GET', 'POST'])
def six_product():
    form = Contact_us()
    if form.is_submitted():
        global db
        db = init_connection_engine()
        try:
            with db.connect() as conn:
                date_and_time = timestamp()
                info = request.form
                email = info['email']
                name = info['name']
                message = info['message']
                conn.execute("INSERT INTO contact_inquiries (email, name, message, timestamp)" +
                             "VALUES (%s,%s,%s,%s)",
                             (email, name, message, date_and_time))
                conn.commit()
                conn.close()
                return redirect(url_for('six_product'))
        except:
            return redirect(url_for('six_product'))
    return render_template('six-products.html', form=form)

@app.route('/seven-products.html', methods=['GET', 'POST'])
def seven_product():
    form = Contact_us()
    if form.is_submitted():
        global db
        db = init_connection_engine()
        try:
            with db.connect() as conn:
                date_and_time = timestamp()
                info = request.form
                email = info['email']
                name = info['name']
                message = info['message']
                conn.execute("INSERT INTO contact_inquiries (email, name, message, timestamp)" +
                             "VALUES (%s,%s,%s,%s)",
                             (email, name, message, date_and_time))
                conn.commit()
                conn.close()
                return redirect(url_for('seven_product'))
        except:
            return redirect(url_for('seven_product'))
    return render_template('seven-products.html', form=form)

@app.route('/eight-products.html', methods=['GET', 'POST'])
def eight_product():
    form = Contact_us()
    if form.is_submitted():
        global db
        db = init_connection_engine()
        try:
            with db.connect() as conn:
                date_and_time = timestamp()
                info = request.form
                email = info['email']
                name = info['name']
                message = info['message']
                conn.execute("INSERT INTO contact_inquiries (email, name, message, timestamp)" +
                             "VALUES (%s,%s,%s,%s)",
                             (email, name, message, date_and_time))
                conn.commit()
                conn.close()
                return redirect(url_for('eight_product'))
        except:
            return redirect(url_for('eight_product'))
    return render_template('eight-products.html', form=form)

@app.route('/nine-products.html', methods=['GET', 'POST'])
def nine_product():
    form = Contact_us()
    if form.is_submitted():
        global db
        db = init_connection_engine()
        try:
            with db.connect() as conn:
                date_and_time = timestamp()
                info = request.form
                email = info['email']
                name = info['name']
                message = info['message']
                conn.execute("INSERT INTO contact_inquiries (email, name, message, timestamp)" +
                             "VALUES (%s,%s,%s,%s)",
                             (email, name, message, date_and_time))
                conn.commit()
                conn.close()
                return redirect(url_for('nine_product'))
        except:
            return redirect(url_for('nine_product'))
    return render_template('nine-products.html', form=form)

@app.route('/ten-products.html', methods=['GET', 'POST'])
def ten_product():
    form = Contact_us()
    if form.is_submitted():
        global db
        db = init_connection_engine()
        try:
            with db.connect() as conn:
                date_and_time = timestamp()
                info = request.form
                email = info['email']
                name = info['name']
                message = info['message']
                conn.execute("INSERT INTO contact_inquiries (email, name, message, timestamp)" +
                             "VALUES (%s,%s,%s,%s)",
                             (email, name, message, date_and_time))
                conn.commit()
                conn.close()
                return redirect(url_for('ten_product'))
        except:
            return redirect(url_for('ten_product'))
    return render_template('ten-products.html', form=form)


@app.route('/test-drive.html', methods=['GET', 'POST'])
def test_drive():
    form = Car_details()
    if form.is_submitted():
        info = request.form
        return redirect(url_for('test_drive_2', make=info['make'], model=info['model'], year=info['year'], state=info['state'], city=info['city']))
    return render_template('test-drive.html', form=form)


@app.route('/test-drive-2.html', methods=['GET', 'POST'])
def test_drive_2():
    request_args = ['make', 'model', 'year', 'state', 'city']
    request_values = []
    for i in request_args:
        request_values.append(request.args.get(i))

    form = Contact_info()
    if form.is_submitted():
        info = request.form
        return redirect(url_for('test_drive_3', make=request_values[0], model=request_values[1], year=request_values[2], state=request_values[3], city=request_values[4], fname=info['fname'], lname=info['lname'], date=info['date'], time=info['time'], phone=info['phone'], email=info['email']))
    return render_template('test-drive-2.html', form=form)


@app.route('/test-drive-3.html', methods=['GET', 'POST'])
def test_drive_3():
    request_args = ['make', 'model', 'year', 'state', 'city', 'fname', 'lname', 'date', 'time', 'phone', 'email']
    request_values = []
    for i in request_args:
        request_values.append(request.args.get(i))
    confirm = Confirm()
    if confirm.is_submitted():
        global db
        db = init_connection_engine()
        try:
            with db.connect() as conn:
                app_num = random.randint(5000,10000)
                conn.execute("INSERT INTO test_drives(make, model, year, state, city, fname, lname, date, time, phone, email, car_id, app_num)" +
                                      "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s)", 
                                      (request_values[0], request_values[1], request_values[2], request_values[3], request_values[4], request_values[5], request_values[6], request_values[7], request_values[8], request_values[9], request_values[10], 1, app_num))
                conn.commit()
                conn.close()
        except:
            return render_template('test-drive-4.html')
        return render_template('test-drive-4.html')
    return render_template('test-drive-3.html', make=request_values[0], model=request_values[1], year=request_values[2], state=request_values[3], city=request_values[4], fname=request_values[5], lname=request_values[6], date=request_values[7], time=request_values[8], phone=request_values[9], email=request_values[10], confirm=confirm)


@app.route('/test-drive-4.html')
def test_drive_4():
    return render_template('test-drive-4.html')


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')


if __name__ == '__main__':
    app.run(use_reloader=True, debug=True)
