from rest_framework import generics, views, status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .utils import checkifvalidIPO

from .serializers import *
from .models import *

class UserRegisterView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class AllPlayerView(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer
    queryset = User.objects.all()

class CompanyListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CompanySerializer
    queryset = Company.objects.all()

class IPOView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = IPOSerializer
    queryset = IPO.objects.all()

class IPOSubscriptionView(generics.ListAPIView):
    serializer_class = SubsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)

class AddIPOSubscriptionView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubscriptionSerializer

    def post(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        company_id = int(request.data['company'])
        offer_bid = int(request.data['offer_bid'])
        quantity = int(request.data['quantity'])
        attempts = len(Subscription.objects.filter(user=user, company=company_id))
        if attempts >= 3:
            return Response({"message" : "Max attempts for this IPO reached!"}, status=status.HTTP_400_BAD_REQUEST)

        if checkifvalidIPO(company_id, quantity, offer_bid):
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user)
            return Response({"message" : "Subscription success"}, status=status.HTTP_201_CREATED)

        return Response({"message" : "try again!"}, status=status.HTTP_400_BAD_REQUEST)

 

