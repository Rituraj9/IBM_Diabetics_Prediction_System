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
                 + "eyJraWQiOiIyMDIwMTEyMTE4MzQiLCJhbGciOiJSUzI1NiJ9.eyJpYW1faWQiOiJJQk1pZC01NTAwMDhSV0FOIiwiaWQiOiJJQk1pZC01NTAwMDhSV0FOIiwicmVhbG1pZCI6IklCTWlkIiwianRpIjoiNjFkNmRiNTAtNDYwZS00YTBjLWE0MzctMDIyNDYzNzg2ODkxIiwiaWRlbnRpZmllciI6IjU1MDAwOFJXQU4iLCJnaXZlbl9uYW1lIjoiUml0dSIsImZhbWlseV9uYW1lIjoicmFqIiwibmFtZSI6IlJpdHUgcmFqIiwiZW1haWwiOiI0bmkxOGlzMDcxX2JAbmllLmFjLmluIiwic3ViIjoiNG5pMThpczA3MV9iQG5pZS5hYy5pbiIsImFjY291bnQiOnsidmFsaWQiOnRydWUsImJzcyI6IjkzZWI1YzY4NDc4YjQ5N2NhZGZmZTg5NzE2ZDBlM2Y3IiwiZnJvemVuIjp0cnVlfSwiaWF0IjoxNjA3ODQ5NTU2LCJleHAiOjE2MDc4NTMxNTYsImlzcyI6Imh0dHBzOi8vaWFtLmJsdWVtaXgubmV0L2lkZW50aXR5IiwiZ3JhbnRfdHlwZSI6InVybjppYm06cGFyYW1zOm9hdXRoOmdyYW50LXR5cGU6YXBpa2V5Iiwic2NvcGUiOiJpYm0gb3BlbmlkIiwiY2xpZW50X2lkIjoiZGVmYXVsdCIsImFjciI6MSwiYW1yIjpbInB3ZCJdfQ.RFy-7zOjzV7dOa_uY6nd4K2NO_Tt-KzKAMLZ_fIv3JQ5zw2htlWudE6BAuEoPmMPV0OELnDD8UJAer9jMzKMyLfdQvxOgdruuk0GY4AFBjS03Xxf_08FDTj4Vi7y30kNQljzFj1zFyVASsiViAaK2RwJkuYPQ3WswPL2Tg1ndZuWPJ2HVEelKi318w4bliGNcVXHZJSKK1-xXrhwvQNXN35XSMSpHafa0tOKUIOhECBsiYwi_KkPu9HM9Q-Y0h84Bw-zAXSRwzrEzEPMs6jV10drNUrBGSuVym0pBXNpnXuOCqXLRiLyLO70CEu7fCRDCPiuPGKD_k5IEfdcHgtghg","refresh_token":"OKCTHr50a_Vektpf7LV8TRrfu99GOw4AezEOOTaOlAZiBSZ3TSgD2MuQkJMe2MUT8YJ_WTIbb9fiPLURP5Lze-VMYghfFHcKjD1XMnIUv60208d1DPC3Nw9ln9HW1VquG6JrD-IzTF0Vmc-pbb1N8nOsnnIFGTClMYpD6ehPeoQErgz8Q0Jp7NNsi8S-9DtwkL03iNu6MSowLLzpX1plc86ejUUy7WCbELFiLDs8d_522-hKE2iDYPI7G0HU_vuiA3j3kSye9KAl_TNOQj4ev1DT0AujOdO1dCbfHTdlvLBVhkfOOsyngBhMOQSGQJ3wB93IaFEnBBl5LcamKGHccjB6a9y_DG_rT_H6xSxkfwhFsEzPGfv0t-o-JEHr8ZYsShsEsfd_8uzK41XmbOQsNSIF7ujZpPylROzpbEJW5g-iapxcyAtPUz0hTpGGYoQ6gSw-DXHWDbSpANTm_Dulvs3_mdTQvUKWTVjTtJsDCRakw4sTRUrm60LFLd8s-7Bv0WWElXqfr-6VFODODN9ET3GZds4StwgUeroFS1gBQ7qrQl7xP-QfGq_JNrvD8jY6t-FSCRiNC1qCHewnJN_3i5pF_llBkIcqMagMEzgQJSX5PytpvmK_8_7_RqHmlzGL8QxJEfYm1_LpnIL-PPlf0bD0oMsS3MeiYX0fFAtbmIDtB83KvOLEA_9-oR_awygklPeNDHw3Rb-APIiuuVmD8YFQ7i55g8RfgUMr7EvaZ7Ws0fZdl_pBqF3kBALwR94qbyUku_EycOZ2FvpDEYDOBZIOz98dUDEZy1GFx-VlchG4WnB1u40TJZYGekk1m2rN5rZlJiKS6JNLMKZIuRX4scjDu9YbmeGe_0AVE6pnrskTHdmb52CWVWxOgRYCxvhCe9anVLQrNm7fU4xJet2b5sYY_SD22MPhEilPwAsZq7PG6Olt1p7wPx9Odc1MdAS-9mZeXZqsN9U67FumQor7m-BdAcy4akTWWHaCXjoXSEfyadNRcd6JYXgLoEmJjuXWnaCBQgQ8riwUqIxjIjiOim8Ku1AwmyEHLk2srGT7Cj5Hb3ypBuxUB3n2NvKxoJ80mCJyCYyixdXACCLBufZw8DsDPw2K_d8hmR9pU-UmjcBL_w"}

        
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
