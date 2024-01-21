from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from core.models.teachers import Teacher

from .schema import AssignmentSchema, AssignmentGradeSchema
principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)


@principal_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of assignments"""

    principal_assignments = Assignment.query.filter(Assignment.state == 'SUBMITTED' or  Assignment.state == 'GRADED').all()
    principal_assignments_dump = AssignmentSchema().dump(principal_assignments, many=True)
    return APIResponse.respond(data=principal_assignments_dump)
