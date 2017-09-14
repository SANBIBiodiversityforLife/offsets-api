import requests

def get_area_info(polygon):
    url = 'http://bgismaps.sanbi.org/arcgis/rest/services/2012VegMap/MapServer/identify'
    coordinates = polygon.tuple
    coordinates_str = str({"rings":  coordinates})\
        .replace('(', '[')\
        .replace(')', ']')\
        .replace('],],]}', ']]}')\
        .replace(']],]}', ']]}')\
        .replace(': [[[[', ': [[[')
    params = {
        'geometry': coordinates_str,
        'geometryType': 'esriGeometryPolygon',
        'tolerance': 0,
        'mapExtent': '-104,35.6,-94.32,41',
        'imageDisplay': '600,550,96',
        'returnGeometry': False,
        'returnZ': False,
        'returnM': False,
        'f': 'json'
    }
    response = requests.post(url, data=params)
    results = response.json()
    info = {}

    try:
        for item in results['results']:
            info[item['value']] = {
                "area": 5,
                "status": "to be retrieved",
                "type": item['layerName']
            }
    except:
        import pdb; pdb.set_trace()
    return info
