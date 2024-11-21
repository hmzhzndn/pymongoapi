from django.db import models

# Create your models here.

from django.conf import settings

class Student:
    @staticmethod
    def insert_student(data):
        # Insert a new student into the students collection
        result = settings.MONGO_DB.students.insert_one(data)
        return result.inserted_id

    @staticmethod
    def get_student(student_id):
        # Retrieve a student by student_id
        return settings.MONGO_DB.students.find_one({'student_id': student_id})

    @staticmethod
    def update_student(student_id, data):
        # Update a student’s details by student_id
        result = settings.MONGO_DB.students.update_one({'student_id': student_id}, {'$set': data})
        return result.modified_count

    @staticmethod
    def delete_student(student_id):
        # Delete a student by student_id
        result = settings.MONGO_DB.students.delete_one({'student_id': student_id})
        return result.deleted_count

    @staticmethod
    def get_all_students():
        # Retrieve all students
        return list(settings.MONGO_DB.students.find())
