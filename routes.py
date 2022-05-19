from flask import Blueprint, Flask, jsonify, request, json, Response, session
from sqlalchemy import select
import models
from flask_sqlalchemy import SQLAlchemy
# from aws_util import login_required


app = Blueprint('/customer', __name__)

@app.route('/customer/orders-api', methods=['GET', 'POST', 'PUT'])
def orders():
    if (request.method == 'GET'):
        try:
            orders_data = models.db.session.execute(select(models.Customer))
            return orders_data
        except:
            return "Nothing was found"

