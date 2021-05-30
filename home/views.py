from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


class HomePageView(APIView):
    def get(self, request, format=None):
        return Response({'success': 'Welcome to HomePage'}, status=status.HTTP_200_OK)