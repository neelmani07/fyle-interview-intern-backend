# Import necessary modules
from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment

# Import necessary schemas
from .schema import AssignmentSchema, AssignmentSubmitSchema

# Create a new Blueprint for student assignments resources
student_assignments_resources = Blueprint('student_assignments_resources', __name__)

# Route handler for GET /assignments endpoint
@student_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.auth_principal
def list_assignments(p):
    """Returns list of assignments"""
    # Get list of assignments for the authenticated student
    students_assignments = Assignment.get_assignments_by_student(p.student_id)
    # Serialize list of assignments using AssignmentSchema
    students_assignments_dump = AssignmentSchema().dump(students_assignments, many=True)
    # Return serialized list of assignments in APIResponse
    return APIResponse.respond(data=students_assignments_dump)

# Route handler for POST /assignments endpoint
@student_assignments_resources.route('/assignments', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.auth_principal
def upsert_assignment(p, incoming_payload):
    """Create or Edit an assignment"""
    # Validate incoming payload using AssignmentSchema
    assignment = AssignmentSchema().load(incoming_payload)
    # Set the student ID of the assignment to the authenticated student ID
    assignment.student_id = p.student_id

    # Upsert the assignment and return upserted assignment
    upserted_assignment = Assignment.upsert(assignment)
    db.session.commit()
    # Serialize upserted assignment using AssignmentSchema
    upserted_assignment_dump = AssignmentSchema().dump(upserted_assignment)
    # Return serialized upserted assignment in APIResponse
    return APIResponse.respond(data=upserted_assignment_dump)

# Route handler for POST /assignments/submit endpoint
@student_assignments_resources.route('/assignments/submit', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.auth_principal
def submit_assignment(p, incoming_payload):
    """Submit an assignment"""
    # Validate incoming payload using AssignmentSubmitSchema
    submit_assignment_payload = AssignmentSubmitSchema().load(incoming_payload)

    # Submit the assignment and return submitted assignment
    submitted_assignment = Assignment.submit(
        _id=submit_assignment_payload.id,
        teacher_id=submit_assignment_payload.teacher_id,
        principal=p
    )
    db.session.commit()
    # Serialize submitted assignment using AssignmentSchema
    submitted_assignment_dump = AssignmentSchema().dump(submitted_assignment)
    # Return serialized submitted assignment in APIResponse
    return APIResponse.respond(data=submitted_assignment_dump)
