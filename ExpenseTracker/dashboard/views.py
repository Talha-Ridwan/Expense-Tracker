from django.shortcuts import render

# Create your views here.
# transactions/views.py
from rest_framework import generics, permissions
from .models import Transactions
from .serializers import TransactionSerializer

class TransactionBaseView(generics.ListCreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Transactions.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AllTransactionsView(TransactionBaseView):
    pass

class CashInTransactionsView(TransactionBaseView):
    def get_queryset(self):
        return super().get_queryset().filter(type='cash_in')

class CashOutTransactionsView(TransactionBaseView):
    def get_queryset(self):
        return super().get_queryset().filter(type='cash_out')
