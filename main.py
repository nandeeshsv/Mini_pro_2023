import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')

# Load the model and perform prediction
def model_predict(img_path, model):
    # Perform the prediction using the model
    # Replace this with your actual model prediction code
    prediction = "Sample Prediction"
    return prediction

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'filename' not in request.files:
            return render_template('index.html', error='No file selected')

        file1 = request.files['filename']
        
        if file1.filename == '':
            return render_template('index.html', error='No file selected')
        
        if file1:
            filename = secure_filename(file1.filename)
            img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file1.save(img_path)
            
            prediction = model_predict(img_path, model)
            return render_template('index.html', prediction=prediction, filename=filename)

    return render_template('index.html', filename='')

if __name__ == '__main__':
    app.run(debug=True)
