from sqlalchemy import Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import mapped_column, Mapped, relationship, DeclarativeBase
from sqlalchemy.ext.declarative import declared_attr
from datetime import datetime
from typing import Optional

# Define the Base model for all other models to inherit from
class Base(DeclarativeBase):
    pass

# Base Model to auto-generate table names
class BaseModel:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

# User Model
class User(Base, BaseModel):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(200), unique=True)
    password: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(50))  # Admin, Teacher, Guardian
    email: Mapped[Optional[str]] = mapped_column(String(150), unique=True)  # Optional for Teacher/Guardian
    date_created: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

# Class Model
class Class(Base, BaseModel):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    class_name: Mapped[str] = mapped_column(String(100), nullable=False)
    teacher_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("user.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    created_by: Mapped[str] = mapped_column(String(64), default="system")
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_by: Mapped[str] = mapped_column(String(64), default="system")

    teacher: Mapped["User"] = relationship("User", backref="classes")

# Student Model
class Student(Base, BaseModel):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    dob: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    guardian_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False)
    class_id: Mapped[int] = mapped_column(Integer, ForeignKey('class.id'), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    created_by: Mapped[str] = mapped_column(String(64), default="system")
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_by: Mapped[str] = mapped_column(String(64), default="system")

    guardian: Mapped["User"] = relationship("User", backref="students")
    student_class: Mapped["Class"] = relationship("Class", backref="students")

# Teacher Model
class Teacher(Base, BaseModel):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String(150), unique=True, nullable=True)
    class_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("class.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    created_by: Mapped[str] = mapped_column(String(64), default="system")
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_by: Mapped[str] = mapped_column(String(64), default="system")

    teacher_class: Mapped["Class"] = relationship("Class", backref="teachers")

# Fee Payment Model
class FeePayment(Base, BaseModel):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey('student.id'), nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    created_by: Mapped[str] = mapped_column(String(64), default="system")
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_by: Mapped[str] = mapped_column(String(64), default="system")

    student: Mapped["Student"] = relationship("Student", backref="fee_payments")
