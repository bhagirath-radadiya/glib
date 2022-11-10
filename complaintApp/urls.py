from django.urls import path, include
from rest_framework import routers
from complaintApp.views import login, logout, registration, complaint, complaintList, statusUpdate, analysis, export
from complaintApp.api import LoginViewSet, RegistrationViewSet, UserComplaintViewSet, WorkerComplaintViewSet, LogoutViewSet

router = routers.SimpleRouter()
router.register(r'login', LoginViewSet)
router.register(r'registration', RegistrationViewSet)
router.register(r'user-complaint', UserComplaintViewSet)
router.register(r'worker-complaint', WorkerComplaintViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('', login),
    path('logout/', logout),
    path('registration/', registration),
    path('complaint/', complaint),
    path('complaint-list/', complaintList),
    path('status-update/', statusUpdate),
    path('analysis/', analysis),
    path('export/', export),
    path('api/logout/', LogoutViewSet.as_view()),
]