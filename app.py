from flask import Flask, request, jsonify
from flask_cors import CORS; 
from lettre import generate_letter
from resume_parser import parse_resume
from pdfminer.high_level import extract_text
import os



app = Flask(__name__)
CORS(app)
app.config['MAX_CONTENT_LENGTH'] = 2048 * 2048
app.config['UPLOAD_EXTENSIONS'] = ['.pdf']

@app.route("/")
def home():
    return "Welcome to cover letter API official page"

# TODO change argument to have a list of messages from front #
@app.route("/create-letter", methods=["POST"])
def create_letter():
    data = request.get_json()
    language = request.args.get("lng")
    letter = generate_letter(data,False,language);   
    return jsonify(letter[7:]), 201

@app.route("/parse-resume", methods=["POST"])
def file_to_resume():
    file = request.files['file']
    if file.filename != '':
        file_ext = os.path.splitext(file.filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            return "Wrong file format", 400
        else:
            #file.filename = os.path.join('resume/provided', 'resume')
            data = extract_text(file.filename)
            data_parsed = parse_resume(data)
            return jsonify(data_parsed), 200

#if you run the current python file
if __name__ == '__main__':
    app.run(debug=True, port=8000)