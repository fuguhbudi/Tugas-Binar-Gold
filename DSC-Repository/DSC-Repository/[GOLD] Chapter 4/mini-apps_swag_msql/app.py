import pandas as pd
from flask import Flask, request, jsonify

import getdata #source code
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from

app = Flask(__name__)

app.json_encoder = LazyJSONEncoder
swagger_template = dict(
info = {
    'title': LazyString(lambda: 'Mini Apps Swagger & MYSQL'),
    'version': LazyString(lambda: '1.0.0'),
    'description': LazyString(lambda: 'Latihan membuat mini apps get data dari database server'),
    },
    host = LazyString(lambda: request.host)
)
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'classicmodels',
            "route": '/classicmodels.json',
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/classicmodels/"
}
swagger = Swagger(app, template=swagger_template,             
                  config=swagger_config)

# Buat tampilan landing page
@app.route('/')
def landing_page():
    tampilan_awal = """
    Tampilan awal mini apps FLASK, SWAGGER, get data from MYSQL server
    <br>
    buka endpoint <a href="/classicmodels/">Swagger MYSQL</a>
    """
    return tampilan_awal


@swag_from("classicmodels/hello_mysql.yml", methods=['GET'])
@app.route("/data-customers", methods=["GET"]) #endpoint
def getData():
    objgetData = getdata.getDatas()
    data = objgetData.getAllData()
    if len(data):
        response = jsonify({
            "result" : data,
            "status" : 200,
        })
    else:
        response = jsonify({
            "result" : [],
            "status" : 400,
        })
    response_data = response
    return response_data
    

app.run("0.0.0.0", debug=True)

