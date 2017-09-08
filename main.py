import time
from datetime import datetime
import csv
import contextlib
from selenium import webdriver
from PIL import Image

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

# check NIP validity
def validateNIP(nip):
    if nip == "":
        return False

    if len(nip) != 10:
        return False

    if not is_number(nip):
        return False

    checksum = 6 * int(nip[0]) + 5 * int(nip[1]) + 7 * int(nip[2]) + 2 * int(nip[3]) + 3 * int(nip[4]) + 4 * int(nip[5]) + 5 * int(nip[6]) + 6 * int(nip[7]) + 7 * int(nip[8])
    checksum = checksum % 11

    if int(nip[9]) != checksum:
        return False

    return True


nip_list = []
with open('nip_list.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=';', quotechar='|')
    for row in reader:
        nip_list.append(row[0])



with contextlib.closing(webdriver.PhantomJS()) as d:
    d.implicitly_wait(10)

    with open('nip_result.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["LP", "NIP", "STATUS", "OPIS", "CZAS SPRAWDZENIA"])

        lp = 1
        for nip in nip_list:
            print "Podmiot " + nip + ":"
            d.get("http://www.finanse.mf.gov.pl/web/wp/pp/sprawdzanie-statusu-podmiotu-w-vat")

            # fill form
            input = d.find_element_by_id('b-7')
            input.send_keys("", nip)

            # click & wait
            d.find_element_by_id('b-8').click()
            time.sleep(4)

            # get timestamp
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            timestamp_short = datetime.now().strftime('%Y%m%d')

            # screenshot
            screenshot_name = nip+'_'+timestamp_short+'.png'
            d.save_screenshot(screenshot_name)

            # validate nip & read result if ok
            if validateNIP(nip):
                result = d.find_element_by_id('caption2_b-3').text.splitlines()[0].split("NIP ")[1]
            else:
                result = "niepoprawny format NIP"

            if "czynny" in result:
                status = "OK"
            else:
                status = "PROBLEM"

            print result
            writer.writerow([lp, nip, status, result, timestamp])
            lp = lp + 1
