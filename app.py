from flask import Flask, request, render_template
from flask_table import Table, Col
import string
import json

app = Flask(__name__)

# Load in data

with open('mvp_data/mvp_comps.json') as j:
    tickers = json.load(j)

class ItemTable(Table):
    Ticker = Col('Ticker')


@app.route('/')
def home():
    """
    Description: Render default page without text
    Output: Rendered page
    """

    return render_template('index.html')


@app.route('/response', methods = ['POST'])
def response():
    """
    Description: Render page with comps
    Output: Rendered page
    """

    raw_ticker =  [str(x) for x in request.form.values()][0]

    cleaned_ticker = raw_ticker.translate(str.maketrans('', '', string.punctuation)).upper()
    
    inputstring = "Companies similar to ${}:".format(cleaned_ticker)

    if cleaned_ticker in tickers:
        items = [{'Ticker': t}  for t in tickers[cleaned_ticker]]
    else:
        return render_template('index.html', Table='ERROR: Please enter a valid ticker')

    table = ItemTable(items)

    return render_template('index.html', Input=inputstring, Table=table)


if __name__ == "__main__":
    app.run(debug = True, host='0.0.0.0')