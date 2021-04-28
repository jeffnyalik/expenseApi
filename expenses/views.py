from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from expenses.serializer.serializers import ExpenseSerializers
from expenses.models import Expense
from rest_framework import permissions
from expenses.permissions import IsOwner


class ExpenseListAPIView(ListCreateAPIView):
    serializer_class = ExpenseSerializers
    queryset = Expense.objects.all()
    permissions_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


class ExpenseDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ExpenseSerializers
    queryset = Expense.objects.all()
    permissions_classes = [permissions.IsAuthenticated, IsOwner]
    lookup_field = "id"


    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)