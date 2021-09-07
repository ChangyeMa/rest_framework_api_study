from django.db.models.query import QuerySet
from django.http.response import HttpResponseForbidden
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.serializers import Serializer
from .models import Article
from .serializers import ArticleSerializer
from django.views.decorators.csrf import csrf_exempt

# When using api_view method
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView  # this is a class based api view

# generics & mixins
from rest_framework import generics
from rest_framework import mixins

# Authentications
from rest_framework.authentication import BasicAuthentication,TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated

#viewset:
from rest_framework import viewsets
from django.shortcuts import get_object_or_404


# Create your views here.
#============================= Model viewset   =============================
class ArticleViewSet(viewsets.ModelViewSet):
    serializer_class=ArticleSerializer
    queryset=Article.objects.all()

#============================= Generic viewset   =============================
# class ArticleViewSet(viewsets.GenericViewSet,mixins.ListModelMixin,mixins.CreateModelMixin,
#                       mixins.UpdateModelMixin,mixins.RetrieveModelMixin, 
#                        mixins.DestroyModelMixin):
#     serializer_class=ArticleSerializer
#     queryset=Article.objects.all()

#============================= viewset method    =============================
# class ArticleViewSet(viewsets.ViewSet):
#     def list(self,request):
#         articles =Article.objects.all()
#         serializer=ArticleSerializer(articles, many=True)
#         return Response(serializer.data) 

#     def create(self,request):
#         serializer = ArticleSerializer(data = request.data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def retrieve(self,request,pk=None):
#         queryset=Article.objects.all()
#         article=get_object_or_404(queryset,pk=pk)
#         serializer=ArticleSerializer(article)
#         return Response(serializer.data)

    # def update(self,request,pk=None):
    #     article= Article.objects.get(pk=pk)
    #     serializer = ArticleSerializer(article, data = request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         # return JsonResponse(serializer.data)
    #         return Response(serializer.data)
    #     # return JsonResponse(serializer.errors,status=400)
    #     return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

#============================= generic method    =============================
class GenericAPIView(generics.GenericAPIView,mixins.ListModelMixin,mixins.CreateModelMixin,
                        mixins.UpdateModelMixin,mixins.RetrieveModelMixin,
                        mixins.DestroyModelMixin):
    serializer_class=ArticleSerializer
    queryset=Article.objects.all()
    lookup_field='id'
    # authentication_classes =[SessionAuthentication,BasicAuthentication]
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]

    def get(self,request,id=None):

        if id:
            return self.retrieve(request)
        else:
            return self.list(request)

    def post(self,request):
        return self.create(request)
    def put(self,request,id=None):
        return self.update(request,id)
    def delete(self,request,id):
        return self.destroy(request,id)
# as we can see from the server that this method has the same effect

#============================= ArticleAPIview  method=============================

class ArticleAPIView(APIView):
    def get(self,request):
        articles =Article.objects.all()
        serializer=ArticleSerializer(articles, many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = ArticleSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ArticleDetails(APIView):
    def get_object(self,id):
        try:
            return Article.objects.get(id=id)
    
        except Article.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self,request,id):
        article= self.get_object(id)
        serializer=ArticleSerializer(article)
        return Response(serializer.data)        

    def put(self,request,id):
        article= self.get_object(id)
        serializer = ArticleSerializer(article, data = request.data)
        if serializer.is_valid():
            serializer.save()
            # return JsonResponse(serializer.data)
            return Response(serializer.data)
        # return JsonResponse(serializer.errors,status=400)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,id):
        article= self.get_object(id)
        article.delete()
        # return HttpResponse(status=204)
        return Response(status=status.HTTP_204_NO_CONTENT)
#=============================article list=============================

# csrf decorator was used in a previous demonstration
# @csrf_exempt    

# another method: api_view
@api_view(['GET','POST'])

def article_list(request):

    if request.method == 'GET':
        articles =Article.objects.all()
        serializer=ArticleSerializer(articles, many=True)
        # return JsonResponse(serializer.data,safe=False)
        return Response(serializer.data)
    
    elif request.method =='POST':
        # data = JSONParser().parse(request)
        serializer = ArticleSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save()
            # return JsonResponse(serializer.data,status=201)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return JsonResponse(serializer.errors,status=400)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#=============================article detail=============================

# csrf decorator was used in a previous demonstration
# @csrf_exempt    

# another method: api_view
@api_view(['GET','PUT','DELETE'])

def article_detail(request,pk):
    try:
        article=Article.objects.get(pk=pk)
    
    except Article.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    
    if request.method =='GET':
        serializer=ArticleSerializer(article)
        # return JsonResponse(serializer.data)
        return Response(serializer.data)

    elif request.method =='PUT':
        # data = JSONParser().parse(request)
        serializer = ArticleSerializer(article, data = request.data)

        if serializer.is_valid():
            serializer.save()
            # return JsonResponse(serializer.data)
            return Response(serializer.data)
        # return JsonResponse(serializer.errors,status=400)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    elif request.method =='DELETE':
        article.delete()
        # return HttpResponse(status=204)
        return Response(status=status.HTTP_204_NO_CONTENT)

#====================================================================================