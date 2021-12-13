from math import sin, cos, sqrt, atan2, radians

# approximate radius of earth in km
def get_distance(lat1,lon1,lat2,lon2):

    R = 6373.0
    print(lat1,lon1,lat2,lon2)
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c



    print("Result:", distance)
    print("Should be:", 278.546, "km")
    return distance


def isvalid_latlong(lat, lng):
    if lat >= -90 and lat <= 90 and lng >= -180 and lng <= 180:
        return True
    else:
        return False


# R = 6373.0
# lat1 = radians(52.2296756)
# lon1 = radians(21.0122287)
# lat2 = radians(52.406374)
# lon2 = radians(16.9251681)
# print(lat1)
# print(lon1)
# print(lat2)
# print(lon2)
# dlon = lon2 - lon1
# dlat = lat2 - lat1
#
# a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
# c = 2 * atan2(sqrt(a), sqrt(1 - a))
#
# distance = R * c
#
#
#
# print("Result:", distance)
# print("Should be:", 278.546, "km")