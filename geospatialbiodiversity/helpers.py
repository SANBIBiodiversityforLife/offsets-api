from geospatialbiodiversity import models
from core import services, models as core_models
from django.contrib.gis.geos import GEOSGeometry, WKTWriter
from os.path import join
import json
from datetime import datetime, date
import csv

# Run using python manage.py shell, from geospatialbiodiversity import helpers

def load_input():
    url = join('..', 'offsets-data-sources', 'input')

    # Developments
    with open(join(url, 'development_sites.geojson')) as file_obj:
        dev_geojson_data = file_obj.read().replace('\n', '')
    dev_json_data = json.loads(dev_geojson_data)

    # Used to convert input geoms into 2D
    wkt_w = WKTWriter()
    wkt_w.outdim = 2

    devs = {}
    for item in dev_json_data['features']:
        polygon = GEOSGeometry(json.dumps(item['geometry']))

        # Make it 2D
        temp = wkt_w.write(polygon)
        polygon = GEOSGeometry(temp)

        devs[item['properties']['Uniq_ID']] = {'polygon': polygon}

    # Offsets
    with open(join(url, 'offsets_receiving_areas.geojson')) as file_obj:
        offset_geojson_data = file_obj.read().replace('\n', '')
    offsets_json_data = json.loads(offset_geojson_data)

    offsets = {}
    for item in offsets_json_data['features']:
        polygon = GEOSGeometry(json.dumps(item['geometry']))

        # Make it 2D
        temp = wkt_w.write(polygon)
        polygon = GEOSGeometry(temp)

        offsets[item['properties']['Uniq_ID']] = {'polygon': polygon }
        if 'PROVINCE' in item['properties']:
            offsets[item['properties']['Uniq_ID']]['province'] = item['properties']['PROVINCE']

    # Used for conversion/mapping
    permit_objs = {}
    for permit in core_models.Permit.objects.all():
        permit_objs[permit.name] = permit
    row_types_mapping = {
        'Agriculture': core_models.Development.AGRICULTURE,
        'Business': core_models.Development.BUSINESS,
        'Commercial': core_models.Development.COMMERCIAL,
        'Government': core_models.Development.GOVERNMENT,
        'Government purposes': core_models.Development.GOVERNMENT_PURPOSES,
        'Industrial': core_models.Development.INDUSTRIAL,
        'Mining': core_models.Development.MINING,
        'Multi-use (Public, Residential, Businees and commercial)': core_models.Development.MULTI_USE,
        'Recreational': core_models.Development.RECREATIONAL,
        'Residential': core_models.Development.RESIDENTIAL,
        'Transport': core_models.Development.TRANSPORT,
        'Unknown': core_models.Development.UNKNOWN
    }
    duration_mapping = {
        'perpetuity': core_models.Offset.PERPETUITY,
        'unspecified': core_models.Offset.UNSPECIFIED,
        'unknown': core_models.Offset.UNKNOWN,
        '< 20 yrs': core_models.Offset.LOWER,
        '20+': core_models.Offset.MIDRANGE,
        '50+ yrs': core_models.Offset.LONG
    }
    implementation_times = {}
    for i_time in core_models.OffsetImplementationTime.objects.all():
        implementation_times[i_time.name] = i_time

    with open(join(url, 'offsets_spreadsheet.csv')) as file_obj:
        reader = csv.DictReader(file_obj)
        for row in reader:
            # ,bo_id,province,year,type,offset_trigger_pa,offset_trigger_ps,offset_trigger_cba,offset_trigger_esa,offset_trigger_nfepa,offset_trigger_ecosys,offset_trigger_species,offset_trigger_specialhabitats,offset_trigger_focuspas,offset_trigger_other,offset_type_hectares,offset_type_research,offset_type_restoration,offset_type_financial,offset_type_unknown,ecosys_impacted,ecosys_offset,ecosys_equiv,ecosys_diff_etshigher,ecosys_diff_etslower,offset_details_conditions,offset_access_agreement,clear_bio_objectives,management_clear,acquisition_required,no_hectares_low,no_hectares_high,management_specified,financial_provision_clear,financial_provision,implementation_time_nature,duration
            if 'year' in row:
                uid = row['unique_id']

                if uid not in offsets:
                    print('no offsets uid for ' + row['unique_id'])
                    continue

                offset = offsets[uid]
                dev = devs[uid]

                #import pdb; pdb.set_trace()
                offset_info = services.get_area_info(offset['polygon'])

                dev_info = services.get_area_info(dev['polygon'])

                #import pdb; pdb.set_trace()

                permits = []
                if row['permit_eia']:
                    permits.append(permit_objs['Environmental Impact Assessment'])
                if row['permit_daff']:
                    permits.append(permit_objs['Department of Agriculture, Forestry and Fisheries Permit'])
                if row['permit_wula']:
                    permits.append(permit_objs['Water Use License Application'])
                if row['permit_dmr']:
                    permits.append(permit_objs['Department of Mineral Resources'])


                new_dev = core_models.Development(year=row['year'], footprint=dev['polygon'][0],
                                                  info=dev_info, type=row_types_mapping[row['type']])

                try:
                    new_dev.save()
                except:
                    continue
                new_dev.permits = permits
                new_dev.save()
                print('created dev ' + row['year'])

                new_offset = core_models.Offset(development=new_dev, polygon=offset['polygon'][0],
                                                type=core_models.Offset.HECTARES, info=offset_info)
                new_offset.duration = duration_mapping[row['duration'].lower()]
                new_offset.save()

                implementations = []
                if 'implement_before' in row and row['implement_before']:
                    implementations.append(implementation_times['Before development'])
                if 'implement_during' in row and row['implement_during']:
                    implementations.append(implementation_times['During development'])
                if 'implement_6m' in row and row['implement_6m']:
                    implementations.append(implementation_times['After development - 6 months'])
                if 'implement_12m' in row and row['implement_12m']:
                    implementations.append(implementation_times['After development - 12 months'])
                if 'implement_24m' in row and row['implement_24m']:
                    implementations.append(implementation_times['After development - 24 months'])
                if 'implement_longer' in row and row['implement_longer']:
                    implementations.append(implementation_times['After development - more than 24 months'])

                new_offset.implementation_times = implementations
                new_offset.save()
                print('created offset for dev ' + str(new_dev.pk))


    import pdb; pdb.set_trace()

