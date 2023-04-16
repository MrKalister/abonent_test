from abonents.models import Abonent
from limits.models import Limit
from rest_framework.serializers import ModelSerializer


class AbonentSerializer(ModelSerializer):

    class Meta:
        model = Abonent
        fields = ('id', 'username', 'phone', 'limit')


class LimitSerializer(ModelSerializer):

    class Meta:
        model = Limit
        fields = ('order_id', 'name', 'description',)
