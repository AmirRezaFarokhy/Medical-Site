from rest_framework.decorators import api_view
from rest_framework.response import Response 
from rest_framework import status

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from api.serializers import SerializetionPatient
from main.models import Doctor, PatientProfile

# Class Based View


# Function Based View

@api_view(['GET', 'POST'])
def CreateListAPIViewFunctionBased(request, pk=None,*args, **kwargs):
    if request.method=='GET':
        if pk is not None:
            obj = get_object_or_404(PatientProfile, pk=pk)
            data = SerializetionPatient(obj, many=False).data 
            return Response(data)

        queyset = PatientProfile.objects.all()
        data = SerializetionPatient(queyset, many=True).data
        return Response(data)
    
    if request.method=='POST':
        serializer = SerializetionPatient(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        
        return Response({"invalid": "not good data"}, 
                         status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['GET', 'PUT'])
def RetrieveUpdateAPIViewFunctionBased(request, pk):
    if request.method=='GET':
        if pk is not None:
            obj = get_object_or_404(PatientProfile, pk=pk)
            data = SerializetionPatient(obj, many=False).data 
            return Response(data)

        return Response({"invalid": "not good url id"}, 
                        status=status.HTTP_400_BAD_REQUEST)

    if request.method=='PUT':
        obj = get_object_or_404(PatientProfile, pk=pk)
        serializer = SerializetionPatient(instance=obj, 
                                          data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data}, 
                             status=status.HTTP_200_OK)
        return Response({"invalid": "not good url id or data"}, 
                        status=status.HTTP_400_BAD_REQUEST)       


@api_view(['GET', 'DELETE'])
def DeleteAPIViewFunctionBased(request, pk):
    try:
        patient = PatientProfile.objects.get(pk=pk)
    except Exception as e:
        return HttpResponse(status=404)

    if request.method=='GET':
        serializer = SerializetionPatient(patient)
        return Response(serializer.data)

    if request.method=='DELETE':
        patient.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    



