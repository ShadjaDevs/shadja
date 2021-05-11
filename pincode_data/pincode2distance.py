'''
On the whole, this script generates a mapping from:
    pincode -> list of pincodes which are nearby for N predefined radii buckets

Steps:
1. Query Google's geocoding API for details of every pincode in India.
2. Filter it to remove faulty results (only pincode bounding boxes retained)
Optional: Check `plot_pincode_bounds.html` to take this data and visually verify on the map
3. List all pairs of pincodes that are close to each other
4. Bucket them based on different limits (5,10,25,50 etc.)
'''

from collections import defaultdict
import json
import itertools

import googlemaps
import haversine

# The maximum distance between two pincodes
DIST_LIMIT = 50

# Latitude/Longitude limit for coarse filtering
# 1 degree is approx. 100 km in India
LAT_LIMIT = 1
LNG_LIMIT = 1

gmaps = googlemaps.Client(key=YOUR_GOOGLE_MAPS_API_KEY_HERE)

with open('all_india_pincodes.json') as f:
    pincodes = json.load(f)['pincodes']

geocode_data = {}

for i,pincode in enumerate(pincodes):
    # Geocoding an address
    print('Getting geocode for ', i, pincode)

    addrs = gmaps.geocode(
        str(pincode),
        region='in',
        components={
            'postal_code': pincode,
            'country': 'IN'
        }
    )
    geocode_data[pincode] = addrs

    # Filter the data to remove faulty/empty entries
    for addr in addrs:
        assert 'geometry' in addr, 'No geometry {0}'.format(pincode)
        assert 'types' in addr, 'No types {0}'.format(pincode)

        # If location_type is ROOFTOP or something else, it means the result was
        # the exact location of the post office or some other building.
        # We are not interested in that. We are looking for the approximate
        # region this pincode covers.
        if not addr['geometry']['location_type']=='APPROXIMATE':
            continue

        # Did not see any other type but wanted to make sure my assumption is correct.
        # A very lazy way of doing it
        assert len(addr['types'])==1, 'Length of types unexpected {0}'.format(pincode)

        # As expected, because our query itself is a pincode :)
        # This confirms that google understood our 'address' which was just a 6 digit
        # number to be indeed a pincode
        assert addr['types'][0]=='postal_code', 'Not a postal code {0}'.format(pincode)

        # There may be multiple results returned in 'addrs', but only one should be valid
        assert pincode not in geocode_data, 'Data already exists {0}'.format(pincode)

        # If everything looks good, add geometry.
        # This contains location (center), viewport (bounding box) etc.
        geocode_data[pincode] = addr['geometry']

# First step of filtering: This is more efficient that doing haversine distance calculation
# for all pair of points which is (O(n^2)) operation.
def near(d):
    '''Given a pair of pincodes as a tuple d (a,b), returns True only if
    the locations of those pincodes are within the bounding box of lat and long
                           -LAT_LIMIT      0     LAT_LIMIT
                                    -------------LNG_LIMIT
                                    |           |
                                    |           |
                                    |     p     |
                                    |           |
                                    |___________|-LNG_LIMIT
    
    '''
    a, b = d
    center_a = (geocode_data[a]['location']['lat'],
        geocode_data[a]['location']['lng'])
    center_b = (geocode_data[b]['location']['lat'],
        geocode_data[b]['location']['lng'])

    # print(geodesic(center_a, center_b).km)
    return ((abs(center_a[0]-center_b[0])<LAT_LIMIT) and
        (abs(center_a[1]-center_b[1])<LNG_LIMIT))

# Get all possible pairs of pincode and initial filtering based on lat, long
pairs = list(filter(near,
    itertools.combinations(geocode_data.keys(), 2)))

def calc_distance(a,b):
    '''Return the distance (in km) between two points on the planet accounting
    for the speherical nature'''
    center_a = (geocode_data[a]['location']['lat'],
        geocode_data[a]['location']['lng'])
    center_b = (geocode_data[b]['location']['lat'],
        geocode_data[b]['location']['lng'])

    return haversine.haversine(center_a, center_b)

# Data structure:
# graded_data: pincode -> radii_dict
# radii_dict: radius -> list of pincodes
graded_data = defaultdict(lambda: defaultdict(list))

# Calculate the exact distance between the points and
# place them in different buckets
for pair in pairs:
    a,b = pair
    distance = calc_distance(a,b)
    print('Distance between {0} and {1} is {2}'.format(a,b,distance))

    if distance > 50:
        # Too far
        pass
    elif distance > 25:
        graded_data[a][50].append(b)
        graded_data[b][50].append(a)
    elif distance > 10:
        graded_data[a][25].append(b)
        graded_data[b][25].append(a)
    elif distance > 5:
        graded_data[a][10].append(b)
        graded_data[b][10].append(a)
    else:
        graded_data[a][5].append(b)
        graded_data[b][5].append(a)

with open('nearby_pincodes.json', 'w') as f:
    json.dump(graded_data, f)
