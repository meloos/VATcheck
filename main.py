from MFDriver import MFDriver
from Validator import Validator

from datetime import datetime
import csv

nip_dict = {}

nip_csv_in = "nip_list.csv"
nip_csv_out = "nip_result.csv"

def check_nip(nip):
    # initialize webdriver and validator
    mf = MFDriver()
    v = Validator()


    # if nip is valid
    if v.validate(nip):
        # check nip
        mf.check(nip)

        # get timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        timestamp_short = datetime.now().strftime('%Y%m%d')

        # screenshot
        screenshot_name = nip+'_'+timestamp_short+'.png'
        mf.screenshot(screenshot_name)

        # get message
        message = mf.message()

    # nip is nod valid
    else:
        message =  "niepoprawny format NIP"

    if message:
        if "czynny" in message:
            status = "OK"
        else:
            status = "PROBLEM"
    else:
        status = "CHECK PROBLEM"

    # fill result dictionary
    nip_dict[nip]["message"] = message
    nip_dict[nip]["timestamp"] = timestamp
    nip_dict[nip]["status"] = status

    # close webdriver
    mf.exit()


# get nips from csv into dictionary
with open(nip_csv_in, 'rb') as csvfile:
     reader = csv.reader(csvfile, delimiter=';', quotechar='|')
     for row in reader:
         nip_dict[row[0]] = {}

# check nips
for nip, data in nip_dict.iteritems():
    print nip
    check_nip(nip)

# create csv
with open(nip_csv_out, 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(["NIP", "STATUS", "OPIS", "CZAS SPRAWDZENIA"])
    for nip, data in nip_dict.iteritems():
        writer.writerow([nip, data["status"], data["message"], data["timestamp"]])

