from django.contrib import admin


from shelix.stash.models import Log


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('app', 'start_ts', 'end_ts', 'logfile')
    search_fields = ('app',)
    date_hierarchy = 'start_ts'
