from flask import Flask, url_for, render_template, redirect
from forms import PredictForm
from flask import request, sessions
import requests
from flask import json
from flask import jsonify
from flask import Request
from flask import Response
import urllib3
import json
# from flask_wtf import FlaskForm

app = Flask(__name__, instance_relative_config=False)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = 'development key' #you will need a secret key

@app.route('/', methods=('GET', 'POST'))

def startApp():
    form = PredictForm()
    return render_template('index.html', form=form)

@app.route('/predict', methods=('GET', 'POST'))
def predict():
    form = PredictForm()
    if form.submit():

        # NOTE: generate iam_token and retrieve ml_instance_id based on provided documentation
        header = {'Content-Type': 'application/json', 'Authorization': 'Bearer '
                 + "eyJraWQiOiIyMDIwMTEyMTE4MzQiLCJhbGciOiJSUzI1NiJ9.eyJpYW1faWQiOiJJQk1pZC01NTAwMDhSV0FOIiwiaWQiOiJJQk1pZC01NTAwMDhSV0FOIiwicmVhbG1pZCI6IklCTWlkIiwianRpIjoiZWZjNjRiZGEtNjg5NS00NDM0LWFjMGUtMzcwMTU0MDE5YzIzIiwiaWRlbnRpZmllciI6IjU1MDAwOFJXQU4iLCJnaXZlbl9uYW1lIjoiUml0dSIsImZhbWlseV9uYW1lIjoicmFqIiwibmFtZSI6IlJpdHUgcmFqIiwiZW1haWwiOiI0bmkxOGlzMDcxX2JAbmllLmFjLmluIiwic3ViIjoiNG5pMThpczA3MV9iQG5pZS5hYy5pbiIsImFjY291bnQiOnsidmFsaWQiOnRydWUsImJzcyI6IjkzZWI1YzY4NDc4YjQ5N2NhZGZmZTg5NzE2ZDBlM2Y3IiwiZnJvemVuIjp0cnVlfSwiaWF0IjoxNjA3ODY5MTUwLCJleHAiOjE2MDc4NzI3NTAsImlzcyI6Imh0dHBzOi8vaWFtLmJsdWVtaXgubmV0L2lkZW50aXR5IiwiZ3JhbnRfdHlwZSI6InVybjppYm06cGFyYW1zOm9hdXRoOmdyYW50LXR5cGU6YXBpa2V5Iiwic2NvcGUiOiJpYm0gb3BlbmlkIiwiY2xpZW50X2lkIjoiZGVmYXVsdCIsImFjciI6MSwiYW1yIjpbInB3ZCJdfQ.bHf38EPnx79HiUky8kx48ZT3n47twChQBZ7EtMNiV6IYq26vZf9boRhl7cH2un1ec_bTn9mlTVbeR5Z9D5GejpbK6cV-bbQvAxyhQeO_8QxOakTbVjrb7XB0fJq6H0cTw3g4VgN2iPM0GmSkmUqG4nHcttkA6GIX38qTRi0vwv5Y4fq-uiQPqQEnPsm8hZ-x-slNSifNhJa9qQ4aimzkTLofihI1ou9ZugAwAr_tibZ-2pKE2q3d1MAMwomN1sUgP9SfXnZAEWcDA9tekGLdvWy828lcKcVJwXdI2jyMdq-dfVc7p6IATWYfldH7fbIhoCdzwnfpQn7hkJCSIsiNhQ","refresh_token":"OKCABPadvvxWIgVb69e4uIyhyx_AnKa_gOJtx-rgeAM0m8_S1pFFoHUbvVkcBHeV9YSNK-o26jCgEPw0-Qn2aIkjZGy2jhmzOzhAXoX5KI-X_yT7c_RT-hyvsy_3oxbczx8Az0kB1y656PfhIThiOtkSw9pNvDfUFUwDwH3hsmmvHO_89LC23SCVBdto183t1Mf8kw3tyaJJvaLFs74UZ8opbeeYJ0Pnng96f_fiXdfMgemT30uZD2zFexNAsQ3SS4EyoXPhm5ZwnuuejWeHZt6d5lAAdX1Zly5FFhV4vC26aFZBOJOjyUTAQph5WbMFS4j8jyRZIbbfnM_rPSW6D6QhNr_MifPxx3wtFGQhD2tpIq220dfR_u0jWya7Ad6peNWJ8T4fzpkP9TK9XXe7CPAeRnhW_8-wq-HO3DjX20HT3Tj7xAfvw9QYyyPFb2Q56C5zg6XqHtsbAA5F9J8tCRbPcU_yjLyQzi_s_L8_Yiah5K49oWwD3M17EYNLKifQ0SKMAAGVczw9ApAqh0QBubEaMKES1559Sy5meqSslyiOAxIaAkcDB7UgrbcKiflHgdOfNXr3bGMXbDOEuOdGkGn98PQ3OSvSwxPKOA9bpZegYeoQtAWCC5mcpx7zL_Aux6mmIVhAS6q-TV0bwk7n4qUm9QTgZbnm92fkuBKvK9Kww04QC43WiqJ_1fXIAou4le9gpiZMaqXUxnZNFz7YEM1QQSxqGozA-majfeSqGRUMpk1oBLteWwn-1hDbptAxaEUZQfC__Fn6CHL-oq0t6zxEzDtvxW3knZNq38LFUevxkHAptyiAjHIo6BjGX_68-hFUeoPVXPO3SJaZkHuAPBQJ-7T0bN1eCFonkLKdxVWhdCRMrgFJULaNJ-ErVO0o4mhlnlxCaHbbpbyizsFbMai0canDQ1sykPoTlAuhKd2QYAG5MonfRPsBEMxOMIt_otgKQ5uljRZWCgjYCFdogyQ-oaEyHYCVaAvYgjhCkVYihzs6Qnv1BQ8y-pWV9j6gcBYybxm3X57x6k2Jtk0hZdbjbBko3fOE8PTnqZ4lDLTFsPUdDqkPsjS3P_W7ZpT0XEcqByZmda1pxoqdm3yt3-nfmxHVUt_fQV1lmqmnLv8Ssw"}

        
        python_object = [int(form.Pregnancies.data), int(form.Glucose.data), int(form.BloodPressure.data),int(form.SkinThickness.data),int(form.Insulin.data),float(form.BMI.data),float(form.DiabetesPedigreeFunction.data),int(form.Age.data)]
        #Transform python objects to  Json
        #print(python_object)
        userInput = []
        userInput.append(python_object)

        # NOTE: manually define and pass the array(s) of values to be scored in the next line
        payload_scoring = {"input_data": [{"fields": ["Pregnancies", "Glucose","BloodPressure","SkinThickness","Insulin","BMI","DiabetesPedigreeFunction","Age"], "values": userInput }]}
        #print(payload_scoring)
        response_scoring = requests.post("https://us-south.ml.cloud.ibm.com/ml/v4/deployments/167da3fa-d770-4b95-b318-46e6b9846d5c/predictions?version=2020-12-13", json=payload_scoring, headers=header)
        #print(response_scoring.text)
        output = json.loads(response_scoring.text)
        #print(output)
        for key in output:
          ab = output[key]
        

        for key in ab[0]:
          bc = ab[0][key]

        #print(bc)
  
        form.abc = bc[0][0] # this returns the response back to the front page
        return render_template('index.html', form=form)

if __name__ == "__main__":
    app.run(debug=True)
