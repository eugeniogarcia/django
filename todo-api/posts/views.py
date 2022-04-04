from rest_framework import generics

from .models import Post
from .serializers import PostSerializer

#View for retrieving a queryset from a model
class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

#View for retrieving, updating or deleting an entry in the model 
class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
