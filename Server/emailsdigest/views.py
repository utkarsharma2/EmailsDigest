from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from emailsdigest import controller, models, searializer, tasks


class ApplicationViewset(ModelViewSet):
    """Application viewset"""
    serializer_class = searializer.ApplicationSerializer
    queryset = models.Application.objects.all()


class EmailViewset(ModelViewSet):
    """Application viewset"""
    serializer_class = searializer.EmailSerializer
    queryset = models.Email.objects.all()


class TestEmail(APIView):
    def get(self, request):
        required_params = ['to']
        if not controller.check_params(
            required_params, request.query_params):
            return Response({
                    "error" : "missing required params",
                    "required_params" : required_params
                }, 400)
            
        controller.send_email('test', 'test', [request.query_params.get('to'),])
        return Response({
            "status": "email sent!"
        })


class Message(APIView):
    def post(self, request):
        required_params = ['subject', 'body', 'app']
        if not controller.check_params(
            required_params, request.data):
            return Response({
                    "error" : "missing required params",
                    "required_params" : required_params
                }, 400)
        
        app = models.Application.objects.filter(name=request.data['app'])
        if not app:
            return Response({
                    "error" : f'application with name \'{request.data["app"]}\' does not exist.',
                }, 400)

        email = { 
            'body' : request.data["body"],
            'subject': request.data["subject"]
        }
        
        tasks.label_emails.delay(email, request.data['app'])
        return Response({
                    "status" : "email added to queue",
                }, 200)
