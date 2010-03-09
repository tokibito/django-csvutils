from csvutils import CSVResponse
from csvutils.utils import UnicodeWriter

__all__ = ('render_to_csv', 'queryset_to_csv')

def render_to_csv(data, *args, **kwargs):
    response = CSVResponse(*args, **kwargs)
    writer = UnicodeWriter(response)
    writer.writerows(data)
    return response

def queryset_to_csv(queryset, fields=None, exclude=None, display=True, *args, **kwargs):
    model = queryset.model
    data = []
    data_fields = []
    # header
    header = []
    for field in model._meta.fields:
        if not fields is None:
            if not field.attname in fields:
                continue
        if not exclude is None:
            if field.attname in exclude:
                continue
        data_fields.append(field)
        if field.rel:
            col = field.verbose_name or field.rel.to.verbose_name or field.attname
        else:
            col = field.verbose_name or field.attname
    data.append(header)
    # body
    for obj in queryset:
        row = []
        for field in data_fields:
            if display:
                val = obj._get_FIELD_display(field)
            else:
                val = getattr(obj, field.attname)
            row.append(val)
        data.append(row)
    return render_to_csv(data, *args, **kwargs)
