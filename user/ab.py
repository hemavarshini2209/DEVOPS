from flask import Flask, render_template, request, send_file
import boto3

app = Flask(__name__)

# AWS credentials and S3 bucket information
AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
S3_BUCKET_NAME = ''

# Function to write data to text file
def write_to_file(data):
    with open('user_data.txt', 'w') as file:
        file.write(data)

# Function to upload file to S3
def upload_to_s3(file_name, bucket_name):
    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    s3.upload_file(file_name, bucket_name, file_name)

# Function to download file from S3
def download_from_s3(file_name, bucket_name):
    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    s3.download_file(bucket_name, file_name, file_name)
    return file_name

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    data = f"Name: {name}\nEmail: {email}"
    write_to_file(data)
    upload_to_s3('user_data.txt', S3_BUCKET_NAME)
    return render_template('success.html')

@app.route('/download')
def download():
    file_name = download_from_s3('user_data.txt', S3_BUCKET_NAME)
    return send_file(file_name, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
