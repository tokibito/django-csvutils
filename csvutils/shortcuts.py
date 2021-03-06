from django.utils.encoding import force_unicode, smart_str
from django.template.defaultfilters import capfirst
from django.db.models.fields import FieldDoesNotExist

from csvutils.http import CSVResponse
from csvutils.utils import UnicodeWriter

__all__ = ('render_to_csv', 'queryset_to_csv')

def render_to_csv(data, *args, **kwargs):
    encoding = kwargs.pop('encoding', None)
    dialect = kwargs.pop('dialect', None)
    errors = kwargs.pop('errors', None)
    response = CSVResponse(*args, **kwargs)
    writer = UnicodeWriter(response, dialect=dialect, encoding=encoding, errors=errors)
    writer.writerows(data)
    return response

def queryset_to_csv(queryset, fields=None, exclude=None, display=True, *args, **kwargs):
    model = queryset.model
    data = []
    # header
    header = []
    if fields is None:
        data_fields = []
        for field in model._meta.fields:
            if not exclude is None:
                if field.attname in exclude:
                    continue
        data_fields.append(field.attname)
    else:
        data_fields = fields

    for field_name in data_fields:
        try:
            field = model._meta.get_field(field_name)
            if field.rel:
                col = field.verbose_name or field.rel.to.verbose_name or field.attname
            else:
                col = field.verbose_name or field.attname
        except FieldDoesNotExist:
            if field_name == '__unicode__':
                col = force_unicode(model._meta.verbose_name)
            elif field_name == '__str__':
                col = smart_str(model._meta.verbose_name)
            else:
                method = getattr(model, field_name)
                col = getattr(method, 'short_description', method.__name__)
        col = capfirst(col.replace('_', ' '))
        header.append(col)
    data.append(header)
    # body
    for obj in queryset:
        row = []
        for field_name in data_fields:
            try:
                field = model._meta.get_field(field_name)
                if display:
                    if field.rel:
                        rel_obj = getattr(obj, field.rel.related_name or field.name)
                        val = force_unicode(rel_obj)
                    else:
                        val = obj._get_FIELD_display(field)
                else:
                    val = getattr(obj, field.attname)
            except FieldDoesNotExist:
                method = getattr(obj, field_name)
                val = method()
            row.append(val)
        data.append(row)
    return render_to_csv(data, *args, **kwargs)
