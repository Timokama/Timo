from django.contrib import admin
from .models import Person, Group,Membership 
class GroupInline(admin.TabularInline):
    model = Group
    extra = 1

class PersonAdmin(admin.ModelAdmin):
    fieldset = [
        (None,               {'fields': ['name'], 'classes': ['collapse']}),
    ]
    #inlines = [GroupInline]

class MembershipAdmin(admin.ModelAdmin):
    list_display = ('person', 'date_joined', 'group')

admin.site.register(Group)
admin.site.register(Membership, MembershipAdmin)
admin.site.register(Person, PersonAdmin)