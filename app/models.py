from datetime import date, datetime, timedelta
from typing import Optional, List
from sqlalchemy import (
    ForeignKey,
    String,
    Integer,
    SmallInteger,
    Text,
    Date,
    DateTime,
    Numeric,
    Interval,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)


# --- Base class ---
class Base(DeclarativeBase):
    pass


# --- Core tables ---

class Program(Base):
    __tablename__ = "program"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cal_year: Mapped[Optional[int]] = mapped_column(SmallInteger)
    program_code: Mapped[Optional[str]] = mapped_column(Text)
    program_name: Mapped[Optional[str]] = mapped_column(Text)
    program_description: Mapped[Optional[str]] = mapped_column(Text)
    start_date: Mapped[Optional[date]] = mapped_column(Date)
    end_date: Mapped[Optional[date]] = mapped_column(Date)

    # Relationships — note names match Survey.program below
    surveys: Mapped[List["Survey"]] = relationship(
        "Survey", back_populates="program", lazy="selectin"
    )


class SurveyType(Base):
    __tablename__ = "survey_type"

    survey_type_cd: Mapped[str] = mapped_column(Text, primary_key=True)
    survey_type_desc: Mapped[Optional[str]] = mapped_column(Text)

    # Relationship name "surveys" matches Survey.survey_type below
    surveys: Mapped[List["Survey"]] = relationship(
        "Survey", back_populates="survey_type", lazy="selectin"
    )


class Survey(Base):
    __tablename__ = "survey"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    survey_type_cd: Mapped[Optional[str]] = mapped_column(ForeignKey("survey_type.survey_type_cd"))
    cal_year: Mapped[Optional[int]] = mapped_column(SmallInteger)
    program_id: Mapped[Optional[int]] = mapped_column(ForeignKey("program.id"))
    program_code: Mapped[Optional[str]] = mapped_column(Text)
    title: Mapped[Optional[str]] = mapped_column(Text)
    description: Mapped[Optional[str]] = mapped_column(Text)
    open_date: Mapped[Optional[date]] = mapped_column(Date)
    close_date: Mapped[Optional[date]] = mapped_column(Date)

    # NOTE: back_populates names must match the attribute names on the other class
    program: Mapped[Optional["Program"]] = relationship(
        "Program", back_populates="surveys", lazy="selectin"
    )
    survey_type: Mapped[Optional["SurveyType"]] = relationship(
        "SurveyType", back_populates="surveys", lazy="selectin"
    )


# class EventType(Base):
#     __tablename__ = "event_type"
#
#     event_type_cd: Mapped[str] = mapped_column(Text, primary_key=True)
#     event_type_desc: Mapped[Optional[str]] = mapped_column(Text)
#
#     base_questions: Mapped[List["BaseQuestion"]] = relationship(back_populates="event_type_rel")


class Category(Base):
    __tablename__ = "category"

    category_cd: Mapped[str] = mapped_column(Text, primary_key=True)
    category_desc: Mapped[Optional[str]] = mapped_column(Text)

    base_questions: Mapped[List["BaseQuestion"]] = relationship(back_populates="category")


# class ResponseGroup(Base):
#     __tablename__ = "response_group"
#
#     group_name: Mapped[str] = mapped_column(Text, primary_key=True)
#     description: Mapped[Optional[str]] = mapped_column(Text)
#
#     values: Mapped[List["ResponseValue"]] = relationship(back_populates="group")
#     base_questions: Mapped[List["BaseQuestion"]] = relationship(back_populates="group")
#
#
# class ResponseValue(Base):
#     __tablename__ = "response_value"
#
#     group_name: Mapped[str] = mapped_column(ForeignKey("response_group.group_name"))
#     group_value: Mapped[Optional[str]] = mapped_column(Text)
#     value_label: Mapped[Optional[str]] = mapped_column(Text)
#
#     group: Mapped["ResponseGroup"] = relationship(back_populates="values")


class BaseQuestion(Base):
    __tablename__ = "base_question"

    db_name: Mapped[str] = mapped_column(Text, primary_key=True)
    # survey_type_cd: Mapped[Optional[str]] = mapped_column(ForeignKey("survey_type.survey_type_cd"))
    # event_type: Mapped[Optional[str]] = mapped_column(ForeignKey("event_type.event_type_cd"))
    category_cd: Mapped[Optional[str]] = mapped_column(ForeignKey("category.category_cd"))
    question_stem: Mapped[Optional[str]] = mapped_column(Text)
    question_text: Mapped[Optional[str]] = mapped_column(Text)
    # group_name: Mapped[Optional[str]] = mapped_column(ForeignKey("response_group.group_name"))
    question_type: Mapped[Optional[str]] = mapped_column(Text)
    conditional: Mapped[Optional[str]] = mapped_column(Text)
    required: Mapped[Optional[str]] = mapped_column(Text)
    cme_cpe: Mapped[Optional[str]] = mapped_column(Text)

    # Relationships
    survey_type: Mapped[Optional["SurveyType"]] = relationship(back_populates="base_questions")
#     event_type_rel: Mapped[Optional["EventType"]] = relationship(back_populates="base_questions")
    category: Mapped[Optional["Category"]] = relationship(back_populates="base_questions")
