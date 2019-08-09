#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  9 10:23:28 2019

@author: lavanyasingh
"""

from flask import Flask, render_template, request
import random
import requests
from chart_maker import create_bar_chart, make_data, create_hover_tool
from bokeh.layouts import row
from bokeh.embed import components
from colls import colls
from bokeh.models.widgets import Button
from functools import partial

app = Flask(__name__)
DATE = '2019-08-08'

session=requests.Session()

@app.route("/")
def index():
    return render_template("index.html", collections=colls)
    

@app.route("/<int:bars_count>/")
def chart(bars_count):
    if bars_count <= 0:
        bars_count = 1
    
    data = {"days": [], "bugs": [], "costs": []}
    for i in range(1, bars_count + 1):
        data['days'].append(i)
        data['bugs'].append(random.randint(1,100))
        data['costs'].append(random.uniform(1.00, 1000.00))
        
    plot = create_bar_chart(data, "Bugs found per day", "days",
                            "bugs")
    script, div = plot

    return render_template("chart.html", bars_count=bars_count,
                           the_div=div, the_script=script)

@app.route('/change_date', methods=["POST"])
def date_handler():
    date_pieces = request.form['date'].split('-')
    if request.form['change'] == "next":
        date_pieces[2] = str(int(date_pieces[2]) + 1)
    if request.form['change'] == "previous":
        date_pieces[2] = str(int(date_pieces[2]) - 1)
    date_pieces = ["0" + piece if len(piece) == 1 else piece for piece in date_pieces]
    new_d = date_pieces[0] + "-" + date_pieces[1] + "-" + date_pieces[2]
    return make_collection_viz(request.form['collection'], new_d)
    
@app.route('/<collection>/<date>')
def make_collection_viz(collection, date):
    session = requests.Session()
    response = session.get('http://localhost:8300/dump/{date}'.format(date=date))
    json = response.json()
        
    try:
        newscrawl = json['collection'][collection]

        domains = make_data(newscrawl['domains'], "domain", "size")
        mimetypes = make_data(newscrawl['mimetypes'], "mimetype", "size")
        statuscodes = make_data(newscrawl['statuscodes'], "statuscode", "size")
        hovers = [create_hover_tool('size') for i in range(3)]
        
        plot1 = create_bar_chart(domains, date+" Domains for Collection {coll}".format(coll=collection), 
                                "domain", "size", "Domain", "Captures", hover_tool=hovers[0])
        plot2 = create_bar_chart(mimetypes, date+" Mimetypes for Collection {coll}".format(coll=collection), 
                                "mimetype", "size", "Mimetype", "Captures", hover_tool=hovers[1], width=700)
        plot3 = create_bar_chart(statuscodes, date+" Statuscodes for Collection {coll}".format(coll=collection), 
                                "statuscode", "size", "Statuscodes", "Captures", hover_tool=hovers[2], width=700)
        plots = [components(plot1), components(row(plot2, plot3))]
        
        divs = [{"div":div, "script":script} for script,div in plots]
        
        return render_template("viz.html", collection=collection, divs=divs, date=date)
    except:
        error = "ERROR IN GETTING {coll}".format(coll=collection)
        return render_template("error.html", error=error)

@app.route('/viz', methods=['POST'])
def forward():
    resp = request.form
    return make_collection_viz(resp['collection'], resp['date'])

if __name__ == "__main__":
    app.run(debug=True)