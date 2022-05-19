from flask import Flask, request, jsonify, Response
from models import db
import os
import sys
from flask_cors import CORS
import traceback
import routes

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, expose_headers =['Content-Disposition'])

os.environ['ENV_FILE'] = 'environment.env'
app.config.from_envvar('ENV_FILE')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(app.config.get("MYSQL_USER"), app.config.get("MYSQL_PASSWORD"), 
app.config.get("MYSQL_ADDRESS"), app.config.get("MYSQL_PORT"),app.config.get("MYSQL_NAME"))
db.init_app(app)

app.register_blueprint(routes.app, url_prefix="")

@app.route('/test', methods=['GET'])
def test():
    try:
        return 'This is the VideoCo Backend'
    except:
        print(str(traceback.format_exc()), file=sys.stderr)
        return "Failed", 500 

if __name__ == "__main__":
    app.run(debug=True)