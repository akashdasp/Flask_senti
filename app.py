from flask import Flask,json,request,render_template,url_for
import string
import nltk
import pickle
import datetime
import random
from flask import jsonify

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('vader_lexicon')
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
stop=set(stopwords.words('english'))
stop.discard('not')
from nltk.stem.porter import PorterStemmer
ps=PorterStemmer()
app = Flask(__name__)
with open('model_lr.pkl','rb') as f:
      model=pickle.load(f)
with open('vectorizer.pkl','rb') as f:
      vectorizer=pickle.load(f)
@app.route("/")
def home():
    return render_template('index.html')
@app.route('/sentiment_analysis', methods=['POST','GET'])
def sentiment_analysis():
    text = request.form['text']
    text=text.lower()
    text=nltk.word_tokenize(text)
    y=[]
  
    for i in text:
      if i.isalnum():
        y.append(i)
    text=y[:]
    y.clear()
  
    for i in text:
       if i  not in stop and i not in string.punctuation:
        y.append(i)
    text=y[:]
    y.clear()
    for i in text:
      y.append(ps.stem(i))
    output= " ".join(y)
    vector_input=vectorizer.transform([output])
    sent = SentimentIntensityAnalyzer()
    score = sent.polarity_scores(output)
    y_pred=model.predict(vector_input)
    pos_score = score['pos']
    neg_score = score['neg']
    if (pos_score>neg_score) or y_pred[0] == 1:
        result = 'positive'
    elif (pos_score<neg_score) and y_pred[0] == 0:
        result = 'negative'
    else:
        result="Please enter text "
    return render_template('index.html', result=result)
@app.route("/about")
def about():
    return render_template('about.html')
@app.route("/contact")
def contact():
    return render_template('contact.html')

@app.route('/sentiment_analyser')
def pie_data_bar_chart():
    hours = ['12', '1pm', '2pm', '3pm', '4pm', '5pm','6pm','7pm','8pm','9pm','10pm','11pm']
    visitors = [random.randint(0, 100) for _ in range(len(hours))]

    # Data for the pie chart
    labels = ['Positive', 'Neutral', 'Negative']
    values = [30, 50, 20]
    return render_template("sentiment_analiser.html", hours=hours, visitors=visitors, labels=labels, values=values) 

if __name__ == '__main__':
    app.run(debug=True)