import csv

from django.conf import settings


def dump(qs, outfile_path=settings.MEDIA_ROOT+'/dump.csv', write=False, separator='\t'):
    print("Dumping")
    model = qs.model
    writer = csv.writer(open(outfile_path, 'w'))
    headers = []
    for field in model._meta.fields:
        headers.append(field.name)
    if write:
        writer.writerow(headers)
    else:
        data = [separator.join(headers)]

    for obj in qs:
        #print(obj)
        row = []
        for field in headers:
            val = getattr(obj, field)
            if callable(val):
                val = val()
            if type(val) == unicode:
                val = val.encode("utf-8")
            row.append(val)
        if write:
            writer.writerow(row)
        else:
            data.append(separator.join(map(str, row)))
    if not write:
        return "<br>".join(data)
