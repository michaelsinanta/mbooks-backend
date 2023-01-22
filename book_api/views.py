from rest_framework.views import APIView
from book_api.models import Book
from book_api.serializers import BookSerializer
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.parsers import MultiPartParser, FormParser
import datetime

class BookList(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request):
        books = Book.objects.filter(user = request.user)
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

class BookCreate(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        serializer = BookSerializer(
            data = {
                'user': request.user.id,
                'title': request.data["title"],
                'author': request.data["author"],
                'description': request.data["description"],
                'number_of_pages': request.data["number_of_pages"],
                'publish_date': request.data["publish_date"],
                'rating': request.data["rating"],
                'image_url': request.data["image_url"],
            }
        )
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': "Create success",
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        else :
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookDetail(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk):
        try : 
            book = Book.objects.get(pk=pk)
            serializer = BookSerializer(book)
            return Response(serializer.data)
        except :
            return Response({
                'error' : 'Book does not exist'
            }, status=status.HTTP_404_NOT_FOUND)
    
    def patch(self, request, pk):
        try :
            book = Book.objects.get(pk=pk)
            serializer = BookSerializer(book, data = request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status': "Update success",
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except :
            return Response({
                'error' : 'Book does not exist'
            }, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk):
        try :
            book = Book.objects.get(pk=pk)
            book.delete()
            return Response({
                'status': 'Deleted',
            }, status=status.HTTP_201_CREATED)
        except :
            return Response({
                'error' : 'Book does not exist'
            }, status=status.HTTP_404_NOT_FOUND)