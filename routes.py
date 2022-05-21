from flask import Blueprint, Flask, jsonify, request, json, Response, session
from sqlalchemy import select
from models import Orders, Persons, Customer, Movies, MovieDetails, Employees, GeneralCategory, db
from flask_sqlalchemy import SQLAlchemy
import traceback
import sys
# from aws_util import login_required


app = Blueprint('/customer', __name__)

@app.route('/customer/orders-api', methods=['GET', 'POST', 'PUT','DELETE'])
def orders():
    if (request.method == 'GET'):
        try:
            orders = []
            orders_data = db.session.query(Orders).all()
            for order in orders_data:
                orders.append(order.to_dict())
            return jsonify(orders)
        except Exception as e:
            print(str(traceback.format_exc()), file=sys.stderr)

    elif(request.method == 'POST'):
        return "post order"

    elif(request.method == 'PUT'):
        return "put order"

    elif(request.method == 'DELETE'):
        return "delete order"
            
@app.route('/customer/customer-api', methods=['GET', 'POST','PUT','DELETE'])
def customer():
    if (request.method == 'GET'):
        try:
            customer_data = db.session.query(Customer).all()
            customers = []
            for customer in customer_data:
                customers.append(customer.to_dict())
            return jsonify(customers)
        except Exception as e:
            print(str(traceback.format_exc()), file=sys.stderr)


    elif(request.method == 'POST'):
        return "post customer"

    elif(request.method == 'PUT'):
        return "put customer"
        
    elif(request.method == 'DELETE'):
        return "delete customer"

@app.route('/customer/movies-api', methods=['GET', 'POST','PUT','DELETE'])
def movies():
    if (request.method == 'GET'):
        try:
            movies = []
            movies_data = db.session.query(Movies).all()
            for movie in movies_data:
                movies.append(movie.to_dict())
            return jsonify(movies)
        except Exception as e:
            print(str(traceback.format_exc()), file=sys.stderr)

    elif(request.method == 'POST'):
        return "post movies"

    elif(request.method == 'PUT'):
        return "put movies"
        
    elif(request.method == 'DELETE'):
        return "delete movies"

@app.route('/customer/persons-api', methods=['GET', 'POST','PUT','DELETE'])
def persons():
    if (request.method == 'GET'):
        try:
            persons = []
            persons_data = db.session.query(Persons).all()
            for person in persons_data:
                persons.append(person.to_dict())
            return jsonify(persons)
        except Exception as e:
            print(str(traceback.format_exc()), file=sys.stderr)

    elif(request.method == 'POST'):
        return "post persons"

    elif(request.method == 'PUT'):
        return "put persons"
        
    elif(request.method == 'DELETE'):
        return "delete persons"

@app.route('/customer/employee-api', methods=['GET', 'POST','PUT','DELETE'])
def employee():
    if (request.method == 'GET'):
        try:
            employees = []
            employees_data = db.session.query(Employees).all()
            for employee in employees_data:
                employees.append(employee.to_dict())
            return jsonify(employees)
        except Exception as e:
            print(str(traceback.format_exc()), file=sys.stderr)

    elif(request.method == 'POST'):
        return "post employee"

    elif(request.method == 'PUT'):
        return "put employee"
        
    elif(request.method == 'DELETE'):
        return "delete employee"

@app.route('/customer/general-api', methods=['GET', 'POST','PUT','DELETE'])
def general():
    if (request.method == 'GET'):
        try:
            general_category = []
            general_data = db.session.query(GeneralCategory).all()
            for general in general_data:
                general_category.append(general.to_dict())
            return jsonify(general_category)
        except Exception as e:
            print(str(traceback.format_exc()), file=sys.stderr)

    elif(request.method == 'POST'):
        return "post general"

    elif(request.method == 'PUT'):
        return "put general"
        
    elif(request.method == 'DELETE'):
        return "delete general"

@app.route('/customer/movie-details-api', methods=['GET', 'POST','PUT','DELETE'])
def movie_details():
    if (request.method == 'GET'):
        try:
            movie_details = []
            movies_data = db.session.query(MovieDetails).all()
            for movie in movies_data:
                movie_details.append(movie.to_dict())
            return jsonify(movie_details)
        except Exception as e:
            print(str(traceback.format_exc()), file=sys.stderr)

    elif(request.method == 'POST'):
        return "post movie details"

    elif(request.method == 'PUT'):
        return "put movie details"
        
    elif(request.method == 'DELETE'):
        return "delete movie details"
