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
    serializer_class = IPOSerializer
    queryset = IPO.objects.all()

class IPOSubscriptionView(generics.ListAPIView):
    serializer_class = SubsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)

class LeaderboardView(generics.ListAPIView):
    queryset = (
        Profile.objects.all().order_by("-net_worth")
    )

    serializer_class = ProfileSerializer

class AddIPOSubscriptionView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        company_id = request.data['company']
        offer_bid = int(request.data['offer_bid'])
        no_of_lots = int(request.data['quantity'])

        ipo_comp = Company.objects.filter(company_id = company_id).first()
        ipo = IPO.objects.filter(company=company_id).first()
        print(ipo, ipo_comp)
        quantity = ipo.lot_size * no_of_lots
        print(quantity)
        attempts = len(Subscription.objects.filter(user=user, company=company_id))
        if attempts >= 3:
            return Response({"message" : "Max attempts for this IPO reached!"}, status=status.HTTP_400_BAD_REQUEST)

        if checkifvalidIPO(company_id, quantity, offer_bid):
            comp = Company.objects.filter(company_id=company_id).first()
            sub = Subscription(user=request.user, company=comp, quantity=quantity, offer_bid=offer_bid)
            sub.save()
            return Response({"message" : "Subscription success"}, status=status.HTTP_201_CREATED)

        return Response({"message" : "try again!"}, status=status.HTTP_400_BAD_REQUEST)


class BuyOrderView(generics.ListAPIView):
    serializer_class = BuyOrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return BuyOrder.objects.filter(user=self.request.user)
 
class AddBuyOrderView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BuyOrderSerializer

    def post(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        company_id = int(request.data['company'])
        quantity = int(request.data['quantity'])
        bid_price = int(request.data['bid_price']) 

        comp = Company.objects.filter(company=company_id)
        if (bid_price <= (0.1*comp.last_traded_price+comp.last_traded_price) and bid_price >= (comp.last_traded_price - 0.1*comp.last_traded_price)):
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user)
            return Response({"message" : "Buy Order placed successfully"}, status=status.HTTP_201_CREATED)
        return Response({"message" : "try again!"}, status=status.HTTP_400_BAD_REQUEST)

class SellOrderView(generics.ListAPIView):
    serializer_class = SellOrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SellOrder.objects.filter(user=self.request.user)
    
class AddSellOrderView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SellOrderSerializer

    def post(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        company_id = int(request.data['company'])
        quantity = int(request.data['quantity'])
        ask_price = int(request.data['ask_price']) 

        comp = Company.objects.filter(company=company_id)
        if (ask_price <= (0.1*comp.last_traded_price+comp.last_traded_price) and ask_price >= (comp.last_traded_price - 0.1*comp.last_traded_price)):
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user)
            return Response({"message" : "Sell Order placed successfully"}, status=status.HTTP_201_CREATED)
        return Response({"message" : "try again!"}, status=status.HTTP_400_BAD_REQUEST)