def load_provinces():
    url = join('..', 'offsets-data-sources', 'sa-provinces.geojson')

    with open(url) as file_obj:
        geojson_data = file_obj.read().replace('\n', '')

    print('finished reading file')
    json_data = json.loads(geojson_data)

    for item in json_data['features']:
        polygon = GEOSGeometry(json.dumps(item['geometry']))
        province = models.ProtectedArea(polygon=polygon, type=models.ProtectedArea.PROVINCE,
                                              name=item['properties']['PROVINCE'])
        province.save()
        print('saved ' + item['properties']['PROVINCE'])

    print('done all')

def load_protected_areas():
    url = join('..', 'offsets-data-sources', 'protected_areas_ramsar_sites.geojson')

    with open(url) as file_obj:
        geojson_data = file_obj.read().replace('\n', '')

    print('finished reading file')
    json_data = json.loads(geojson_data)

    print('starting loop')
    for item in json_data['features']:
        try:
            polygon = GEOSGeometry(json.dumps(item['geometry']))
            date = datetime.strptime(item['properties']['DESIGNATIO'], '%d %B %Y')
            protected_area = models.ProtectedArea(polygon=polygon, date=date.date(), type=models.ProtectedArea.RAMSAR,
                                                  identifier=item['properties']['SITE_NO'], name=item['properties']['NAME'])
            protected_area.save()
            print('saved ' + protected_area.name)
        except:
            import pdb; pdb.set_trace()

    print('done all')

    import pdb; pdb.set_trace()