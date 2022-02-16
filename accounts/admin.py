from django.contrib import admin
from .models import User, DoctorProfile, Department, DoctorAvailability, WorkingShift
# Register your models here.
admin.site.register(User)
admin.site.register(Department)

# class DoctorProfileAdmin()
class DoctorAvailabilityInline(admin.StackedInline):
    model = DoctorAvailability

class DoctorWorkingShiftInline(admin.StackedInline):
    model = WorkingShift

class DoctorProfileAdmin(admin.ModelAdmin):
    inlines = [DoctorAvailabilityInline, DoctorWorkingShiftInline]
    
admin.site.register(DoctorProfile, DoctorProfileAdmin)
