import tkinter as tk
from textblob import TextBlob
import nltk
from newspaper import Article

window = tk.Tk()
url = ""
def summarize():
    url = urlvariable.get()
    article = Article(url)
    article.download()
    article.parse()
    article.nlp()

    title = article.title
    authors = article.authors
    pu_date = article.publish_date
    summary = article.summary
    analysis = TextBlob(article.text)
    sentiment = analysis.polarity
    entry4title.configure(state="normal")
    titlevariable.set(title)
    entry4title.configure(state="readonly")
    
    entry4authors.configure(state="normal")
    authorsvariable.set(authors)
    entry4authors.configure(state="readonly")

    entry4pu_date.configure(state="normal")
    pu_datevariable.set(pu_date)
    entry4pu_date.configure(state="readonly")

    entry4summary.configure(state="normal")
    entry4summary.delete("1.0", tk.END)
    entry4summary.insert(tk.END, summary)
    entry4summary.configure(state="disabled") 

    entry4sentiment.configure(state="normal")
    sentimentvariable.set(sentiment)
    entry4sentiment.configure(state="readonly")

pu_datevariable = tk.StringVar()
sentimentvariable = tk.StringVar()
authorsvariable = tk.StringVar()
urlvariable = tk.StringVar()
titlevariable = tk.StringVar()
window.geometry("500x750")
title_label = tk.Label(window,text="Article's title")
entry4title = tk.Entry(window,state="readonly",textvariable=titlevariable)
authors_label = tk.Label(window,text="Article's authors")
entry4authors = tk.Entry(window,state="readonly",textvariable=authorsvariable)
pu_date_label = tk.Label(window,text="Article's publication date")
entry4pu_date = tk.Entry(window,state="readonly",textvariable=pu_datevariable)
summary_label = tk.Label(window,text="Article's summary")
entry4summary = tk.Text(window,state="disabled")
url_label = tk.Label(window,text="Enter an Article's url")
entry4url = tk.Entry(window,textvariable=urlvariable)
sentiment_label = tk.Label(window,text="Article's sentiment")
entry4sentiment = tk.Entry(window,state="readonly",textvariable=sentimentvariable)
summarize_btn = tk.Button(window,text="Summarize",command=summarize)

title_label.pack()
entry4title.pack(fill="x")
authors_label.pack()
entry4authors.pack(fill="x")
pu_date_label.pack()
entry4pu_date.pack(fill="x")
summary_label.pack()
entry4summary.pack()
url_label.pack()
entry4url.pack(fill="x")
sentiment_label.pack()
entry4sentiment.pack(fill="x")
summarize_btn.pack()
window.mainloop()