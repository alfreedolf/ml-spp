from flask import Flask, request, render_template
from source_deepar.display_quantiles import display_quantiles_flask
import json

app = Flask(__name__)

@app.route("/")
def home():
    return render_template(
        "index.html"
    )


@app.route('/postmethod', methods = ['POST'])
def get_post_javascript_data():
    jsdata = request.form['javascript_data']
    js_obj_data = json.loads(jsdata)['predictions'][0]['quantiles']
    quantiles_plot = display_quantiles_flask(js_obj_data)
    return quantiles_plot

@app.route('/getmethod/<jsdata>')
def get_javascript_data(jsdata):
    return json.loads(jsdata)[0]