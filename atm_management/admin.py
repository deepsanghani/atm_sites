from django.contrib import admin
from .models import ATMSite, State, City

class ATMSiteAdmin(admin.ModelAdmin):
    change_list_template = "../templates/excel_upload.html"
    list_display = ('id', 'name', 'site_id', 'address', 'contact_details', 'state_name', 'city_name')

    list_display = ('id', 'name', 'site_id', 'address', 'contact_details', 'get_states', 'get_cities')

    def get_states(self, obj):
        state = State.objects.filter(atm_site=obj).first()
        return state.name

    def get_cities(self, obj):
        city = City.objects.filter(atm_site=obj).first()
        return city.name

    get_states.short_description = 'State'
    get_cities.short_description = 'City'

class StateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'atm_site_id')

    def atm_site_id(self, obj):
        return obj.atm_site.id

class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'atm_site_id')

    def atm_site_id(self, obj):
        return obj.atm_site.id

admin.site.register(ATMSite, ATMSiteAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(City, CityAdmin)

admin.site.site_header = 'All in One ATM'
admin.site.index_title = 'All in One ATM'
admin.site.site_title = 'All in One ATM'
