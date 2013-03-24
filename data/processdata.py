import itertools
import pickle
import csv
import collections
import string


files = [
    'data/all_hospitals.csv',
    'data/all_gps.csv',
    'data/all_pharmacies.csv',
    'data/all_dentists.csv',
    'data/all_opticians.csv',
    'data/sexual_health.csv',
    'data/travel_clinics.csv',
    ]
pcfile = 'data/postcodes.csv'

outputfile = 'all_data.csv'

def get_headers(filename):
    """
    Get the first header row so we can see what fields are present in all files
    """
    with open(filename) as f:
        return csv.reader(f).next()


def map_field_name(fieldname):
    """
    At least one field has a different name across datasets
    """
    fn = fieldname.lower()
    if fn == 'dataset code code':
        return 'dataset code'
    return fn


def get_combined_fields(filenames):
    # Using this as an ordered set
    all_fields = collections.OrderedDict()
    n = 0
    for f in filenames:
        hs = get_headers(f)
        for h in hs:
            f = map_field_name(h)
            if not all_fields.has_key(f):
                all_fields[f] = None
                n += 1
    return all_fields


def read_dataset(filename, all_fields):
    #all_fields = get_combined_fields(filenames)
    # Inefficient... but it'll do
    data = []

    with open(filename) as f:
        r = csv.reader(f)
        line = r.next()
        fields = [map_field_name(fn) for fn in line]
        #print fields

        for line in r:
            d = all_fields.copy()
            for f, v in itertools.izip(fields, line):
                d[f] = v
            data.append(d)

    return data

def read_all_datasets(filenames):
    data = []
    all_fields = get_combined_fields(filenames)
    for f in filenames:
        d = read_dataset(f, all_fields)
        data.extend(d)
        print f, len(d)

    # Sanity check
    for d in data:
        assert(data[0].keys() == d.keys())

    return data




################################################################################
# Postcode geolocation
################################################################################

def normalise_postcode(pc):
    pcn = pc.translate(None, string.whitespace).upper()
    # For some reason a few postcodes in the NHS files have extra characters
    pcn = pcn.replace('\xc2\xa0', '')
    return pcn

def postcode_lat_long_map():
    pcmap = {}

    with open(pcfile) as f:
        for r in csv.reader(f, delimiter=',', quotechar='"'):
            pcmap[normalise_postcode(r[0])] = (r[1], r[2])
    return pcmap

def append_lat_long(data, pcmap):
    failures = []
    n = 0
    for d in data:
        n += 1
        pc = normalise_postcode(d['post code'])

        try:
            latitude, longitude = pcmap[pc]
        except KeyError:
            err = (n, d['post code'], pc)
            print 'Lookup failed: row:%d input:%s normalised:%s' % err
            failures.append(err)
            latitude, longitude = None, None

        d['latitude'] = latitude
        d['longitude'] = longitude

    return data, failures


def write_data_csv(filename, datadict):
    fields = datadict[0].keys()
    # The header line also needs to be a dict
    header = collections.OrderedDict(itertools.izip(fields, fields))
    with open(filename, 'w') as csvf:
        w = csv.DictWriter(csvf, fields)
        w.writerow(header)
        w.writerows(datadict)

pcmap = postcode_lat_long_map()
data = read_all_datasets(files)
datall, failures = append_lat_long(data, pcmap)
write_data_csv(outputfile, datall)

