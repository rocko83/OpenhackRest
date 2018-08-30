from django.conf.urls import url
from myncraft import views as myncraft_views
urlpatterns = [
    url(r'^$', myncraft_views.index,name='index'),
    url(r'^myncraft/(?P<myncraft>[.\w\-]+)', myncraft_views.myncraft, name='myncraft' )
]
