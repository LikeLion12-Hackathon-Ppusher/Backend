from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

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