from flask import Flask,render_template,request
from google import genai
import os


if GOOGLE_API_KEY:
    # 如果你用的是 API Key
    client = genai.Client(api_key=GOOGLE_API_KEY)
else:
    # 如果你用的是服务账号认证
    client = genai.Client(
        vertexai=True,
        project=GCP_PROJECT_ID,
        location=GCP_LOCATION,
    )




user_name = ""
flag = 1

@app.route("/",methods=["GET","POST"])
def index():
    global flag
    flag = 1
    return(render_template("index.html"))




@app.route("/main",methods=["GET","POST"])
def main():
    global flag,user_name
    if flag==1:
        user_name = request.form.get("q")
        flag = 0
    return(render_template("main.html",r=user_name))

@app.route("/joke",methods=["GET","POST"])
def joke():
    return(render_template("joke.html"))


@app.route("/prediction",methods=["GET","POST"])
def prediction():
    return(render_template("prediction.html"))

@app.route("/DBS",methods=["GET","POST"])
def DBS():
    return(render_template("DBS.html"))

@app.route("/DBS_prediction",methods=["GET","POST"])
def DBS_prediction():
    q = float(request.form.get("q"))
    return(render_template("DBS_prediction.html",r=90.2 + (-50.6*q)))

@app.route("/makersuite",methods=["GET","POST"])
def makersuite():
    return(render_template("makersuite.html"))

@app.route("/makersuite_1", methods=["GET", "POST"])
def makersuite_1():
    q = "Can you help me prepare my tax return?"
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=q
        )
        reply = response.text
    except Exception as e:
        reply = f"Error: {str(e)}"
    return render_template("makersuite_1_reply.html", r=reply)

@app.route("/makersuite_gen", methods=["GET", "POST"])
def makersuite_gen():
    q = request.form.get("q")
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=q
        )
        reply = response.text
    except Exception as e:
        reply = f"Error: {str(e)}"
    return render_template("makersuite_gen_reply.html", r=reply)

if __name__ == "__main__":
    app.run()
