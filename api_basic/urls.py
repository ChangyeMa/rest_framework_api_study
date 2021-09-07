
from MyProject import urls
from django.urls import path,include
from .views import article_list,article_detail, ArticleAPIView,ArticleViewSet, ArticleDetails,GenericAPIView
from rest_framework.routers import DefaultRouter


router=DefaultRouter()
router.register('article',ArticleViewSet,basename='article')

urlpatterns = [
    path('viewset/',include(router.urls)),
    path('viewset/int:<pk>/',include(router.urls)),

    # normal method:
    # path('article/', article_list),
    # path('detail/<int:pk>', article_detail),

    # method: class based api view
    # Since using class here we need to add ".as_view()" otherwise it will say that 2 input given 
    path('article/', ArticleAPIView.as_view()),
    path('detail/<int:id>/', ArticleDetails.as_view()),
    path('generic/article/<int:id>/', GenericAPIView.as_view()),
]
