from django.urls import path

import shelix.stash.views as stash_views

urlpatterns = [
    path('start-process/', stash_views.start_process),
    path('save-log/', stash_views.save_log),
]
