from django.urls import path

from api.views import (
            # CreateListAPIViewFunctionBased, 
            # RetrieveUpdateAPIViewFunctionBased,
            # DeleteAPIViewFunctionBased,
            EvrythingAPIViewClassBased,

        )

urlpatterns = [
    # function based
    # path('', CreateListAPIViewFunctionBased, name='apiview'),
    # path('<int:pk>/', RetrieveUpdateAPIViewFunctionBased, name='idapiview'),
    # path('<int:pk>/delete', DeleteAPIViewFunctionBased, name='deleteapiview'),


    # class based
    path('', EvrythingAPIViewClassBased.as_view()),
    path('<int:pk>/', EvrythingAPIViewClassBased.as_view()),  
]

