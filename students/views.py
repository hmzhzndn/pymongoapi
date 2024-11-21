from django.shortcuts import render

# Create your views here.

# students/views.py
from django.http import JsonResponse
from .models import Student
from bson import ObjectId
from django.views.decorators.csrf import csrf_exempt
import json
from bson.errors import InvalidId
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

@csrf_exempt
def create_student(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        student_id = Student.insert_student(data)
        return JsonResponse({'status': 'success', 'student_id': str(student_id)})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_student(request, student_id):
    try:
        # Convert the student_id to an ObjectId
        student_object_id = ObjectId(student_id)
        
        # Retrieve the student data, excluding `_id` from the result
        student = settings.MONGO_DB.students.find_one({"_id": student_object_id}, {"_id": 0})

        if student is None:
            return JsonResponse({"error": "Student not found"}, status=404)

        return JsonResponse(student)
    
    except InvalidId:
        return JsonResponse({"error": "Invalid student ID format"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def update_student(request, student_id):
    if request.method == 'PUT':
        data = json.loads(request.body)
        updated_count = Student.update_student(student_id, data)
        if updated_count:
            return JsonResponse({'status': 'success', 'updated_count': updated_count})
        else:
            return JsonResponse({'error': 'Update failed'}, status=400)

@csrf_exempt
def delete_student(request, student_id):
    if request.method == 'DELETE':
        deleted_count = Student.delete_student(student_id)
        if deleted_count:
            return JsonResponse({'status': 'success', 'deleted_count': deleted_count})
        else:
            return JsonResponse({'error': 'Delete failed'}, status=400)

@csrf_exempt
def get_all_students(request):
    students = Student.get_all_students()
    return JsonResponse({'students': students})
