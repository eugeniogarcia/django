from django.shortcuts import render

from rest_framework import generics, permissions

from .permisos import IsAuthorOrReadOnly
from .models import Post
from .serializers import PostSerializer

#View for retrieving a queryset from a model
class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

#View for retrieving, updating or deleting an entry in the model 
class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthorOrReadOnly,) # indicamos que hay que estar autenticado para poder usar esta vista
    queryset = Post.objects.all()
    serializer_class = PostSerializer
