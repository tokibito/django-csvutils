from django.http import HttpResponse

__all__ = ('CSVResponse',)

class CSVResponse(HttpResponse):
    def __init__(self, content='', mimetype=None, status=None, content_type='application/octet-stream', filename=None)
        super(HttpResponseCSV, self).__init__(content, mimetype, status, content_type)
        if not filename is None:
            self.set_filename(filename)

    def set_filename(self, filename):
        self._headers['Content-Disposition'] = 'attachment; filename=%s' % filename
