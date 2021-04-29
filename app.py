from flask import Flask, request, jsonify, abort, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime
import os


today = int(datetime(datetime.now().date().year, datetime.now().date().month, datetime.now().date().day).timestamp())


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
    start_date = db.Column(db.Integer)
    finish_date = db.Column(db.Integer)
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
    if finish_date >= start_date >= today:
        db.session.add(new_course)
        db.session.commit()
        return course_schema.jsonify(new_course), 201
    elif start_date < today:
        return make_response(jsonify({"message": f"'start_date' can't be from past"}), 400)
    else:
        return make_response(jsonify({"message": f"'finish_date' can't be less then 'start_date'"}), 400)


# Get All Courses or only Searched courses or Filter courses by date
@app.route('/course', methods=['GET'])
def get_courses():
    search_string = request.args.get('searchString')
    start_course_from = request.args.get('startCourseFrom')
    start_course_to = request.args.get('startCourseTo')
    finish_course_from = request.args.get('finishCourseFrom')
    finish_course_to = request.args.get('finishCourseTo')
    if search_string:
        result = Course.query.filter(Course.title.like(f'%{search_string}%')).all()
        if len(result) != 0:
            return courses_schema.jsonify(result), 200
        else:
            return make_response(jsonify({"message": f"No results for '{search_string}'"}), 200)

    elif start_course_from and start_course_to and finish_course_from and finish_course_to:
        result = Course.query.\
            filter(Course.start_date >= int(start_course_from)).\
            filter(Course.start_date <= int(start_course_to)).\
            filter(Course.finish_date >= int(finish_course_from)).\
            filter(Course.finish_date <= int(finish_course_to)).all()
        if len(result) != 0:
            return courses_schema.jsonify(result), 200
        else:
            return make_response(jsonify({"message": f"No results for applied filter"}), 200)

    elif start_course_from and start_course_to:
        result = Course.query.\
            filter(Course.start_date >= int(start_course_from)).\
            filter(Course.start_date <= int(start_course_to)).all()
        if len(result) != 0:
            return courses_schema.jsonify(result), 200
        else:
            return make_response(jsonify({"message": f"No results for applied filter"}), 200)

    elif finish_course_from and finish_course_to:
        result = Course.query.\
            filter(Course.finish_date >= int(finish_course_from)).\
            filter(Course.finish_date <= int(finish_course_to)).all()
        if len(result) != 0:
            return courses_schema.jsonify(result), 200
        else:
            return make_response(jsonify({"message": f"No results for applied filter"}), 200)
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


# Update a Course
@app.route('/course/<id>', methods=['PUT'])
def update_course(id):
    course = Course.query.get(id)
    if not course:
        abort(404)
    if not request.json or 'title' not in request.json or 'start_date' not in request.json \
            or 'finish_date' not in request.json or 'qty' not in request.json:
        abort(400)
    title = request.json['title']
    start_date = request.json['start_date']
    finish_date = request.json['finish_date']
    qty = request.json['qty']

    course.title = title
    course.start_date = start_date
    course.finish_date = finish_date
    course.qty = qty

    if finish_date >= start_date >= today:
        db.session.commit()
        return course_schema.jsonify(course), 200
    elif start_date < today:
        return make_response(jsonify({"message": f"'start_date' can't be from past"}), 400)
    else:
        return make_response(jsonify({"message": f"'finish_date' can't be less then 'start_date'"}), 400)


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