#     group: Mapped[Optional["ResponseGroup"]] = relationship(back_populates="base_questions")
#
#     crosswalks: Mapped[List["QuestionCrosswalk"]] = relationship(back_populates="base_question")
#     survey_data: Mapped[List["SurveyData"]] = relationship(back_populates="base_question")


# class Survey(Base):
#     __tablename__ = "survey"
#
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     survey_type_cd: Mapped[Optional[str]] = mapped_column(ForeignKey("survey_type.survey_type_cd"))
#     cal_year: Mapped[Optional[int]] = mapped_column(SmallInteger)
#     program_id: Mapped[Optional[int]] = mapped_column(ForeignKey("program.id"))
#     program_code: Mapped[Optional[str]] = mapped_column(Text)
#     title: Mapped[Optional[str]] = mapped_column(Text)
#     description: Mapped[Optional[str]] = mapped_column(Text)
#     open_date: Mapped[Optional[date]] = mapped_column(Date)
#     close_date: Mapped[Optional[date]] = mapped_column(Date)
#
#     survey_type: Mapped[Optional["SurveyType"]] = relationship(back_populates="survey")
#     program: Mapped[Optional["Program"]] = relationship(back_populates="survey")
#
#     # crosswalks: Mapped[List["QuestionCrosswalk"]] = relationship(back_populates="survey")
#     # survey_data: Mapped[List["SurveyData"]] = relationship(back_populates="survey")


# class QuestionCrosswalk(Base):
#     __tablename__ = "question_crosswalk"
#
#     survey_id: Mapped[Optional[int]] = mapped_column(ForeignKey("survey.id"))
#     program_id: Mapped[Optional[int]] = mapped_column(ForeignKey("program.id"))
#     program_code: Mapped[Optional[str]] = mapped_column(Text)
#     cal_year: Mapped[Optional[int]] = mapped_column(SmallInteger)
#     db_name: Mapped[Optional[str]] = mapped_column(ForeignKey("base_question.db_name"))
#     survey_name: Mapped[Optional[str]] = mapped_column(Text)
#
#     survey: Mapped[Optional["Survey"]] = relationship(back_populates="crosswalks")
#     base_question: Mapped[Optional["BaseQuestion"]] = relationship(back_populates="crosswalks")
#
#
# class SurveyData(Base):
#     __tablename__ = "survey_data"
#
#     survey_id: Mapped[Optional[int]] = mapped_column(ForeignKey("survey.id"))
#     program_id: Mapped[Optional[int]] = mapped_column(ForeignKey("program.id"))
#     program_code: Mapped[Optional[str]] = mapped_column(Text)
#     cal_year: Mapped[Optional[int]] = mapped_column(SmallInteger)
#     db_name: Mapped[Optional[str]] = mapped_column(ForeignKey("base_question.db_name"))
#     text_val: Mapped[Optional[str]] = mapped_column(Text)
#     num_val: Mapped[Optional[float]] = mapped_column(Numeric)
#     add_upd_dt: Mapped[Optional[datetime]] = mapped_column(DateTime)
#
#     survey: Mapped[Optional["Survey"]] = relationship(back_populates="survey_data")
#     base_question: Mapped[Optional["BaseQuestion"]] = relationship(back_populates="survey_data")
#
#
# class ProgramActivity(Base):
#     __tablename__ = "program_activity"
#
#     id: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
#     program_id: Mapped[Optional[int]] = mapped_column(ForeignKey("program.id"))
#     program_code: Mapped[Optional[str]] = mapped_column(Text)
#     program_year: Mapped[Optional[int]] = mapped_column(SmallInteger)
#     activity_type: Mapped[Optional[str]] = mapped_column(Text)
#     activity_number: Mapped[Optional[int]] = mapped_column(SmallInteger)
#     activity_name: Mapped[Optional[str]] = mapped_column(Text)
#     activity_date_time: Mapped[Optional[datetime]] = mapped_column(DateTime)
#     activity_duration_min: Mapped[Optional[timedelta]] = mapped_column(Interval)
#
#     program: Mapped[Optional["Program"]] = relationship(back_populates="activities")
#     personnel: Mapped[List["ProgramPersonnel"]] = relationship(back_populates="activity")
#
#
# class ProgramPersonnel(Base):
#     __tablename__ = "program_personnel"
#
#     program_id: Mapped[Optional[int]] = mapped_column(ForeignKey("program.id"))
#     program_code: Mapped[Optional[str]] = mapped_column(Text)
#     program_year: Mapped[Optional[int]] = mapped_column(SmallInteger)
#     activity_id: Mapped[Optional[int]] = mapped_column(ForeignKey("program_activity.id"))
#     activity_type: Mapped[Optional[str]] = mapped_column(Text)
#     activity_number: Mapped[Optional[int]] = mapped_column(SmallInteger)
#     personnel_name: Mapped[Optional[str]] = mapped_column(Text)
#     personnel_number: Mapped[Optional[int]] = mapped_column(SmallInteger)
#
#     program: Mapped[Optional["Program"]] = relationship(back_populates="personnel")
#     activity: Mapped[Optional["ProgramActivity"]] = relationship(back_populates="personnel")
