import urllib.request
import json
cc = {}

# http://www.europeancuisines.com/Europe-European-Two-Letter-Country-Code-Abbreviations
eu_codes = [ 
        "AL", "AD", "AT", "BY", "BE", "BA", "BG", "HR", "CY",
        "CZ", "DK", "EE", "FO", "FI", "FR", "DE", "GI", "GR", 
        "HU", "IS", "IE", "IT", "LV", "LI", "IT", "LU", "MK",
        "MT", "MD", "MC", "NL", "NO", "PL", "PT", "RO", "RU",
        "SM", "RS", "SK", "SI", "ES", "SE", "CH", "UA", "GB",
        "VA", "RS", "IM", "RS", "ME" ]
na_codes = [
        "AI", "AG", "AW", "BS", "BB", "BZ", "BM", "VG", "CA",
        "KY", "CR", "CU", "CW", "DM", "DO", "SV", "GL", "GD", 
        "GP", "GT", "HT", "HN", "JM", "MQ", "MX", "PM", "MS",
        "CW", "KN", "NI", "PA", "PR", "LC", "VC", "TT", "TC",
        "VI", "US", "SX", "BQ", "SA", "SE" ]
sa_codes = [
        "AR", "BO", "BR", "CL", "CO", "EC", "FK", "GF", "GY",
        "PY", "PE", "SR", "UY", "VE" ]
af_codes = [
        "DZ", "AO", "SH", "BJ", "BW", "BF", "BI", "CM", "CV",
        "CF", "TD", "KM", "CG", "DJ", "EG", "GQ", "ER", "ET",
        "GA", "GM", "GH", "GW", "GN", "CI", "KE", "LS", "LR",
        "LY", "MG", "MW", "ML", "MR", "MU", "YT", "MA", "MZ",
        "NA", "NE", "NG", "ST", "RE", "RW", "ST", "SN", "SC",
        "SL", "SO", "ZA", "SH", "SD", "SZ", "TZ", "TG", "TN",
        "UG", "CD", "ZM", "TZ", "ZW", "SS", "CD" ]
as_codes = [
        "AF", "AM", "AZ", "BH", "BD", "BT", "BN", "KH", "CN",
        "CX", "CC", "IO", "GE", "HK", "IN", "ID", "IR", "IQ",
        "IL", "JP", "JO", "KZ", "KP", "KR", "KW", "KG", "LA",
        "LB", "MO", "MY", "MV", "MN", "MM", "NP", "OM", "PK",
        "PH", "QA", "SA", "SG", "LK", "SY", "TW", "TJ", "TH",
        "TR", "TM", "AE", "UZ", "VN", "YE", "PS" ]
au_codes = [
        "AS", "AU", "NZ", "CK", "FJ", "PF", "GU", "KI", "MP",
        "MH", "FM", "UM", "NR", "NC", "NZ", "NU", "NF", "PW",
        "PG", "MP", "SB", "TK", "TO", "TV", "VU", "UM", "WF",
        "WS", "TL" ]
aq_codes = [ "AQ" ]

eu_cntr = 0
na_cntr = 0
sa_cntr = 0
af_cntr = 0
as_cntr = 0
au_cntr = 0
aq_cntr = 0
unk_cntr = 0

with open('attackers.txt', 'r') as fd:
    file_data = fd.readlines()

for IP in file_data:
    url = "http://localhost/json/" + IP
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
