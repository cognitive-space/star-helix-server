from django.contrib import admin


from shelix.stash.models import Log, LogChunk, LoggingToken


@admin.register(LoggingToken)
class TokenAdmin(admin.ModelAdmin):
    list_display = ('id', 'token', 'active', 'modified')
    list_filter = ('active',)
    search_fields = ('id',)
    date_hierarchy = 'modified'


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
