from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

# 프/백 연결 테스트 api
def hello_world_test(request):
    if request.method == "GET":
        return JsonResponse({
            'status' : 200,
            'data' : 'hello 뿌셔~'
        })

def connections_test(request):
    if request.method == "GET":
        return JsonResponse({
            'status' : 200,
            'data' : 'connection success~'
        })

# 소셜 로그인 구현을 위한 테스트 api
from .serializers import PostSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from .models import Post

class PostList(APIView):
    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class PostList(APIView):
    def get(self, request, format=None):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

class PostDetail(APIView):
    def get(self, request, id):
        post = get_object_or_404(Post, id=id)
        serializer = PostSerializer(post)
        return Response(serializer.data)

class PostDetail(APIView):
    def delete(self,request,id):
        post = get_object_or_404(Post, id=id)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class KakaoLoginView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        '''
        kakao code 요청
        '''
        client_id = KAKAO_CONFIG['KAKAO_REST_API_KEY']
        redirect_uri = KAKAO_CONFIG['KAKAO_REDIRECT_URI']

        uri = f"{kakao_login_uri}?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
        
        res = redirect(uri)
        return res