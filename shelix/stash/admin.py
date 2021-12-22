from django.contrib import admin


from shelix.stash.models import Log


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('app', 'process', 'start_ts', 'end_ts', 'logfile')
    search_fields = ('app', 'process')
    date_hierarchy = 'start_ts'
