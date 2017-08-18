from geospatialbiodiversity import models
from django.contrib.gis.geos import GEOSGeometry
from os.path import join
import json
from datetime import datetime, date

# Run using python manage.py shell, from geospatialbiodiversity import helpers

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