from django.shortcuts import render
from expenses.serializer.income.serializers import IncomeSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from income.models import Income
from rest_framework import permissions
from expenses.permissions import IsOwner


class ListIncomApiView(ListCreateAPIView):
    serializer_class = IncomeSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    queryset = Income.objects.all()

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


class UpdateIncomeApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = IncomeSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    lookup_field = "id"
    queryset = Income.objects.all()
    
    
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)