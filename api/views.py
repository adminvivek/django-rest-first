from functools import partial
import imp
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import TodoSerializer, TimingTodoSerializer
from rest_framework.views import APIView
from rest_framework import status, viewsets
from .models import Todo,TimingTodo
from rest_framework.decorators import action
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
# from rest_framework.authtoken.models import Token
from django.core.paginator import Paginator
from .helpers import paginate
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

# function base api view.

@api_view(['GET'])
def get_api(request):
    return Response({
        'status' : 200,
        'message' : "This is api view"
    })

@api_view(['GET'])
def get_todo(request):
    todo_obj = Todo.objects.all()
    serializer = TodoSerializer(todo_obj, many=True)
    return Response({
            'status'    :   True,
            'message'   :   'Todo fetched',
            'data'  :   serializer.data

        })

@api_view(['POST'])
def post_todo(request):
    try:
        data = request.data
        serializer = TodoSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response({
            'status'    :   True,
            'message'   :   'Success data',
            'data'  :   serializer.data

        })

        return Response({
            'status'    :   False,
            'message'   :   'Invailid data',
            'data'  :   serializer.errors

        })

    except Exception as e:
        print(e)
        return Response({
            'status'    :   False,
            'message'   :   'Something went wrong'
        })        


@api_view(['PATCH'])
def patch_todo(request):
    try:
        data = request.data
        if not data.get('uid'):
            return Response({
            'status'    :   False,
            'message'   :   'uid is required',
            'data' : {}
        }) 

        obj = Todo.objects.get(uid = data.get('uid'))
        serializer = TodoSerializer(obj, data= data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
            'status'    :   True,
            'message'   :   'Success data',
            'data'  :   serializer.data

            })
        return Response({
            'status'    :   False,
            'message'   :   'Invailid data',
            'data'  :   serializer.errors

        })    


    except Exception as e :
        return Response({
            'status'    :   False,
            'message'   :   'Invailid uid',
            'data'  :   {}

        })            



# class base api view.        

class TodoView(APIView):

    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # @method_decorator(cache_page(60*60*2))
    def get(self, request):
        # todo_obj = Todo.objects.all()
        todo_obj = Todo.objects.filter(user = request.user)        
        page = request.GET.get('page',1)        
        page_obj = Paginator(todo_obj, page)
        results = paginate(todo_obj, page_obj,page)
        serializer = TodoSerializer(results['results'], many=True)
        return Response({
                'status'    :   True,
                'message'   :   'Todo fetched',
                'results'  :   {'data' : serializer.data, 'pagination': results['pagination'] }

            })

    def post(self, request):
        try:
            data = request.data
            print(request.user.id)
            data['user'] = request.user.id
            serializer = TodoSerializer(data = data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                'status'    :   True,
                'message'   :   'Success data',
                'data'  :   serializer.data

            })

            return Response({
                'status'    :   False,
                'message'   :   'Invailid data',
                'data'  :   serializer.errors

            })

        except Exception as e:
            print(e)
            return Response({
                'status'    :   False,
                'message'   :   'Something went wrong'
            }) 


    def patch(self, request):
        try:
            data = request.data           
            if not data.get('uid'):
                return Response({
                'status'    :   False,
                'message'   :   'uid is required',
                'data' : {}
            }) 

            obj = Todo.objects.get(uid = data.get('uid'))
            serializer = TodoSerializer(obj, data= data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                'status'    :   True,
                'message'   :   'Success data',
                'data'  :   serializer.data

                })
            return Response({
                'status'    :   False,
                'message'   :   'Invailid data',
                'data'  :   serializer.errors

            })    


        except Exception as e :
            return Response({
                'status'    :   False,
                'message'   :   'Invailid uid',
                'data'  :   {}

            })          

        


# Model ViewSet  API

class TodoViewSet(viewsets.ReadOnlyModelViewSet):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    lookup_field = 'pk'


    @action(detail=False, methods=['GET'])
    def get_timing_todo(self, request):
        objs = TimingTodo.objects.all()
        serializer = TimingTodoSerializer(objs, many=True)
        return Response({
            'status'    :   True,
            'message'   :   'Timing todo fetched',
            'data'  :   serializer.data

        })


    @action(detail=False, methods=['POST'])
    def add_date_to_todo(self, request):
        try:
            data = request.data
            serializer = TimingTodoSerializer(data = data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status'    :   True,
                    'message'   :   'Success data',
                    'data'  :   serializer.data

                })
            return Response({
                'status'    :   False,
                'message'   :   'Invailid data',
                'data'  :   serializer.errors

            })     


        except Exception as e:
            return Response({
                'status'    :   False,
                'message'   :   'Invailid uid',
                'data'  :   {}

            })      