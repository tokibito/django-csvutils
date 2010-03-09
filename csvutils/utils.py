import csv

from django.conf import settings
from django.utils.encoding import smart_encode

__all__ = ('UnicodeWriter',)

class UnicodeWriter(object):
    def __init__(self, stream, dialect=csv.excel, encoding=None, **kwds):
        self.writer = csv.writer(stream, dialect=dialect, **kwds)
        self.encoding = encoding or settings.DEFAULT_CHARSET

    def writerow(self, row):
        self.writer.writerow([s.encode(self.encoding) for s in row])

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)
