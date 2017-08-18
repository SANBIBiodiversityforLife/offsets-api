import requests

def get_area_info(polygon):
    url = 'http://bgismaps.sanbi.org/arcgis/rest/services/2012VegMap/MapServer/identify'
    coordinates = polygon.tuple
    params = {
        'geometry': str({"rings":  coordinates}).replace('(', '[').replace(')', ']'),
        'geometryType': 'esriGeometryPolygon',
        'tolerance': 0,
        'mapExtent': '-104,35.6,-94.32,41',
        'imageDisplay': '600,550,96',
        'returnGeometry': False,
        'returnZ': False,
        'returnM': False,
        'f': 'json'
    }
    response = requests.get(url, params=params)
    results = response.json()
    for item in results:
        area_info = item['attributes']
        attributes.append(area_info)

    return attributes
