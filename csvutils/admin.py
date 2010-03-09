from django.conf import settings
from django.utils.translation import ugettext as _
from django.template.defaultfilters import slugify

from csvutils.shortcuts import queryset_to_csv

__all__ = ('ExportCSVAction', 'export_csv')

class ExportCSVAction(object):
    short_description = _('Export to CSV')

    def __init__(self, encoding=None):
        self.encoding = encoding or settings.DEFAULT_CHARSET

    @property
    def __name__(self):
        return self.__class__.__name__.lower()

    def __call__(self, modeladmin, request, queryset):
        fields = []
        ld = list(modeladmin.list_display)
        if ld and len(ld) > 0:
            if ld[0] == 'action_checkbox':
                del ld[0]
            fields = ld
        return queryset_to_csv(queryset, fields, encoding=self.encoding,
                filename='%s.csv' % slugify(modeladmin.model.__name__))

export_csv = ExportCSVAction()
