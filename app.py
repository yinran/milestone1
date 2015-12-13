from flask import Flask, render_template, request, redirect
import requests
import simplejson as json
import pandas as pd

from bokeh.plotting import *
from bokeh.resources import INLINE
from bokeh.embed import components
from bokeh.util.string import encode_utf8

app = Flask(__name__)

@app.route('/')
def main():
    return redirect('/index')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    ticker = request.form['ticker']
    url = "https://www.quandl.com/api/v3/datasets/WIKI/" + ticker + "/data.json"
    payload = {'api_key':'9o4vcpiASzqaA6dczzzZ','start_date': '2015-11-01', 'end_date': '2015-11-30'}
    res = requests.get(url, params=payload)
    raw_data = json.loads(res.text)
    date_strings = [x[0] for x in raw_data["dataset_data"]["data"]]
    close_price = [x[4] for x in raw_data["dataset_data"]["data"]]
    date = pd.to_datetime(pd.Series(date_strings))
    p = figure(title="Sotck Price for "+ticker+" (source: Quandl WIKI)", x_axis_label="Date",y_axis_label="Price", x_axis_type="datetime")
    p.line(date ,close_price, legend="Close Price", line_width=3)
    script, div = components(p, INLINE)
    html = render_template('results.html', plot_script=script, plot_div=div)
    return encode_utf8(html)

if __name__ == '__main__':
    app.run(port=33507)
