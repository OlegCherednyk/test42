"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf.urls.static import static

import tests
from tests.views import TestListView, LeaderBoardListView, TestRunView, StartTestView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', TemplateView.as_view(template_name='index.html'), name='index'),

    path('account/', include("user_account.urls")),

    path('test_list/', TestListView.as_view(), name='test_list'),
    path('test_list/leaderboard_list/', LeaderBoardListView.as_view(), name='leaderboard_list'),
    path('test_list/<int:pk>/next', TestRunView.as_view(), name='next'),
    path('test_list/<int:pk>/start', StartTestView.as_view(), name='start'),
]

urlpatterns += \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

handler404 = tests.views.handler404
handler403 = tests.views.handler403
handler400 = tests.views.handler400
handler500 = tests.views.handler500
