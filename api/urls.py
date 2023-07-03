from django.urls import path

from api.views import (
            CreateListAPIView, 
            RetrieveUpdateAPIView,
            # update_apiview,
            # delete_apiview,
            # doctorApiView
        )

urlpatterns = [
    path('', CreateListAPIView, name='apiview'),
    path('<int:pk>/', RetrieveUpdateAPIView, name='idapiview'),
    # path('<int:pk>/update', update_apiview, name='updateapiview'),
    # path('<int:pk>/delete', delete_apiview, name='deleteapiview'),
]

