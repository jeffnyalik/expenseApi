from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from expenses.serializer.serializers import ExpenseSerializers
from expenses.models import Expense
from rest_framework import permissions
from expenses.permissions import IsOwner
from rest_framework.response import Response


class ExpenseListAPIView(ListCreateAPIView):
    serializer_class = ExpenseSerializers
    queryset = Expense.objects.all().order_by('-date')
    permissions_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def list(self, request):
        queryset = self.queryset.filter(owner=self.request.user);
        serializer = ExpenseSerializers(queryset, many=True)
        return Response(serializer.data);



class ExpenseDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ExpenseSerializers
    queryset = Expense.objects.all()
    permissions_classes = [permissions.IsAuthenticated, IsOwner]
    lookup_field = "id"


    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)