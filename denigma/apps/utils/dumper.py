import csv

from django.conf import settings


def dump(qs, outfile_path=settings.MEDIA_ROOT+'/dump.csv', write=False, separator='\n',
         writer=False, exclude=()):
    print("Dumping")
    model = qs.model
    if write:
        file_writer = csv.writer(open(outfile_path, 'w'))
    headers = []
    for field in model._meta.fields:
        if field.name in exclude: continue
        headers.append(field.name)
    if write:
        file_writer.writerow(headers)
    elif writer:
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
            if isinstance(val, basestring):
                val = val.replace('\t', '')
            row.append(val)
        if write:
            file_writer.writerow(row)
        elif writer:
            writer.writerow(row)
        else:
            data.append(separator.join(map(str, row)))
    if not write and not writer:
        return "<br>".join(data)
