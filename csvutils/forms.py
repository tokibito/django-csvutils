#:coding=utf-8:

import csv

from django import forms
from django.forms.formsets import (
    TOTAL_FORM_COUNT, INITIAL_FORM_COUNT, MAX_NUM_FORM_COUNT,
    DELETION_FIELD_NAME, BaseFormSet, formset_factory
)
from django.forms.models import modelformset_factory, BaseModelFormSet

from utils import UnicodeReader

def csv_formset_factory(csvfile, form, formset=None, can_delete=False, update=False, encoding=None):
    """
    
    """
    if hasattr(form._meta, "model"): # ModelForm
        formset_cls = modelformset_factory(
            model=form._meta.model,
            form=form,
            formset=formset or BaseModelFormSet,
            extra=0,
            can_delete=can_delete,
        )
    else:
        formset_cls = formset_factory(
            form=form,
            formset=formset or BaseFormSet,
            extra=0,
            can_delete=can_delete
        )

    fieldnames = form.base_fields.keys()
    if can_delete: 
        # The last field is a boolean delete flag
        fieldnames.append(DELETION_FIELD_NAME)

    data = {}
    reader = csv.DictReader(csvfile, fieldnames=fieldnames)
    reader.reader = UnicodeReader(csvfile, encoding=encoding) 
    form_prefix = formset_cls.get_default_prefix()
    form_count = 0
    for index, data_dict in enumerate(reader):
        data.update(dict([
            ("%s-%d-%s" % (form_prefix, index, field_name), value)
                for field_name, value in data_dict.iteritems()
        ]))
        form_count += 1
    import pdb;pdb.set_trace()
    data['%s-%s' % (form_prefix, TOTAL_FORM_COUNT)] = form_count
    data['%s-%s' % (form_prefix, INITIAL_FORM_COUNT)] = form_count if update else 0
    data['%s-%s' % (form_prefix,  MAX_NUM_FORM_COUNT)] = form_count if update else 0
    return formset_cls(data)
