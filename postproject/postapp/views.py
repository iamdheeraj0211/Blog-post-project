from django.shortcuts import render
from rest_framework.views import APIView
from .models import PostModel
# from rest_framework.permissions im
from .serializers import PostModelSerializer,UserSerializer,UserLoginSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model,authenticate
from rest_framework.permissions import IsAuthenticated,AllowAny
# from rest_framework.authtoken.models import Token
# User=get_user_model()
from rest_framework.pagination import PageNumberPagination

from rest_framework.authentication import TokenAuthentication

class CustomPagination(PageNumberPagination):
    page_size = 5
    # page_size_query_param = 'page_size'  
    # max_page_size = 100 

class RegisterUserView(APIView):
    permission_classes = (AllowAny,)
    def post(self,request):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"user created succesfuly"})
        return Response(serializer.errors)
    

        
class PostAPIView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[TokenAuthentication]
    pagination_class=CustomPagination
    
    
    def get(self,request,pk=None):
        # queryset=PostModel.objects.all()
        # print(queryset)
        if pk is not None:
            try:
                post=PostModel.objects.get(pk=pk)
                serializer=PostModelSerializer(post)

                return Response(serializer.data)
            except BaseException as e:
                return Response(f"Error:{e}")
        else:
            post=PostModel.objects.all()
            # print("here",request.query_params)
            # title= request.query_params.get('title')
            # body= request.query_params.get('body')
            # print("body",body)
            # author = request.query_params.get('author')
            # if title:
            #     post = post.filter(title__icontains=title)
            # if body:
            #     post = post.filter(body__icontains=body)
            #     print("i am here")
            # if author:
            #     post = post.filter(author__username__icontains=author)
            query_params = {
            'title__icontains': request.query_params.get('title'),
            'body__icontains': request.query_params.get('body'),
            'author__username__icontains': request.query_params.get('author'),
             }
            final_filter={k:v for k,v in query_params.items() if v is not None}
            if final_filter:
                from django.db.models import Q
                query=Q(**final_filter)
                post=post.filter(query)

            serializer=PostModelSerializer(post,many=True)

            return Response(serializer.data)
            
    
    def post(self,request):
        # post=PostModel.objects.create()
        try:
            u=request.data
            print(type(u))
            new_data={"title":u['title'],"body":u['body'],"author":request.user.id}
            print("req update",new_data)
            print(type(new_data))

            serializer=PostModelSerializer(data=new_data)
            print(request.user.username)
            if serializer.is_valid():
                print("valid")
                serializer.save()
                return Response(serializer.data)
        except BaseException as e:
            return Response(f"error:{e}")
    
    def put(self,request,pk):
        try:

            post=get_object_or_404(PostModel,pk=pk)
            u=request.data
            print(type(u))
            new_data={"title":u['title'],"body":u['body'],"author":request.user.id}
            print("re up",new_data)
            serializer=PostModelSerializer(post,data=new_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        except BaseException as e:
            return Response(f"error:{e}")
        # return Response(serializer.errors)
    
    def delete(self,request,pk):
        post=get_object_or_404(PostModel,pk=pk)
        post.delete()
        return Response('Delted:Post deleted successfully')



# class UserLoginView(APIView):
#     def post(self, request):
#         serializer = UserLoginSerializer(data=request.data)
#         print(serializer)
#         if serializer.is_valid():
            
#             username = serializer.validated_data['username']
#             password = serializer.validated_data['password']
#             print("username",username)
#             print("request",request)
#             user = authenticate(request, username=username, password=password)
#             print(user)

#             if user:
#                 token, created = Token.objects.get_or_create(user=user)
#                 return Response({'token': token.key},)
#             else:
#                 return Response({'error': 'Invalid credentials'})
#         else:
#             return Response(serializer.errors)