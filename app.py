from flask import Flask,render_template,request,redirect
import speech_recognition as sr
import boto3

app=Flask(__name__)

@app.route('/')
def homePage():
    return render_template('index.html')

@app.route("/", methods=["GET", "POST"])
def index():
    transcript = ""
    if request.method == "POST":
        print("FORM DATA RECEIVED")

        if "file" not in request.files:
            return redirect(request.url)

        file = request.files["file"]
        if file.filename == "":
            return redirect(request.url)

        if file:
            recognizer = sr.Recognizer()
            audioFile = sr.AudioFile(file)
            with audioFile as source:
                data = recognizer.record(source)
            transcript = recognizer.recognize_google(data, key=None)
            client=boto3.client('comprehend')
            response=client.detect_sentiment(Text=transcript,LanguageCode='en')
            transcript=(response['Sentiment'])

    return render_template('index.html', transcript=transcript)

if __name__=="__main__":
    app.run(debug=True)