from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment, AssignmentStateEnum

from .schema import AssignmentSchema, AssignmentGradeSchema
teacher_assignments_resources = Blueprint('teacher_assignments_resources', __name__)


@teacher_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of assignments"""
    teachers_assignments = Assignment.get_assignments_by_teacher()

    updated_assignments = [assignment for assignment in teachers_assignments if assignment.state in [AssignmentStateEnum.GRADED, AssignmentStateEnum.SUBMITTED] and assignment.teacher_id is p.teacher_id]

    teachers_assignments_dump = AssignmentSchema().dump(updated_assignments, many=True)
    return APIResponse.respond(data=teachers_assignments_dump)


@teacher_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p, incoming_payload):
    """Grade an assignment"""
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)
    payload_id = grade_assignment_payload.id
    payload_grade = grade_assignment_payload.grade
    assignment = Assignment.get_by_id(payload_id)
    if assignment is None:
        return APIResponse.respond(data={'error':'FyleError'}, status_code=404)
    if assignment.state == AssignmentStateEnum.SUBMITTED and len(payload_grade) == 1:
        graded_assignment = Assignment.mark_grade(
           _id=payload_id,
           grade=payload_grade,
           auth_principal=p)
        
        db.session.commit()
        graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
        
        return APIResponse.respond(data=graded_assignment_dump, status_code=200)
    elif assignment.state == AssignmentStateEnum.GRADED:
        return APIResponse.respond(data={'message': 'Already graded'},status_code=200)
    else:
        return APIResponse.respond(data={'error':'FyleError'}, status_code=400)
    
    

