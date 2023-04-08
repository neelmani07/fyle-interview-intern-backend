# Import necessary modules
from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from .schema import AssignmentSchema, AssignmentGradeSchema

# Create a new Blueprint for teacher assignments resources
teacher_assignments_resources = Blueprint('teacher_assignments_resources', __name__)

# Route handler for GET /assignments endpoint
@teacher_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.auth_principal
def list_assignments(p):
    """Returns list of assignments"""
    # Get list of assignments for the authenticated teacher
    teachers_assignments = Assignment.get_assignment_by_teacher(p.teacher_id)
    # Serialize list of assignments using AssignmentSchema
    teachers_assignments_dump = AssignmentSchema().dump(teachers_assignments, many=True)
    # Return serialized list of assignments in APIResponse
    return APIResponse.respond(data=teachers_assignments_dump)

# Route handler for POST /assignments/grade endpoint
@teacher_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.auth_principal
def grade_assignment(p, incoming_payload):
    """Grade an assignment"""
    # Validate incoming payload using AssignmentGradeSchema
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)
    # Grade the assignment and return graded assignment
    graded_assignment = Assignment.grade_assignment(
        _id=grade_assignment_payload.id,
        grade=grade_assignment_payload.grade,
        principal=p
    )
    # Commit changes to database
    db.session.commit()
    # Serialize graded assignment using AssignmentSchema
    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    # Return serialized graded assignment in APIResponse
    return APIResponse.respond(data=graded_assignment_dump)
