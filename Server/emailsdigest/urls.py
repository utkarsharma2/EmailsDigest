from django.conf.urls import include, url
from rest_framework import routers
from emailsdigest import views

router = routers.DefaultRouter()

router.register("applications", views.ApplicationViewset)
router.register("email", views.EmailViewset)

urls = [
    url(r"^api/v1/", include(router.urls)),
    url(r"^api/v1/testemail", views.TestEmail.as_view()),
    url(r"^api/v1/enqueue", views.Message.as_view())
]

urlpatterns = urls