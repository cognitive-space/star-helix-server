from django.urls import path

import shelix.stash.views as stash_views

urlpatterns = [
    path('start-log/', stash_views.start_log),
    path('end-log/', stash_views.end_log),
    path('save-log/', stash_views.save_log),
    path('read-log/', stash_views.get_log_content),
]
