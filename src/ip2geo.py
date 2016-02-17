import os
import urllib.request
import json
import argparse
from configparser import ConfigParser

def conf_read():
    ''' Loads the configuration file if one is discovered. This is implemented 
    because I use a local database instead of the freegeoip.net so I can make 
    frequent queries for testing. '''
    if os.path.exists('config.ini'):
        print("Loading configuration file...")
        config = ConfigParser()
        config.read('config.ini')
        return config
    else:
        return 0

class Lookup():

    def __init__(self, args):
        self.host = args.url
        self.verbose = args.verbose

        self.cc = {} # Holds a KEY:VALUE for COUNTRY_CODE:AMOUNT. Amount will be the number of discovered attempts.
        # Country codes obtained from: http://www.countrycallingcodes.com/iso-country-codes/
        self.eu_codes = [ 
                "AL", "AD", "AT", "BY", "BE", "BA", "BG", "HR", "CY",
                "CZ", "DK", "EE", "FO", "FI", "FR", "DE", "GI", "GR", 
                "HU", "IS", "IE", "IT", "LV", "LI", "IT", "LU", "MK",
                "MT", "MD", "MC", "NL", "NO", "PL", "PT", "RO", "RU",
                "SM", "RS", "SK", "SI", "ES", "SE", "CH", "UA", "GB",
                "VA", "RS", "IM", "RS", "ME" ]
        self.na_codes = [
                "AI", "AG", "AW", "BS", "BB", "BZ", "BM", "VG", "CA",
                "KY", "CR", "CU", "CW", "DM", "DO", "SV", "GL", "GD", 
                "GP", "GT", "HT", "HN", "JM", "MQ", "MX", "PM", "MS",
                "CW", "KN", "NI", "PA", "PR", "LC", "VC", "TT", "TC",
                "VI", "US", "SX", "BQ", "SA", "SE" ]
        self.sa_codes = [
                "AR", "BO", "BR", "CL", "CO", "EC", "FK", "GF", "GY",
                "PY", "PE", "SR", "UY", "VE" ]
        self.af_codes = [
                "DZ", "AO", "SH", "BJ", "BW", "BF", "BI", "CM", "CV",
                "CF", "TD", "KM", "CG", "DJ", "EG", "GQ", "ER", "ET",
                "GA", "GM", "GH", "GW", "GN", "CI", "KE", "LS", "LR",
                "LY", "MG", "MW", "ML", "MR", "MU", "YT", "MA", "MZ",
                "NA", "NE", "NG", "ST", "RE", "RW", "ST", "SN", "SC",
                "SL", "SO", "ZA", "SH", "SD", "SZ", "TZ", "TG", "TN",
                "UG", "CD", "ZM", "TZ", "ZW", "SS", "CD" ]
        self.as_codes = [
                "AF", "AM", "AZ", "BH", "BD", "BT", "BN", "KH", "CN",
                "CX", "CC", "IO", "GE", "HK", "IN", "ID", "IR", "IQ",
                "IL", "JP", "JO", "KZ", "KP", "KR", "KW", "KG", "LA",
                "LB", "MO", "MY", "MV", "MN", "MM", "NP", "OM", "PK",
                "PH", "QA", "SA", "SG", "LK", "SY", "TW", "TJ", "TH",
                "TR", "TM", "AE", "UZ", "VN", "YE", "PS" ]
        self.au_codes = [
                "AS", "AU", "NZ", "CK", "FJ", "PF", "GU", "KI", "MP",
                "MH", "FM", "UM", "NR", "NC", "NZ", "NU", "NF", "PW",
                "PG", "MP", "SB", "TK", "TO", "TV", "VU", "UM", "WF",
                "WS", "TL" ]
        self.aq_codes = [ "AQ" ]

        self.eu = 0
        self.na = 0
        self.sa = 0
        self.af = 0
        self.as = 0
        self.au = 0
        self.aq = 0
        self.unk  = 0

    def set_host(self):
        if not self.url:
            if not os.path.exists("config.ini"):
                self.host = "http://freegeoip.net/"
            else:
                config = conf_read()
                self.host = config['URL']['host_db']
        else:
            self.host 


options = argparse.ArgumentParser(description="A tool that takes in the input of an IP and returns the GeoLocation data associated with it.")
group = options.add_mutually_exclusive_group()
group.add_argument('-q', '--quiet', help="no output except region amount.",
        action='store_false', dest="verbose")
group.add_argument('-v', '--verbose', help="set verbose output [default]",
        action='store_true', dest="verbose")
options.add_argument('-u', '--url', help="alternate url to use as a db",
        default=False)
args = options.parse_args()

with open('attackers.txt', 'r') as fd:
    file_data = fd.readlines()

for IP in file_data:
    url = host + "json/" + IP
    response = urllib.request.urlopen(url).read()
    data = response.decode()
    response  = json.loads(data)
    code = response['country_code']
    if code == "":
        code = "UNK"

    if code in cc:
        cc[code] += 1
    else:
        cc[code] = 1

    #print("{:<15} {:<3} {:<6}".format(response['ip'], response['country_code'], response['region_code']))

#for KEY, PAIR in cc.items():
#    print("{:<3} {:<4}".format(KEY, PAIR))

    if code in eu_codes:
        eu_cntr += 1
    elif code in na_codes:
        na_cntr += 1
    elif code in sa_codes:
        na_cntr += 1
    elif code in af_codes:
        af_cntr += 1
    elif code in as_codes:
        as_cntr += 1
    elif code in au_codes:
        au_cntr += 1
    elif code in aq_codes:
        aq_cntr += 1
    else:
        unk_cntr += 1

print("EU: %d" % eu_cntr)
print("NA: %d" % na_cntr)
print("SA: %d" % sa_cntr)
print("AF: %d" % af_cntr)
print("AS: %d" % as_cntr)
print("AU: %d" % au_cntr)
print("AQ: %d" % aq_cntr)
print("UNKNOWN: %d" % unk_cntr)
