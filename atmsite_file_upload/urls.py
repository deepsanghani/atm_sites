from django.urls import path

from .views import ATMSiteExcelUpload

urlpatterns =[
    path('atm-site', ATMSiteExcelUpload.as_view(), name='upload-atm-site')
]