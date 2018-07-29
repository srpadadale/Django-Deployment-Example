from django.conf.urls import url
from Myapp import views

app_name = 'Myapp'

urlpatterns = [
    url(r'^register/$',views.register,name='register'),
    url(r'^user_login/',views.user_login,name='user_login'),
]
