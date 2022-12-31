import requests
import json
from datetime import datetime

response = requests.get("https://www.nordpoolgroup.com/api/marketdata/page/10")

data = response.json()

myJsonData = {}

### FUNCTION TO CONVERT MWh TO KWh AND PRISE ###
def price_converter(MWh):
        KWh = float(MWh.replace(",",".")) / 1000 # convert price for MWh to KWh + danish notation
        static_currency = 7.5 # convert Euro to DKK
        converted_price_pr_KWh = round((KWh * static_currency)*1.25 + 0.06, 2) # add tax and round
        return str(converted_price_pr_KWh)


if __name__ == "__main__":
    for i in range(0, 24):
        # Get timestamp from python dictionary
        startTime = data.get('data').get("Rows")[i].get("StartTime")
        endTime = data.get('data').get("Rows")[i].get("EndTime")

        # Get name (DK1) from python dictionary
        name = data.get('data').get("Rows")[i].get("Columns")[6].get("Name")

        # Get prise from python dictionary
        value = data.get('data').get("Rows")[i].get("Columns")[6].get("Value")
        # convert prise 
        value = price_converter(value)

        print(f'Pris for {name} i tidsrummet {startTime}-{endTime}: {value}')

        # Formate timestamt
        startDateTime = datetime.strptime(startTime, "%Y-%m-%dT%H:%M:%S")
        endDateTime = datetime.strptime(endTime, "%Y-%m-%dT%H:%M:%S")

        _data = {}
        _data["Date"] = str(datetime.date(startDateTime))
        _data["StartTime"] = str(datetime.time(startDateTime))
        _data["EndTime"] = str(datetime.time(endDateTime))
        _data["pris"] = value
        myJsonData[i] = _data

    # Serialize python dict to JSON
    myJsonData = json.dumps(myJsonData, indent = 4)
                    