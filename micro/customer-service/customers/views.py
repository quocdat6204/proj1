from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Customer
from .serializers import CustomerSerializer, CustomerRegistrationSerializer, CustomerLoginSerializer
import hashlib

@api_view(['POST'])
def register(request):
    """Register a new customer"""
    serializer = CustomerRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        customer = serializer.save()
        return Response(
            CustomerSerializer(customer).data,
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    """Login customer"""
    serializer = CustomerLoginSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = hashlib.sha256(serializer.validated_data['password'].encode()).hexdigest()
        
        try:
            customer = Customer.objects.get(email=email, password=password)
            return Response(CustomerSerializer(customer).data)
        except Customer.DoesNotExist:
            return Response(
                {'error': 'Invalid email or password'},
                status=status.HTTP_401_UNAUTHORIZED
            )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_customer(request, customer_id):
    """Get customer by ID"""
    try:
        customer = Customer.objects.get(id=customer_id)
        return Response(CustomerSerializer(customer).data)
    except Customer.DoesNotExist:
        return Response(
            {'error': 'Customer not found'},
            status=status.HTTP_404_NOT_FOUND
        )
