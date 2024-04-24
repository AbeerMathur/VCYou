from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('app/', include('vcyou_app.urls')),  # Including URLs from the app
]

from django.views.generic import TemplateView

class ReactAppView(TemplateView):
    template_name = "index.html"

urlpatterns += [path('', ReactAppView.as_view()),]

from django.views.generic import TemplateView
urlpatterns += [path('', TemplateView.as_view(template_name='index.html'), name='home'),]