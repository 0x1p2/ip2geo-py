import os
import sys
import urllib.request
from urllib.error import HTTPError
import json
import argparse
import configparser

class Lookup:
    def __init__(self, args):
        self.url = args.url
        self.verbose = args.verbose
        self.FILE = args.FILE

        self.cc = {} # Holds a KEY:VALUE for COUNTRY_CODE:AMOUNT. Amount will be the number of discovered attempts.
        self.reg = { "EU":0, "NA":0, "SA":0, "AF":0, "ASIA":0, "AUS":0, "AQ":0, "UNK":0 }
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
        self.asia_codes = [
                "AF", "AM", "AZ", "BH", "BD", "BT", "BN", "KH", "CN",
                "CX", "CC", "IO", "GE", "HK", "IN", "ID", "IR", "IQ",
                "IL", "JP", "JO", "KZ", "KP", "KR", "KW", "KG", "LA",
                "LB", "MO", "MY", "MV", "MN", "MM", "NP", "OM", "PK",
                "PH", "QA", "SA", "SG", "LK", "SY", "TW", "TJ", "TH",
                "TR", "TM", "AE", "UZ", "VN", "YE", "PS" ]
        self.aus_codes = [
                "AS", "AU", "NZ", "CK", "FJ", "PF", "GU", "KI", "MP",
                "MH", "FM", "UM", "NR", "NC", "NZ", "NU", "NF", "PW",
                "PG", "MP", "SB", "TK", "TO", "TV", "VU", "UM", "WF",
                "WS", "TL" ]
        self.aq_codes = [ "AQ" ]


    def conf_read(self):
        ''' Loads the configuration file if one is discovered. This is implemented 
        because I use a local database instead of the freegeoip.net so I can make 
        frequent queries for testing. '''
        if os.path.exists('config.ini'):
            print("Loading configuration file...")
            config = configparser.ConfigParser()
            config.read('config.ini')
            return config
        else:
            return 0

    def set_host(self):
        if not self.url:
            if not os.path.exists("config.ini"):
                self.host = "http://freegeoip.net/"
            else:
                config = self.conf_read()
                self.host = config['URL']['host_db']
        else:
            self.host = self.url    # Add a check to see if it is availible, if not default to localhost.
        print("Using: [ %s ]" % self.host)


    def set_list(self):
        if not os.path.exists(self.FILE):
            print("No file %s found." % self.FILE)
            sys.exit()            
        else:
            with open(self.FILE) as fd:
                self.IPs = fd.readlines()


    def query(self):
        count = 0
        print("Starting query...")
        for IP in self.IPs:
            count += 1
            print("[%d] [ %s ]" % (count, IP.strip()))
            url = self.host + "json/" + IP.strip()
            try:
                sent = urllib.request.urlopen(url)
                if sent.getcode() == 404 or sent.getcode() == 503 or sent.getcode() == 403:
                    print("%s is not availible, use a different resource/db" % self.host)
                    raise HTTPError
                else:
                    text = sent.read()
                    data = text.decode()
                    info = json.loads(data)
                    self.parse(info)
            except HTTPError as err:
                print("  [ ERROR ]  IO Error: [Code: %s, %s]" % (err.errno, err.strerror))
                break


    def parse(self, info):
        code = info['country_code']
        if code == "":
            code = "UNK"
        if code in self.cc:
            self.cc[code] += 1
        else:
            self.cc[code] = 1

        if code in self.eu_codes:
            self.reg['EU'] += 1
        elif code in self.na_codes:
            self.reg['NA'] += 1
        elif code in self.sa_codes:
            self.reg['SA'] += 1
        elif code in self.af_codes:
            self.reg['AF'] += 1
        elif code in self.asia_codes:
            self.reg['ASIA'] += 1
        elif code in self.aus_codes:
            self.reg['AUS'] += 1
        elif code in self.aq_codes:
            self.reg['AQ'] += 1
        else:
            self.reg['UNK'] += 1


    def printf(self):
        print("-" * 15)
        for key, value in self.reg.items():     # Could be changed to self.cc
            print("{:>5} | {:<5}".format(key, value))


    def start(self):
        self.set_host()
        self.set_list()
        self.query()
        self.printf()




options = argparse.ArgumentParser(description="A tool that takes in the input of an IP and returns the GeoLocation data associated with it.")
group = options.add_mutually_exclusive_group()
group.add_argument('-q', '--quiet', help="no output except region amount.",
        action='store_false', dest="verbose")
group.add_argument('-v', '--verbose', help="set verbose output [default]",
        action='store_true', dest="verbose")
options.add_argument('-u', '--url', help="alternate url to use as a db",
        default=False)
options.add_argument('FILE', help="file to parse.")
args = options.parse_args()

my_search = Lookup(args)
my_search.start()

