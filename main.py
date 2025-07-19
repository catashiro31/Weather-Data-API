import pandas as pd
from flask import Flask, render_template

app = Flask(__name__)
@app.route('/')
def home():
    df = pd.read_csv('data/stations.txt', skiprows=17)
    df = df[['STAID','STANAME                                 ']]
    return render_template('home.html', data=df.to_html())

@app.route('/api/v1/<station>/<date>')
def query_station_date(station, date):
    try:
        filepath = 'data/TG_STAID' + str(station).zfill(6) + '.txt'
        df = pd.read_csv(filepath, skiprows=20, parse_dates=['    DATE'])
        temperature = df[df['    DATE'] == date]['   TG'].squeeze() / 10
        result_dict = {'date' : date,
                       'station' : station,
                       'temperature' : temperature}
        return result_dict
    except FileNotFoundError:
        return render_template("404_not_found.html")

@app.route('/api/v1/<station>')
def query_station(station):
    try:
        filepath = 'data/TG_STAID' + str(station).zfill(6) + '.txt'
        df = pd.read_csv(filepath, skiprows=20, parse_dates=['    DATE'])
        return render_template('station_data.html',
                               data=df.to_html())
    except FileNotFoundError:
        return render_template("404_not_found.html")

@app.route('/api/v1/yearly/<station>/<year>')
def query_station_year(station, year):
    try:
        filepath = 'data/TG_STAID' + str(station).zfill(6) + '.txt'
        df = pd.read_csv(filepath, skiprows=20, parse_dates=['    DATE'])
        df = df[df['    DATE'].apply(lambda x : x.year) == int(year)]
        result = df.to_dict(orient="records")
        return result
    except FileNotFoundError:
        return render_template("404_not_found.html")

if __name__ == '__main__':
    app.run(debug=True)