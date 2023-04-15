from rest_framework.viewsets import ModelViewSet

from abonents.models import Abonent
from limits.models import Limit

from .serializers import AbonentSerializer, LimitSerializer


class AbonentViewSet(ModelViewSet):

    queryset = Abonent.objects.all()
    serializer_class = AbonentSerializer


class LimitViewSet(ModelViewSet):

    queryset = Limit.objects.all()
    serializer_class = LimitSerializer
