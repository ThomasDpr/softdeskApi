from django.contrib import admin

from .models import Contributor, Project


class ContributorInline(admin.TabularInline):
    model = Contributor
    extra = 1
    readonly_fields = ('created_time',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'author', 'created_time')
    search_fields = ('title', 'description')
    inlines = [ContributorInline]  


@admin.register(Contributor)
class ContributorAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'created_time')
    list_filter = ('project', 'user')
