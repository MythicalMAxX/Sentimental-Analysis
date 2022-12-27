from flask import render_template, Flask, request, redirect, url_for
from nltk.sentiment import SentimentIntensityAnalyzer
from urllib import request as urllibrequest
import re

def datascrapper(url):
    with urllibrequest.urlopen(url) as response:
        response_data  =response.read()
    para = re.findall(r"<p>(.*?)</p>",str(response_data))
    Complete_content = ""
    for content in para:
        content = re.compile(r'<[^>]+>').sub('', content)
        content = re.sub(r'(\\x(.){2})', '',content)
        content = re.sub(r'&[^>]+;','',content)
        content = re.sub(r'\[]+n','',content)
        Complete_content = Complete_content+content
    return Complete_content

def string_to_list(string):
    string_list = string.split(".")
    print(string_list)
    return string_list


def Process(list):
    Total_score = 0
    Positive_texts = []
    Negetive_texts = []
    sia = SentimentIntensityAnalyzer()
    for strings in list:
        data = sia.polarity_scores(strings)
        score = data["compound"]
        Total_score = Total_score+score
        if score>0:
            Positive_texts.append(strings)
        if score<0:
            Negetive_texts.append(strings)
    return Positive_texts,Negetive_texts,Total_score

app = Flask(__name__)
@app.route('/')
def myapp():
    return render_template("landingpage.html")

@app.route('/indexu',methods=["POST","GET"])
def indexu():
    if request.method == "POST":
        global url
        url = request.form["url"]
        return redirect(url_for("analysisreport", link = url))
    else:
        return render_template("indexu.html")

@app.route('/indext',methods=["POST","GET"])
def indext():
    if request.method == "POST":
        global text
        text = request.form["text"]
        return redirect(url_for("textanalysis", link = text))
    else:
        return render_template("indext.html")



@app.route('/Analysis')
def analysisreport():
    data = datascrapper(url)
    list_of_string = string_to_list(data)
    list_of_positivetext,list_of_negetivetext,Total_score = Process(list_of_string)
    return render_template("index.html", val = Total_score, P_text = list_of_positivetext, N_text = list_of_negetivetext)

@app.route('/TAnalysis')
def textanalysis():
    list_of_string = string_to_list(text)
    list_of_positivetext,list_of_negetivetext,Total_score = Process(list_of_string)
    return render_template("index.html", val = Total_score, P_text = list_of_positivetext, N_text = list_of_negetivetext)

app.run(debug=True)

"""
https://www.inverse.com/article/54378-super-taster-test-why-some-people-hate-vegetables
https://www.askdrsears.com/topics/feeding-eating/family-nutrition/vegetables/7-reasons-why-veggies-are-so-good-for-you/
"""