from django.contrib import admin


from shelix.stash.models import Log, LogChunk


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('app', 'start_ts', 'end_ts')
    search_fields = ('app',)
    date_hierarchy = 'start_ts'


@admin.register(LogChunk)
class ChunkAdmin(admin.ModelAdmin):
    list_display = ('log', 'created')
    search_fields = ('log__app',)
    date_hierarchy = 'created'
