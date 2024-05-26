from django.shortcuts import render
import pandas as pd
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from atm_management.models import ATMSite, State, City
import os

@method_decorator(csrf_exempt, name='dispatch')
class ATMSiteExcelUpload(APIView):
    def post(self, request):
        try:
            uploaded_file = request.FILES['file']
            with open('temp_file.xlsx', 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
            df = pd.read_excel('temp_file.xlsx')
            for index, row in df.iterrows():
                try: 
                    nrow = json.loads(row.to_json())

                    site_id = nrow.get("ID")
                    name = nrow.get("Name")
                    address = nrow.get("Address")
                    state_name = nrow.get("State")
                    city_name = nrow.get("City")
                    contact_details = {
                        "person_name": nrow.get("Person Name"),
                        "phone": nrow.get("Phone"),
                        "email": nrow.get("Email")
                    }
                    atm_site, created = ATMSite.objects.get_or_create(
                        site_id=site_id,
                        defaults={
                            "name": name,
                            "address": address,
                            "contact_details": contact_details
                        }
                    )
                    if not created:
                        atm_site.name = name
                        atm_site.address = address
                        atm_site.contact_details = contact_details
                        atm_site.save()

                    state, created = State.objects.get_or_create(
                        atm_site=atm_site,
                        name=state_name
                    )

                    city, created = City.objects.get_or_create(
                        atm_site=atm_site,
                        name=city_name
                    )
                except Exception as e:
                    print(e)
                    return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            os.remove('temp_file.xlsx')
            return Response({"message": "Excel file read successfully"}, status=status.HTTP_200_OK)
        except KeyError:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)