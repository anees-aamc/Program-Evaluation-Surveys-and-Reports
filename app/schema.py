from datetime import date, datetime, timedelta
from pydantic import BaseModel
from typing import Optional, List


# -------------------------------------------------
# 🔹 Base class for all schemas
# -------------------------------------------------
class BaseSchema(BaseModel):
    """Base schema with FastAPI ORM compatibility."""
    model_config = {"from_attributes": True}


# -------------------------------------------------
# 🔹 Core (flat) schemas — used for create/update
# -------------------------------------------------

class Program(BaseSchema):
    id: Optional[int] = None
    cal_year: Optional[int] = None
    program_code: Optional[str] = None
    program_name: Optional[str] = None
    program_description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None


class ProgramUpdate(BaseSchema):
    id: Optional[int] = None
    cal_year: Optional[int] = None
    program_code: Optional[str] = None
    program_name: Optional[str] = None
    program_description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None


class SurveyType(BaseSchema):
    survey_type_cd: str
    survey_type_desc: Optional[str] = None


class SurveyTypeUpdate(BaseSchema):
    survey_type_cd: Optional[str] = None
    survey_type_desc: Optional[str] = None


class Survey(BaseSchema):
    id: Optional[int] = None
    survey_type_cd: Optional[str] = None        # FK → survey_type
    cal_year: Optional[int] = None
    program_id: Optional[int] = None            # FK → program
    program_code: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    open_date: Optional[date] = None
    close_date: Optional[date] = None


class SurveyUpdate(BaseSchema):
    id: Optional[int] = None
    survey_type_cd: Optional[str] = None        # FK → survey_type
    cal_year: Optional[int] = None
    program_id: Optional[int] = None            # FK → program
    program_code: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    open_date: Optional[date] = None
    close_date: Optional[date] = None


class EventType(BaseSchema):
    event_type_cd: str
    event_type_desc: Optional[str] = None


class Category(BaseSchema):
    category_cd: str
    category_desc: Optional[str] = None


class CategoryUpdate(BaseSchema):
    category_cd: Optional[str] = None
    category_desc: Optional[str] = None


class ResponseGroup(BaseSchema):
    group_name: str
    description: Optional[str] = None


class ResponseValue(BaseSchema):
    group_name: str  # FK → response_group.group_name
    group_value: Optional[str] = None
    value_label: Optional[str] = None


class BaseQuestion(BaseSchema):
    db_name: str
    survey_type_cd: Optional[str] = None        # FK → survey_type
    # event_type: Optional[str] = None            # FK → event_type
    category_cd: Optional[str] = None           # FK → category
    question_stem: Optional[str] = None
    question_text: Optional[str] = None
    # group_name: Optional[str] = None            # FK → response_group
    question_type: Optional[str] = None
    conditional: Optional[str] = None
    required: Optional[str] = None
    cme_cpe: Optional[str] = None


class QuestionCrosswalk(BaseSchema):
    survey_id: Optional[int] = None             # FK → survey
    program_id: Optional[int] = None            # FK → program
    program_code: Optional[str] = None
    cal_year: Optional[int] = None
    db_name: Optional[str] = None               # FK → base_question
    survey_name: Optional[str] = None


class SurveyData(BaseSchema):
    survey_id: Optional[int] = None             # FK → survey
    program_id: Optional[int] = None            # FK → program
    program_code: Optional[str] = None
    cal_year: Optional[int] = None
    db_name: Optional[str] = None               # FK → base_question
    text_val: Optional[str] = None
    num_val: Optional[float] = None
    add_upd_dt: Optional[datetime] = None


class ProgramActivity(BaseSchema):
    id: int
    program_id: Optional[int] = None            # FK → program
    program_code: Optional[str] = None
    program_year: Optional[int] = None
    activity_type: Optional[str] = None
    activity_number: Optional[int] = None
    activity_name: Optional[str] = None
    activity_date_time: Optional[datetime] = None
    activity_duration_min: Optional[timedelta] = None


class ProgramPersonnel(BaseSchema):
    program_id: Optional[int] = None            # FK → program
    program_code: Optional[str] = None
    program_year: Optional[int] = None
    activity_id: Optional[int] = None           # FK → program_activity
    activity_type: Optional[str] = None
    activity_number: Optional[int] = None
    personnel_name: Optional[str] = None
    personnel_number: Optional[int] = None


# -------------------------------------------------
# 🔹 Nested (detailed) schemas — for API responses
# -------------------------------------------------

class ResponseGroupDetail(ResponseGroup):
    """Include group values."""
    values: Optional[List[ResponseValue]] = None


class BaseQuestionDetail(BaseQuestion):
    """Include foreign key references."""
    survey_type: Optional[SurveyType] = None
    event_type_rel: Optional[EventType] = None
    category: Optional[Category] = None
    group: Optional[ResponseGroupDetail] = None


class ProgramActivityDetail(ProgramActivity):
    personnel: Optional[List[ProgramPersonnel]] = None


class ProgramDetail(Program):
    """Program with related activities and personnel."""
    activities: Optional[List[ProgramActivityDetail]] = None
    personnel: Optional[List[ProgramPersonnel]] = None
    surveys: Optional[List[Survey]] = None


class SurveyDetail(Survey):
    """Survey including nested program and survey type."""
    program: Optional[Program] = None
    survey_type_cd: Optional[SurveyType] = None
    survey_data: Optional[List[SurveyData]] = None
    crosswalks: Optional[List[QuestionCrosswalk]] = None


class QuestionCrosswalkDetail(QuestionCrosswalk):
    survey: Optional[Survey] = None
    base_question: Optional[BaseQuestionDetail] = None


class SurveyDataDetail(SurveyData):
    survey: Optional[Survey] = None
    base_question: Optional[BaseQuestionDetail] = None
