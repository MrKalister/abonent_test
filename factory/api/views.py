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
    pass


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

    def append_obj(self, row, header_row=None):
        '''Return dict with fields and values for upload in Abonent.'''

        data = {}
        for field in self.fields_of_model():
            if field == 'limit' and header_row:
                order_id = row[header_row.index(field)]
                limit_obj = Limit.objects.get_or_none(order_id=order_id)
                if not limit_obj:
                    raise UploadException(
                        f'In the database no order_id with {order_id} number.')
                data[field] = limit_obj
            elif field == 'limit' and not header_row:
                limit_obj = Limit.objects.get_or_none(
                    order_id=row.get(field))
                if not limit_obj:
                    raise UploadException('In the database no order_id with '
                                          f'{row.get(field)} number.')
                data[field] = limit_obj
            elif field != 'limit' and header_row:
                data[field] = row[header_row.index(field)]
            elif field != 'limit' and not header_row:
                data[field] = row.get(field)
        return data

    def post(self, request):
        '''Create objects in Abonent tables.'''

        model_fields = self.fields_of_model()
        try:
            file = next(request.FILES.values())
            if not file:
                raise UploadException('Key for file must be "file".')
            ext = file.name.split('.')[-1]
            if ext not in self.suitable_formats:
                raise UploadException('Unknown file format.')
            if ext == 'csv':
                book = io.TextIOWrapper(file.file)
                header_row = next(csv.reader(book))
                book.seek(0)
                if header_row[:len(model_fields)] != model_fields:
                    raise UploadException(
                        'Fields in file do not match the model fields')
                objs = [Abonent(**self.append_obj(row))
                        for row in csv.DictReader(book)]
            else:
                book = openpyxl.open(file.file, read_only=True).active
                header_row = [cell.value.lower() for cell in book[1]]
                if header_row[:len(model_fields)] != model_fields:
                    raise UploadException(
                        'Fields in file do not match the model fields')
                objs = [Abonent(**self.append_obj(row, header_row))
                        for row in book.iter_rows(min_row=2, values_only=True)]
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
