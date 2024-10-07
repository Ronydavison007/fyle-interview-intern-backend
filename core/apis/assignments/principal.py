from flask import Blueprint
from core import db
from core.apis import decorators
from core.libs.exceptions import FyleError
from core.apis.responses import APIResponse
from core.models.assignments import Assignment, GradeEnum, AssignmentStateEnum
from .schema import AssignmentSchema, AssignmentGradeSchema

submitted_assignments = Blueprint('submitted_assignments', __name__)

@submitted_assignments.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of submitted and graded assignments"""
    # Filter assignments by their state (GRADED or SUBMITTED)
    state_filter = [AssignmentStateEnum.GRADED, AssignmentStateEnum.SUBMITTED]
    assignments = Assignment.query.filter(Assignment.state.in_(state_filter)).all()

    # Filter assignments that have a valid grade
    graded_assignments = [assignment for assignment in assignments if assignment.grade in GradeEnum.__members__.values()]

    # Serialize the assignments using the to_dict() method
    serialized_assignments = [assignment.to_dict() for assignment in graded_assignments]

    # Check if any assignments were found
    if serialized_assignments:
        return APIResponse.respond(data=serialized_assignments)
    else:
        return APIResponse.respond(data={"error": 'No submitted and graded assignments found'})

    
@submitted_assignments.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def nondraft_grade_assignment(p, incoming_payload):
    
    try:
       update = AssignmentGradeSchema().load(incoming_payload)
       id = update.id
       grade = update.grade
        # Mark the assignment grade
       nondraft_assignment = Assignment.mark_grade(_id=id, grade=grade, auth_principal=p)
        # Serialize the updated assignment
       serialized_assignment = AssignmentSchema().dump(nondraft_assignment)
       return APIResponse.respond(data=serialized_assignment)
    
    except FyleError as e:
        return APIResponse.respond(data={'message':e.message}, status_code=e.status_code)
    


    

    



    

    
    

    
    