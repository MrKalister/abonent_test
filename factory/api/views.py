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
    suitable_formats = ('csv', 'xlsx')
    model = Abonent

    def fields_of_model(self):
        return [
            (field.name) for field in self.model._meta.fields
            if field.name != 'id'
        ]

    def post(self, request):
        model_fields = self.fields_of_model()
        try:
            file = next(request.FILES.values())
            if not file:
                raise UploadException('Key for file must be "file".')
            ext = file.name.split('.')[-1]
            if ext not in self.suitable_formats:
                raise UploadException('Unknown file format.')
            if ext == 'csv':
                paramFile = io.TextIOWrapper(file.file)
                # objs = [
                #     Abonent(**self.append_obj(ext, row))
                #     for row in csv.DictReader(paramFile)
                # ]
                objs = [
                    Abonent(
                        **{
                            field: (Limit.objects.get(order_id=row.get(field)) if field == 'limit' else row.get(field))
                            for field in model_fields
                        }
                    )
                    for row in csv.DictReader(paramFile)
                ]
            else:
                sheet = openpyxl.open(file.file, read_only=True).active
                header_row = [cell.value.lower() for cell in sheet[1]]
                objs = [
                    Abonent(
                        **{
                            field: (Limit.objects.get(order_id=row.get(header_row.index(field))) if field == 'limit' else row.get(header_row.index(field)))
                            for field in model_fields
                        }
                    )
                    for row in sheet.iter_rows(min_row=2, values_only=True)
                ]
            if not objs:
                raise UploadException(
                    'An error occurred while reading the file')
            Abonent.objects.bulk_create(objs)
            message = {'message': 'Imported successfully'}
            status_code = status.HTTP_201_CREATED
        except UploadException as e:
            message = {'error': str(e)}
            status_code = status.HTTP_400_BAD_REQUEST
        except Exception as e:
            message = {'error': str(e)}
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        finally:
            return r.Response(message, status=status_code)
