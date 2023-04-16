import csv
import io

import openpyxl
from rest_framework import permissions, response as r, status, views, viewsets

from abonents.models import Abonent
from api.serializers import AbonentSerializer, LimitSerializer
from limits.models import Limit


class AbonentViewSet(viewsets.ModelViewSet):

    queryset = Abonent.objects.all()
    serializer_class = AbonentSerializer


class LimitViewSet(viewsets.ModelViewSet):

    queryset = Limit.objects.all()
    serializer_class = LimitSerializer


class UploadException(Exception):
    def __init__(self, text):
        self.txt = text


class Upload(views.APIView):
    '''Bulk upload to the database from xlsx and csv files.'''

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        file = next(iter(request.FILES.values()))
        try:
            if not file:
                raise UploadException('Key for file must be "file".')
            ext = file.name.split('.')[-1]
            if ext not in ('csv', 'xlsx'):
                raise UploadException('Unknown file format.')
            if ext == 'csv':
                paramFile = io.TextIOWrapper(file.file)
                objs = [
                    Abonent(
                        username=row.get('username'),
                        phone=row.get('phone'),)
                    for row in list(csv.DictReader(paramFile))]
            else:
                sheet = openpyxl.open(file.file, read_only=True).active
                if (sheet[1][0].value.lower() != "username" or
                        sheet[1][1].value.lower() != "phone"):
                    raise UploadException(
                        'First column must be "username" and'
                        'second column must be "phone"')
                objs = [
                    Abonent(
                        username=sheet[row][0].value,
                        phone=sheet[row][1].value,)
                    for row in range(2, sheet.max_row+1)]
            if not objs:
                raise UploadException(
                    'An error occurred while reading the file')
            Abonent.objects.bulk_create(objs)
            message = ({'message': 'Imported successfully'},
                       status.HTTP_201_CREATED)
        except Exception as e:
            message = ({'error': str(e)},
                       status.HTTP_400_BAD_REQUEST)
        finally:
            return r.Response(*message)
