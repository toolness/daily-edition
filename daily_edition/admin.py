from django.contrib import admin
from daily_edition.models import Person, Alias, Site

class AliasInline(admin.TabularInline):
    model = Alias
    extra = 1

class SiteInline(admin.TabularInline):
    model = Site
    extra = 1

class PersonAdmin(admin.ModelAdmin):
    search_fields = ['name']
    inlines = [AliasInline, SiteInline]

admin.site.register(Person, PersonAdmin)
