from django.conf import settings
from django.utils.translation import ugettext as _

from csvutils.shortcuts import queryset_to_csv

__all__ = ('ExportCSVAction', 'export_csv')

class ExportCSVAction(object):
    short_description = _('Export to CSV')

    def __init__(self, encoding=None):
        self.encoding = encoding or settings.DEFAULT_CHARSET

    def __call__(self, modeladmin, request, queryset):
        fields = []
        ld = modeladmin.list_display
        if ld and len(ld) > 0:
            if ld[0] == 'action_checkbox':
                del ld[0]
            fields = ld
        return queryset_to_csv(queryset, fields)

export_csv = ExportCSVAction()
