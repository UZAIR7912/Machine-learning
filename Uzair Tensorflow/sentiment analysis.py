from textblob import TextBlob

print('write anything to get its sentiment! To quit write:"leave()"')
text = input("you:")
if text == "leave()":
    leave = True
else:
    leave = False
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity
    if sentiment == -1.0:
        feedback = "very negative!"
    elif sentiment == 1.0:
        feedback = "very positive!"
    elif sentiment == 0.0:
        feedback = "neutral"
    elif sentiment >= 0.0 and sentiment <= 1.0:
        feedback = "quite positive"
    elif sentiment <= 0.0 and sentiment >= -1.0:
        feedback = "quite negative"
    print(f"sentiment: {sentiment}")
    print(feedback)
while leave == False:
    text = input("you:")
    if text == "leave()":
        leave = True
    else:
        leave = False
    if leave == False:    
        blob = TextBlob(text)
        sentiment = blob.sentiment.polarity
        if sentiment == -1.0:
           feedback = "very negative!"
        elif sentiment == 1.0:
         feedback = "very positive!"
        elif sentiment == 0.0:
            feedback = "neutral"
        elif sentiment >= 0.0 and sentiment <= 1.0:
           feedback = "quite positive"
        elif sentiment <= 0.0 and sentiment >= -1.0:
            feedback = "quite negative"
        print(f"sentiment: {sentiment}")
        print(feedback)
    else:
        break