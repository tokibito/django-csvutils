import csv

from django.conf import settings
from django.utils.encoding import force_unicode

__all__ = ('UnicodeWriter', 'UnicodeReader')

class UnicodeWriter(object):
    def __init__(self, stream, dialect=None, encoding=None, errors="strict", **kwds):
        self.writer = csv.writer(stream, dialect=dialect or csv.excel, **kwds)
        self.encoding = encoding or settings.DEFAULT_CHARSET
        self.errors = errors

    def writerow(self, row):
        self.writer.writerow(map(lambda s: force_unicode(s, errors=self.errors).encode(self.encoding, self.errors), row))

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

class UnicodeReader(object):
    def __init__(self, stream, dialect=None, encoding=None, errors="strict", **kwds):
        self.reader = csv.reader(stream, dialect=dialect or csv.excel, **kwds)
        self.encoding = encoding or settings.DEFAULT_CHARSET
        self.line_num = 0 # Needed for DictReader
        self.errors = errors

    def __iter__(self):
        return self

    def next(self):
        return map(lambda s: force_unicode(s, encoding=self.encoding, errors=self.errors), self.reader.next())
