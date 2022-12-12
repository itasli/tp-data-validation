# external imports
import numpy as np
import pandera as pa
from marshmallow import Schema, fields, validate

CONTENT_TYPE_LIST = [
    "video", "course", "exercise", "press_article", "web_url", "exam"
]

KEYWORDS_LIST = [
    "maths", "computer_science", "data_science",
    "history", "biology", "physics",
    "arts", "sport", "video_games",
    "economics", "social_sciences", "management"
]

YEAR_LEVEL_LIST = ["L1", "L2", "L3", "M1", "M2"]

# VALIDATE API PARAMETERS


class ParametersSchema(Schema):
    student_id = fields.Int(required=True, validate=validate.Range(1))

    #keyword is not required, but if it is provided, it must be a string in KEYWORDS_LIST
    keyword = fields.Str(required=False, validate=validate.OneOf(KEYWORDS_LIST), load_default=None)

parameter_schema = ParametersSchema()

# VALIDATE DATAFRAMES

CourseContentData = pa.DataFrameSchema(
    {

        #id is positive integer, unique and non null
        "id": pa.Column(pa.Int, pa.Check.ge(0), required=True, unique=True),

        #title is a string, non null
        "title": pa.Column(pa.String, required=True),

        #keyword is a string, non null and in KEYWORDS_LIST
        "keyword": pa.Column(pa.String, required=True, checks=pa.Check.isin(KEYWORDS_LIST)),

        #duration is greater than 0 but lesser than 180, non null
        "duration": pa.Column(pa.Int, pa.Check.ge(0), pa.Check.le(180), required=True),

        #creation_date is a date, can be convert to np.dtype('datetime64[s]'), can be null but if it's not null, it must be greater than 1990-01-01
        "creation_date": pa.Column(np.dtype('datetime64[s]'), pa.Check.greater_than("1990-01-01"), nullable=True, coerce=True),

        #type is string in CONTENT_TYPE_LIST
        "type": pa.Column(pa.String, pa.Check.isin(CONTENT_TYPE_LIST)),

    }
)  # à compléter

StudentProfileData = pa.DataFrameSchema(
    {

        #id is positive integer, unique and non null
        "student_id": pa.Column(pa.Int, pa.Check.ge(0), required=True, unique=True),

        #year_level is a string in YEAR_LEVEL_LIST, can be null
        "year_level": pa.Column(pa.String, pa.Check.isin(YEAR_LEVEL_LIST), nullable=True),

        #area_of_interest is a string in KEYWORDS_LIST, can not be null
        "area_of_interest": pa.Column(pa.String, pa.Check.isin(KEYWORDS_LIST), required=True),
    }
)  # à compléter
