# transactions/urls.py
from django.urls import path
from .views import AllTransactionsView, CashInTransactionsView, CashOutTransactionsView

urlpatterns = [
    path('all/', AllTransactionsView.as_view(), name='all-transactions'),
    path('cash-in/', CashInTransactionsView.as_view(), name='cash-in-transactions'),
    path('cash-out/', CashOutTransactionsView.as_view(), name='cash-out-transactions'),
]
