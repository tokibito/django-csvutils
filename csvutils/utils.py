import csv

from django.conf import settings
from django.utils.encoding import force_unicode

__all__ = ('UnicodeWriter', 'UnicodeReader')

class UnicodeWriter(object):
    def __init__(self, stream, dialect=csv.excel, encoding=None, **kwds):
        self.writer = csv.writer(stream, dialect=dialect, **kwds)
        self.encoding = encoding or settings.DEFAULT_CHARSET

    def writerow(self, row):
        self.writer.writerow(map(lambda s: force_unicode(s).encode(self.encoding), row))

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

class UnicodeReader(object):
    def __init__(self, stream, dialect=csv.excel, encoding=None, **kwds):
        self.reader = csv.reader(stream, dialect=dialect, **kwds)
        self.encoding = encoding or settings.DEFAULT_CHARSET
        self.line_num = 0 # Needed for DictReader

    def __iter__(self):
        return self

    def next(self):
        return map(lambda s: force_unicode(s, encoding=self.encoding), self.reader.next())
