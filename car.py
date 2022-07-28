#Holds basic info on cars 
class Car_info:
    car_id = None
    make = None
    model = None
    price = None
    mileage = None
    year = None    
    owners = None
    loc_state = None
    loc_city = None
    specs = None
    media = None

#Holds additional Specs on the cars
class Car_specs:
    description = None
    body_type = None
    cylinders = None
    engine = None
    trans = None
    fuel = None

#Holds car media links and other info
class Car_media:
    main_thumbnail = None
    product_img_1 = None
    product_img_2 = None
    product_img_3 = None
    product_img_4 = None
    product_img_5 = None
    yt_link = None
    product_link = None


#Holds DB query and search parameters
class Query_container:
    query = None
    params = None







"""
Order of Events:

1.) Page routing
2.) QuickSearch sends a POST request containing search parameters
3.) The function takes the data and builds a query based on the selected input
4.) The function returns a list of Car objects containing car info
5.) The function redirects us to a new html template and dynamically creates the listings w/ Jinja2

"""
