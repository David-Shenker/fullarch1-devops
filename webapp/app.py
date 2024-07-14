import argparse
from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from pymongo import MongoClient
import boto3
from flask_bootstrap import Bootstrap

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Flask app configuration')
# parser.add_argument('--secret_key', required=True, help='Secret key for the Flask app')
parser.add_argument('--mongo_uri', required=True, help='MongoDB URI')
parser.add_argument('--s3_bucket', required=True, help='S3 bucket name')
# parser.add_argument('--aws_access_key', required=True, help='AWS access key')
# parser.add_argument('--aws_secret_key', required=True, help='AWS secret key')
parser.add_argument('--aws_region', required=True, help='AWS region')
args = parser.parse_args()

app = Flask(__name__)
app.config['SECRET_KEY'] = args.secret_key
app.config['MONGO_URI'] = args.mongo_uri
app.config['S3_BUCKET'] = args.s3_bucket
# app.config['AWS_ACCESS_KEY'] = args.aws_access_key
# app.config['AWS_SECRET_KEY'] = args.aws_secret_key
app.config['AWS_REGION'] = args.aws_region
bootstrap = Bootstrap(app)

client = MongoClient(app.config['MONGO_URI'])
db = client['student_db']
collection = db['students']

s3 = boto3.client(
    's3',
    # aws_access_key_id=app.config['AWS_ACCESS_KEY'],
    # aws_secret_access_key=app.config['AWS_SECRET_KEY'],
    region_name=app.config['AWS_REGION']
)

class StudentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    student_id = StringField('Student ID', validators=[DataRequired()])
    course = StringField('Course', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = StudentForm()
    if form.validate_on_submit():
        student_data = {
            'name': form.name.data,
            'student_id': form.student_id.data,
            'course': form.course.data
        }
        collection.insert_one(student_data)
        flash('Student data submitted successfully!')
        return redirect(url_for('index'))

    photos = s3.list_objects_v2(Bucket=app.config['S3_BUCKET']).get('Contents', [])
    photo_urls = [
        f"https://{app.config['S3_BUCKET']}.s3.{app.config['AWS_REGION']}.amazonaws.com/{photo['Key']}" for photo in photos
    ]

    return render_template('index.html', form=form, photo_urls=photo_urls)

if __name__ == '__main__':
    app.run(debug=True)
