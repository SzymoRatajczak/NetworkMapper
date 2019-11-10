import pygeoip

def GetCountry(ip_address):
    print(pygeoip.GeoIP("geo.dat").country_name_by_addr(ip_address))

GetCountry('103.31.6.36')