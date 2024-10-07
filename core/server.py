from flask import jsonify
from marshmallow.exceptions import ValidationError
from core import app
from core.apis.assignments import student, teacher, principal
from core.libs.exceptions import FyleError
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError

app.register_blueprint(student.student_assignments_resources, url_prefix='/student')
app.register_blueprint(teacher.teacher_assignments_resources, url_prefix='/teacher')
app.register_blueprint(principal.submitted_assignments, url_prefix='/principal')

@app.errorhandler(Exception)
def handle_error(err):
    if isinstance(err, ValidationError):
        return jsonify(
            error=err.__class__.__name__, message=err.messages
        ), 400
    raise err
