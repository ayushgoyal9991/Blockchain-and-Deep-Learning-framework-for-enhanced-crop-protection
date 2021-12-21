#import required packages
from flask import Flask, render_template, request
from access_blockchain import *
from jinja2 import *
import pickle
import numpy as np
import cv2
import os
import ipfshttpclient

app = Flask("Crop Disease Prediction")
api=ipfshttpclient.connect("/dns/127.0.0.1/tcp/5001")
model = pickle.load(open('model.pkl', 'rb'))

my_address="0x0b71E13F73365c274575c52DF1ad6Bba1c8e4Adb"
private_key="1755838bd5e2f490497c3a808f1dc10556d593b4edc4f0a725550eb60bfb0a52"

addresses,befores,afters,texts=[],[],[],[]
#initial_fund(my_address,private_key,2*10**18)

@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')

def preprocess(image):
  image = cv2.resize(image,(225,225))
  intensity_matrix = np.ones(image.shape,dtype='uint8')*60
  image = np.asarray(image,np.uint8)
  bright_image = cv2.add(image,intensity_matrix)
  image_array = np.asarray(bright_image)
  image_array = np.true_divide(image_array,255)
  return image_array


@app.route("/predict", methods=['GET','POST'])
def predict():
    if request.method == 'POST':
        initial_image = request.form['image']
        image = cv2.imread(initial_image)
        image = preprocess(image)
        image = np.expand_dims(image, axis=0)
        output = model.predict(image)
        output= np.argmax(output)

        my_address=request.form['address']
        private_key=request.form['private_key']
        if len(my_address)==42 and len(private_key)==64:
            pay_ml(my_address,private_key)
            return render_template('predict.html',prediction_text=f"Payment was successful.\nYour Crop Disease id is {output}")#,image=initial_image)
        else:
            return render_template('predict.html',prediction_text=f"Payment was unsuccessful. Please try again")

    else:
        return render_template('predict.html',prediction_text="")

@app.route("/accessall", methods=['GET','POST'])
def accessall():
    global addresses,befores,afters,texts
    if request.method=='POST':
        disease_id=int(request.form['disease_id']) 
        if disease_id not in range(0,9):
            return render_template('accessall.html',result="Invalid disease id")
        all=access_solution(disease_id)
        
        addresses=all[0].split("  ")[1:]
        befores=all[1].split("  ")[1:]
        afters=all[2].split("  ")[1:]
        texts=all[3].split("  ")[1:]
        available=True

        return render_template('accessall.html',available=available,befores=befores,afters=afters)
    else:
        return render_template('accessall.html')

@app.route("/accessall/view",methods=['GET','POST'])
def view():
    if request.method=='POST':
        solution_index=int(request.form['solution_index'])-1
        my_address=request.form['address']
        private_key=request.form['private_key']
        pay_for_solution(my_address,private_key)

        solution_provider="0x"+addresses[solution_index]
        #give_incentive(my_address,private_key,solution_provider)
        return render_template('view.html',before=befores[solution_index],after=afters[solution_index],text=texts[solution_index])
    else:
        return render_template('view.html')
    print(request.form['solution_index'])

@app.route("/upload", methods=['GET','POST'])
def upload():
    if request.method=='POST':
        my_address=request.form['address']
        private_key=request.form['private_key']
        disease_id=int(request.form['disease_id'])
        text=request.form['text']

        before=request.form['before']
        before=api.add(before)
        before=str(before['Hash'])
        after=request.form['after']
        after=api.add(after)
        after=str(after['Hash'])
        #Add these files to ipfs and store their hashes
        if len(my_address)==42 and len(private_key)==64:
            add_to_network(my_address,private_key,disease_id,before,after,text)
            return render_template('upload.html',result=f"The solution has been uploaded successfully")#,image=initial_image)
        return render_template('upload.html')
    else:
        return render_template('upload.html',result="")

#"http://localhost:8080/ipfs/QmVMRnj6GvCPr6yCaEXKvhrxNYzncWg6sYucdSyaQQV9we"
if __name__=="__main__":
    app.run(debug=True)
