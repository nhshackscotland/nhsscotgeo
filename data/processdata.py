import itertools
import pickle
import csv
import collections
import string
import re

files = collections.OrderedDict([
        ('exported/All_Hospitals.csv', 'HOS'),
        ('MIU_AAE/AAE.csv', 'AAE'),
        ('MIU_AAE/MIU.csv', 'MIU'),
        ('exported/All_GPs.csv', 'GP'),
        ('exported/All_pharmacies.csv', 'PHA'),
        ('exported/All_dentists.csv', 'DEN'),
        ('exported/All_opticians.csv', 'OPT'),
        ('exported/Sexual Health.csv', 'SEX'),
        ('exported/Travel Clinics.csv', 'TC'),
        ])
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
    Also lowercase and replace spaces
    """
    fn = fieldname.lower().replace(' ', '_')
    if fn == 'dataset_code_code':
        return 'dataset_code'
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

def read_all_datasets(files_types):
    data = []
    typecodes = []
    all_fields = get_combined_fields(files_types.keys())
    for (f, t) in files_types.iteritems():
        d = read_dataset(f, all_fields)
        data.extend(d)
        typecodes.extend([t] * len(d))
        print f, t, len(d)

    # Sanity check
    for d in data:
        assert(data[0].keys() == d.keys())

    return data, typecodes




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
        pc = normalise_postcode(d['post_code'])

        try:
            latitude, longitude = pcmap[pc]
        except KeyError:
            err = (n, d['post_code'], pc)
            print 'Lookup failed: row:%d input:%s normalised:%s' % err
            failures.append(err)
            latitude, longitude = None, None

        d['latitude'] = latitude
        d['longitude'] = longitude

    return data, failures


################################################################################
# Post processing
################################################################################
def opening_times(d):
    def not_empty(s):
        return s and len(s.strip()) > 0

    def get_time(s):
        try:
            return re.search('(\d\d\:\d\d):\d\d', s).group(1)
        except:
            return None

    days = [
        'monday',
        'tuesday',
        'wednesday',
        'thursday',
        'friday',
        'saturday',
        'sunday']
    periods = [1, 2, 3]

    openstrs = []
    for day in days:
        daytimes = []
        for per in periods:
            op = get_time(d['%s_open_%d' % (day, per)])
            cl = get_time(d['%s_close_%d' % (day, per)])
            if op and cl:
                daytimes.append('%s-%s' %(op, cl))
        if daytimes:
            openstrs.append(day[0].capitalize() + day[1:] + ' ' + ' '.join(daytimes))

    rota = d['rota_opening_hours']
    if not_empty(rota):
        openstrs.append(rota)

    hol = d['public_holiday_opening_hours']
    if not_empty(hol):
        openstrs.append(hol)

    openstr = '\n'.join(openstrs)
    return openstr

def qualifying_comment(typecode):
    if typecode == 'GP':
        return 'Use SBAR tool when conducting a clinical conversation. Expect a call back within 10 minutes. Patient must be stable.'
    if typecode == 'MIU':
        return 'Patient must be stable.'
    if typecode == 'AAE':
        return 'Pre-alert for sepsis.'
    return ''

def get_cleaned_fields(data, typecodes):
    namefields = ['name_of_hospital',
                  'name_of_aae',
                  'name_of_miu',
                  'practice_name',
                  'name_of_pharmacy',
                  'name_of_clinic'
                  ]
    phonefields = ['reception/switchboard_phone_number',
                   'reception_phone_number',
                   'pharmacy_public_phone_number',
                   'clinic_public_phone_number',
                   'alt_phone_number_1',
                   'alt_phone_number_2'
                   ]
    addressfields = ['address_line_1',
                     'address_line_2',
                     'address_line_3',
                     'address_line_4',
                     'post_town',
                     'post_code'
                     ]

    failures = []

    for n in xrange(len(data)):
        d = data[n]

        typecode = typecodes[n]

        name = None
        for f in namefields:
            if d[f]:
                name = d[f]
                break

        phone = None
        for f in phonefields:
            if d[f]:
                phone = d[f]
                break

        address = None
        for f in addressfields:
            if d[f]:
                s = d[f].strip()
                if s:
                    if address:
                        address += '\n' + s
                    else:
                        address = s


        d['demo_id'] = n + 1
        d['type_code'] = typecode
        d['location_name'] = name
        d['phone'] = phone
        d['address'] = address
        d['opening_times'] = opening_times(d)
        d['qualifying_comment'] = qualifying_comment(typecode)

    return data

def delete_missing_location(data):
    for i in xrange(len(data) - 1, -1, -1):
        if not data[i]['latitude'] or  not data[i]['longitude']:
            del data[i]
    return data


################################################################################
# Final output
################################################################################

def write_data_csv(filename, datadict):
    fields = datadict[0].keys()
    # The header line also needs to be a dict
    header = collections.OrderedDict(itertools.izip(fields, fields))
    with open(filename, 'w') as csvf:
        w = csv.DictWriter(csvf, fields)
        w.writerow(header)
        w.writerows(datadict)


pcmap = postcode_lat_long_map()
all_fields = get_combined_fields(files)
data, typecodes = read_all_datasets(files)
data, failures = append_lat_long(data, pcmap)
data = get_cleaned_fields(data, typecodes)
#data = delete_missing_location(data)
write_data_csv(outputfile, data)


#with open('processed.pkl','w') as f:
#    pickle.dump({'all_fields':all_fields, 'data':data, 'pcmap':pcmap, 'failures':failures}, f)
