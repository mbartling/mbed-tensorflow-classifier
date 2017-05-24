import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
import label_image

UPLOAD_FOLDER = '/tmp/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
#            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            fname = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            scores = label_image.predict(fname)
            print scores
            target, score = scores[0]
            if score < 0.70:
                target = "Unsure"
            return '''
            <!doctype html>
            <head>
                <title>Result</title>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
                <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
                <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
            </head>
            <div class="jumbotron text-center">
                <h1>Target=%s, Score=%f</h1>
            </div>
            ''' % (target, score)
            #return redirect(url_for('uploaded_file',
            #                        filename=filename))
    return '''
    <!doctype html>
    <head>
        <title>Upload new File</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
    </head>
    <div class="jumbotron text-center">
        <h1>Magical mbed thing recognizer</h1>
    </div>
    <div class="container">
        <div class="row">
            <div class="col-sm-6"
            <h2>Upload new File</h1>
            <form method=post enctype=multipart/form-data>
              <p><input type=file class="btn" name=file>
                 <input type=submit class="btn" value=Upload>
            </form>
            </div>
    </div>
    </div>
    '''

if __name__ == "__main__":
    app.run(host='0.0.0.0')
