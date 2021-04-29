from flask import Flask, request, jsonify, abort, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import literal
import os

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)


# Course Class/Model
class Course(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True)
    start_date = db.Column(db.String(10))
    finish_date = db.Column(db.String(10))
    qty = db.Column(db.Integer)

    def __init__(self, title, start_date, finish_date, qty):
        self.title = title
        self.start_date = start_date
        self.finish_date = finish_date
        self.qty = qty


# Course Schema
class CourseSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'start_date', 'finish_date', 'qty')


# Init schema
course_schema = CourseSchema()
courses_schema = CourseSchema(many=True)


@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


# Create a Course
@app.route('/course', methods=['POST'])
def add_course():
    if not request.json or 'title' not in request.json or 'start_date' not in request.json \
            or 'finish_date' not in request.json or 'qty' not in request.json:
        abort(400)
    title = request.json['title']
    start_date = request.json['start_date']
    finish_date = request.json['finish_date']
    qty = request.json['qty']
    new_course = Course(title, start_date, finish_date, qty)

    db.session.add(new_course)
    db.session.commit()
    return course_schema.jsonify(new_course), 201


# Get All Courses or only Searched courses
@app.route('/course', methods=['GET'])
def get_courses():
    search_string = request.args.get('searchString')
    if search_string:
        result = Course.query.filter(Course.title.like(f'%{search_string}%')).all()
        print(result)
        if len(result) != 0:
            return courses_schema.jsonify(result), 200
        else:
            return make_response(jsonify({'message': 'No courses found'}), 200)
    else:
        all_courses = Course.query.all()
        result = courses_schema.dump(all_courses)
        return jsonify(result), 200


# Get Single Course
@app.route('/course/<id>', methods=['GET'])
def get_course(id):
    course = Course.query.get(id)
    if not course:
        abort(404)
    return course_schema.jsonify(course), 200


@app.route("/courses", methods=['GET'])
def search():
    search_string = request.args.get('searchString')
    result = Course.query.filter(Course.title.like(f'%{search_string}%')).all()
    print(result)
    return courses_schema.jsonify(result), 200


# Update a Course
@app.route('/course/<id>', methods=['PUT'])
def update_course(id):
    course = Course.query.get(id)
    if not course:
        abort(404)
    title = request.json['title']
    start_date = request.json['start_date']
    finish_date = request.json['finish_date']
    qty = request.json['qty']

    course.title = title
    course.start_date = start_date
    course.finish_date = finish_date
    course.qty = qty

    db.session.commit()

    return course_schema.jsonify(course), 200


# Delete Course
@app.route('/course/<id>', methods=['DELETE'])
def delete_course(id):
    course = Course.query.get(id)
    if not course:
        abort(404)
    else:
        db.session.delete(course)
        db.session.commit()

        return course_schema.jsonify(course), 200


# Run Server
if __name__ == '__main__':
    app.run(debug=True)
