from django.contrib import admin
from . models import *

admin.site.register(RequestBlood)
admin.site.register(BloodGroup)

admin.site.register(City)
admin.site.register(Street)
admin.site.register(Donor)
admin.site.register(Profile)
admin.site.register(State)

admin.site.register(District)

admin.site.register(Contact)