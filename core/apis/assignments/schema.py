from marshmallow import Schema, EXCLUDE, fields, post_load
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
# from marshmallow_enum import EnumField
from core.models.assignments import Assignment, GradeEnum
from core.libs.helpers import GeneralObject


# Define a Marshmallow schema for the Assignment model that extends SQLAlchemyAutoSchema
class AssignmentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Assignment
        unknown = EXCLUDE  # Ignore any unknown fields when loading

    # Specify fields to include/exclude and their attributes
    id = auto_field(required=False, allow_none=True)
    content = auto_field(required=True)
    created_at = auto_field(dump_only=True)
    updated_at = auto_field(dump_only=True)
    teacher_id = auto_field(dump_only=True)
    student_id = auto_field(dump_only=True)
    grade = auto_field(dump_only=True)
    state = auto_field(dump_only=True)

    # Define a post-load method that creates an Assignment object from the loaded data
    @post_load
    def initiate_class(self, data_dict, many, partial):
        # pylint: disable=unused-argument,no-self-use
        return Assignment(**data_dict)


# Define a Marshmallow schema for the payload used to submit an assignment
class AssignmentSubmitSchema(Schema):
    class Meta:
        unknown = EXCLUDE  # Ignore any unknown fields when loading

    # Define fields for the required payload data
    id = fields.Integer(required=True, allow_none=False)
    teacher_id = fields.Integer(required=True, allow_none=False)

    # Define a post-load method that creates a GeneralObject from the loaded data
    @post_load
    def initiate_class(self, data_dict, many, partial):
        # pylint: disable=unused-argument,no-self-use
        return GeneralObject(**data_dict)


# Define a Marshmallow schema for the payload used to grade an assignment
class AssignmentGradeSchema(Schema):
    class Meta:
        unknown = EXCLUDE  # Ignore any unknown fields when loading

    # Define fields for the required payload data
    id = fields.Integer(required=True, allow_none=False)
    grade = fields.String(required=True, allow_none=False)

    # Define a post-load method that creates a GeneralObject from the loaded data
    @post_load
    def initiate_class(self, data_dict,many, partial):
        # pylint: disable=unused-argument,no-self-use
        return GeneralObject(**data_dict)
