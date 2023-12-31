from django.contrib import admin
from django.urls import include, path # reverse_lazy
# from django.views.generic.base import RedirectView

from polls import views

urlpatterns = [
    # path('', RedirectView.as_view(url=reverse_lazy('admin:index'))),
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('login/', views.login, name='login'),
    path('logout/', views.logout.as_view(), name='logout'),

    # OpenID provider
    path('openid/', include('oidc_provider.urls', namespace='oidc_provider')),
]
