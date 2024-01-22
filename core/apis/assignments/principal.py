from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from core.models.teachers import Teacher
from .schema import AssignmentSchema, AssignmentGradeSchema, Teacherchema

principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)


@principal_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_all_assignments(p):
    """Returns list of assignments"""

    principal_assignments = Assignment.query.filter(Assignment.state == 'SUBMITTED' or  Assignment.state == 'GRADED').all()
    principal_assignments_dump = AssignmentSchema().dump(principal_assignments, many=True)
    return APIResponse.respond(data=principal_assignments_dump)


@principal_assignments_resources.route('/teachers', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_all_teachers(p):
    """Returns list of teachers"""

    principal_teachers = Teacher.query.all()
    principal_teachers_dump = Teacherchema().dump(principal_teachers, many=True)
    return APIResponse.respond(data=principal_teachers_dump)


@principal_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment_draft_assignments(p,incoming_payload):

    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)

    graded_assignment = Assignment.mark_grade_submitted_by_principal(
        _id=grade_assignment_payload.id,
        grade=grade_assignment_payload.grade,
        auth_principal=p
    )
    db.session.commit()
    
    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    
    return APIResponse.respond(data=graded_assignment_dump)
