from django.db import models
from bson import ObjectId
from django.conf import settings

class Student:
    @staticmethod
    def insert_student(data):
        # Insert a new student into the students collection
        result = settings.MONGO_DB.students.insert_one(data)
        return str(result.inserted_id)  # Return _id as a string

    @staticmethod
    def get_student(ObjectId):
        try:
            # Convert student_id to ObjectId
            student_id = ObjectId(student_id)
        except Exception:
            return None
        return settings.MONGO_DB.students.find_one({'_id': student_id})

    @staticmethod
    def update_student(student_id, data):
        try:
            student_id = ObjectId(student_id)
        except Exception:
            return 0
        result = settings.MONGO_DB.students.update_one({'_id': student_id}, {'$set': data})
        return result.modified_count

    @staticmethod
    def delete_student(student_id):
        try:
            student_id = ObjectId(student_id)
        except Exception:
            return 0
        result = settings.MONGO_DB.students.delete_one({'_id': student_id})
        return result.deleted_count

    @staticmethod
    def get_all_students():
        # Retrieve all students
        return list(settings.MONGO_DB.students.find())
