from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from .models import Student
from bson import ObjectId
from bson.errors import InvalidId

class StudentViewSet(ViewSet):
    def create(self, request):
        try:
            # Parse data from the request
            data = request.data
            # Insert data into MongoDB
            student_id = Student.insert_student(data)
            return Response({'status': 'success', '_id': student_id}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None):
        try:
            student = Student.get_student(pk)
            if not student:
                return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
            student["_id"] = str(student["_id"])  # Convert ObjectId to string for JSON serialization
            return Response(student, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        try:
            data = request.data
            updated_count = Student.update_student(pk, data)
            if updated_count:
                return Response({'status': 'success', 'updated_count': updated_count}, status=status.HTTP_200_OK)
            return Response({'error': 'Update failed'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None):
        try:
            deleted_count = Student.delete_student(pk)
            if deleted_count:
                return Response({'status': 'success', 'deleted_count': deleted_count}, status=status.HTTP_200_OK)
            return Response({'error': 'Delete failed'}, status=status.HTTP_400_BAD_REQUEST)
        except InvalidId:
            return Response({"error": "Invalid student ID format"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        try:
            students = Student.get_all_students()
            for student in students:
                student["_id"] = str(student["_id"])  # Convert ObjectId to string
            return Response({'students': students}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def partial_update(self, request, pk=None):
        try:
            # Parse data from the request
            data = request.data
            try:
                student_id = ObjectId(pk)
            except InvalidId:
                return Response({"error": "Invalid student ID format"}, status=status.HTTP_400_BAD_REQUEST)

            updated_count = Student.update_student(student_id, data)
            if updated_count:
                return Response({'status': 'success', 'updated_count': updated_count}, status=status.HTTP_200_OK)
            return Response({'error': 'Student not found or update failed'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
