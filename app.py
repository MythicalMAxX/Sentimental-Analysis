from flask import render_template, Flask, request, redirect, url_for
from nltk.sentiment import SentimentIntensityAnalyzer
from urllib import request as urllibrequest
import re
import ssl

context = ssl._create_unverified_context()

def perc(neu,pos,neg):
    neu_perc = (neu*100)/(neu+pos+neg)
    pos_perc = (pos * 100) / (neu + pos + neg)
    neg_perc = (neg*100)/(neu+pos+neg)
    return neu_perc,pos_perc,neg_perc


def datascrapper(url):
    with urllibrequest.urlopen(url,context=context) as response:
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
    Negative_texts = []
    positive_score = 0
    negative_score = 0
    neutral_score = 0
    sia = SentimentIntensityAnalyzer()
    for strings in list:
        data = sia.polarity_scores(strings)
        neutral_score = neutral_score+data["neu"]
        positive_score = positive_score + data["pos"]
        negative_score = negative_score + data["neg"]
        score = data["compound"]
        Total_score = Total_score+score
        if score>0:
            Positive_texts.append(strings)
        if score<0:
            Negative_texts.append(strings)

    return Positive_texts,Negative_texts,Total_score,positive_score,negative_score,neutral_score

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
    list_of_positivetext,list_of_Negativetext,Total_score, p_score, n_score,neu_score = Process(list_of_string)
    neu_perc, pos_perc, neg_perc = perc(neu_score, p_score, n_score)
    pos_perc = round(pos_perc, 1)
    neg_perc = round(neg_perc, 1)
    neu_perc = round(neu_perc, 1)
    return render_template("index.html", val = Total_score, P_text = list_of_positivetext, N_text = list_of_Negativetext,P_score = p_score,N_score = n_score,Neu_score=neu_score,Neu_perc=neu_perc,Pos_perc=pos_perc,Neg_perc=neg_perc)

@app.route('/TAnalysis')
def textanalysis():
    list_of_string = string_to_list(text)
    list_of_positivetext,list_of_Negativetext,Total_score, p_score, n_score,neu_score = Process(list_of_string)
    neu_perc, pos_perc, neg_perc = perc(neu_score, p_score, n_score)
    pos_perc = round(pos_perc, 1)
    neg_perc = round(neg_perc, 1)
    neu_perc = round(neu_perc, 1)
    return render_template("index.html", val = Total_score, P_text = list_of_positivetext, N_text = list_of_Negativetext,P_score = p_score, N_score = n_score,Neu_score=neu_score,Neu_perc=neu_perc,Pos_perc=pos_perc,Neg_perc=neg_perc)

app.run(debug=True)
