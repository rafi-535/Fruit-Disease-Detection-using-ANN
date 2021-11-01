import os
from flask import Flask, request, render_template, send_from_directory,session
import mysql.connector

app = Flask(__name__)
# app = Flask(__name__, static_folder="images")



APP_ROOT = os.path.dirname(os.path.abspath(__file__))

classes = ['Apple Blotch','Aspergillus Fruit Rot','Bacterial Blight','Black Rot','Downy Mildew','Gray Mold','Powdery Mildew','Apple scab','RottenApples']

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/user")
def user():
    return render_template("user.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route('/registration')
def registration():
    return render_template("ureg.html",msg='Successfully Registered!!')

@app.route('/userlog',methods=['POST', 'GET'])
def userlog():
    global name, password
    global user

    if request.method == "POST":

        username = request.form['email']
        password1 = request.form['pass']
        print('p')
        mydb = mysql.connector.connect(host="localhost",user="root",passwd="",database="fruit")
        cursor = mydb.cursor()
        sql = "select * from ureg where email='%s' and pwd='%s'" % (username, password1)
        print('q')
        x = cursor.execute(sql)
        print(x)
        results = cursor.fetchall()
        print(results)
        if len(results) > 0:
            print('r')
            #session['user'] = username
            #session['id'] = results[0][0]
            #print(id)
            #print(session['id'])
            return render_template('userhome.html', msg="Login Success")
        else:
            return render_template('user.html', msg="Login Failure!!!")

    return render_template('user.html')


@app.route('/uregback',methods=['POST','GET'])
def uregback():
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        pwd=request.form['pass']
        ph=request.form['ph']
        gender=request.form['gender']

        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="fruit"
        )
        mycursor = mydb.cursor()

        sql = "INSERT INTO ureg (name,email,pwd,ph,gender) VALUES (%s, %s,%s,%s,%s)"
        val = (name,email,pwd,ph,gender)
        mycursor.execute(sql, val)
        mydb.commit()
    return render_template('user.html')
    print("Successfully Registered")

@app.route('/upload1')
def upload1():
    return render_template("upload.html",msg='Successfully logined!!')

@app.route('/userhome')
def userhome():
    return render_template("userhome.html",msg='Successfully logined!!')





@app.route("/upload", methods=["POST"])
def upload():
    if request.method=="POST":
        myfile = request.files['file']
        fn = myfile.filename
        mypath = os.path.join('images/', fn)
        myfile.save(mypath)
        accepted_format=['jpg','jpeg','jfif','png']
        if fn.split('.')[-1] not in accepted_format:
            return render_template('upload1.html',msg="Image formats only accepted here")
        print("{} is the file name", fn)
        print("Accept incoming file:", fn)
        print("Save it to:", mypath)

        #import tensorflow as tf
        import numpy as np
        from tensorflow.keras.preprocessing import image

        from tensorflow.keras.models import load_model
        new_model = load_model('alg/Model.h5')
        # new_model.summary()
        test_image = image.load_img(mypath, target_size=(224, 224))
        print("loading image data------------", test_image)
        test_image = image.img_to_array(test_image)
        print("Image Array values------",test_image)
        test_image=test_image/255
        print("Numeric values of image----------",test_image)
        test_image = np.expand_dims(test_image, axis = 0)
        result = new_model.predict(test_image)
        print("Result values---------",result)
       # prediction=classes[np.argmax(result)]
        print("index values is----",np.argmax(result))
        prediction=classes[np.argmax(result)]
        print("Prediction=============",prediction)
        if prediction=='Apple Blotch':
            msg="Remedies for Apple Blotch: apply a cover spray, trifloxystrobin with thiophanate-methy."
        elif prediction=='Aspergillus Fruit Rot':
            msg="Remedies for Aspergillus Fruit Rot :  filbertworm, leaffooted bugs, and carob moth ."
        elif prediction=='Bacterial Blight':
            msg="Remedies for Bacterial Blight: combination of copper and mancozeb-containing fungicides,spray disinfectants."
        elif prediction=='Black Rot':
            msg="Remedies for Black Rot : Start with clean seed. In warm, humid weather,Maintain hygienic conditions."
        elif prediction=='Downy Mildew':
            msg="Remedies for Downy Mildew : spraying grapevines with a fungicide, spraying the vines."
        elif prediction=='Gray Mold':
            msg="Remedies for Gray Mold : Remove the infected plants and destroy them.,covers the blossom prevents the use of preharvest sprays."
        elif prediction=='Powdery Mildew':
            msg="Remedies for Powdery Mildew : Combine one tablespoon baking soda and one-half teaspoon of liquid, non-detergent soap with one gallon of water."
        elif prediction=='Apple scab':
            msg="Remedies for Apple scab : Remove and destroy the fallen leaf litter,Fungicide."

    #return send_from_directory("images", filename, as_attachment=True)
    return render_template("template.html",image_name=fn, text=prediction,msg=msg)

@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("images", filename)

if __name__ == "__main__":
    app.run(debug=False, threaded=False)

