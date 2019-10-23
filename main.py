import csv
import os
import requests

######################################################################################################################
# Configurations
######################################################################################################################

# Add funds into this file. The name should be same as in the FUND_DETAIL_FILE Scheme Name field.
# Each fund name should be present in a separate line
FUNDS_TO_MONITOR_FILE = "funds_to_monitor.txt"

# These fields should match the fields in the FUND_DETAIL_FILE
MUTUAL_FUND_FIELDS = [
    "Scheme Code",
    "ISIN Div Payout/ ISIN Growth",
    "ISIN Div Reinvestment",
    "Scheme Name",
    "Net Asset Value",
    "Date"
]

# Index value as per MUTUAL_FUND_FIELDS
SCHEME_NAME_INDEX = 3
NAV_INDEX = 4
DATE_INDEX = 5

# Percentage change in NAV for which we need to highlight
HIGHLIGHT_THRESHOLD = 3.0

FUND_DETAIL_URL = "https://www.amfiindia.com/spages/NAVAll.txt"
FUND_DETAIL_FILE = "mutual_funds.txt"

# File which stores details of monitored funds when last executed
PREVIOUS_TRACKED_DETAILS_FILE = "last_tracked_details.txt"


######################################################################################################################
#    F U N C T I O N S
######################################################################################################################

def GetFundListToMonitor(file_path):
    fundsToMonitor = []
    if (os.path.isfile(file_path)):
        f = open(file_path, 'r')
        fundsToMonitor = f.read().splitlines()
        f.close()
    else:
        print ("ERROR: List of funds to monitor not found! Please provide [ %s ]" % file_path)


    return fundsToMonitor

######################################################################################################################
# @name                                 : DownloadFundDetailsFile
#
# @description                          : Fetches the mutual funds' detail file from the given URL and
#                                         saves a local copy of it with the full path specified by file_path
#
# @param url                            : URL of mutual funds' details file
# @param file_path                      : Local file path to which the details have to be stored into
#
# @returns                              : Nothing
######################################################################################################################
def DownloadFundDetailsFile(url, file_path):
    # Remove existing file first
    if (os.path.isfile(file_path)):
        os.remove(file_path)

    # create HTTP response object
    r = requests.get(url)

    # send a HTTP request to the server and save
    # the HTTP response in a response object called r
    with open(file_path, 'wb') as f:
        # Saving received content as a png file in
        # binary format

        # write the contents of the response (r.content)
        # to a new file in binary mode.
        f.write(r.content)

    print ("Downloaded [ %s ] from %s" % (file_path, url))

######################################################################################################################
# @name                                 : ValidateSchema
#
# @description                          : Checks if the fields are the same as expected by this program
#
# @param fields                         : List of fields present in the given file
#
# @returns                              : True if the number of fields and number of entries in each row are same.
######################################################################################################################
def ValidateSchema(fields):
    return (MUTUAL_FUND_FIELDS == fields)

######################################################################################################################
# @name                                 : InitializeMonitoredFundDictionary
#
# @description                          : Initializes the monitored fund dictionary to keep track of funds
#                                         whose details have been found in the fund details file.
#
# @param fundsToMonitor                 : List of fields present in the given file
#
# @returns                              : dictionary of fund name and true/false
######################################################################################################################
def InitializeMonitoredFundDictionary(fundsToMonitor):
    fundDict = {}
    for fund in fundsToMonitor:
        fundDict[fund] = False

    return fundDict

######################################################################################################################
# @name                                 : LoadFundDetailsFile
#
# @description                          : Loads the file_path containing details of all the mutual funds in a
#                                         CSV format. The format is:
#                                         "Scheme Code";"ISIN Div Payout/ ISIN Growth","ISIN Div Reinvestment";"Scheme Name";"Net Asset Value";"Date"
#
# @param file_path                      : File path containing the details of all the Mutual Funds.
#
# @returns                              : List of all the entries found in the file
######################################################################################################################
def LoadFundDetailsFile(file_path):
    fields = []
    rows = []

    if (not os.path.isfile(file_path)):
        return rows

    statinfo = os.stat(file_path)
    if (statinfo.st_size > 0):
        # creating a csv reader object
        csvreader = csv.reader(open(file_path), delimiter=";")

        # extracting field names through first row
        fields = next(csvreader)
        if (ValidateSchema(fields)):
            # extracting each data row one by one
            for row in csvreader:
                # only those rows are valid which have same number of
                # attributes as number of fields
                if (len(row) == len(fields)):
                    rows.append(row)
        else:
            print ("\n*** WARNING: Schema of file has changed! Processing might not work correctly\n")

        # get total number of rows
        print("Total no. of rows in file                 : %d" % (csvreader.line_num))
        print("Total no. of Mutual Funds entries in file : %d\n" % (len(rows)))

    else:
        print ("%s: File Not found!" % file_path)

    return rows

######################################################################################################################
# @name                                 : DisplayFundDetails
#
# @description                          : Displays the details of the funds which are being monitored
#
# @param monitoredFunds                 : List of funds to monitor
#
# @returns                              : Nothing
######################################################################################################################
def DisplayFundDetails(monitoredFunds, status):
    recordIndex = 1
    fieldIndex = 0
    print ("\n *** Funds being monitored *** ")
    for fund in monitoredFunds:
        print ("+------------------------------------------------------------------------------------+")
        print ("| %d) %s" % (recordIndex, fund[SCHEME_NAME_INDEX]))
        print ("+------------------------------------------------------------------------------------+")
        for fieldIndex in range(len(MUTUAL_FUND_FIELDS)):
            if (fieldIndex != SCHEME_NAME_INDEX):
                print ("| %-30s  : %s " % (MUTUAL_FUND_FIELDS[fieldIndex], fund[fieldIndex]))

        recordIndex = recordIndex + 1

######################################################################################################################
# @name                                 : FetchMonitoredFundDetails
#
# @description                          :
#
# @param allMutualFunds                 : List of all the mutual funds'  details
# @param fundsToMonitor                 : List of fund names to monitor
# @param monitoredFundDictionary        : [OUT] A dictionary of funds being monitored
#
# @returns                              : List of monitored funds' details. Each item in itself
#                                         is a list containing field values (name, nav, date etc.)
######################################################################################################################
def FetchMonitoredFundDetails(allMutualFunds, fundsToMonitor, monitoredFundDictionary):
    monitoredFundDetails = []

    for fund in allMutualFunds:
        # If this fund is in the list of funds to monitor
        if (fund[SCHEME_NAME_INDEX] in fundsToMonitor):
            # Display details
            monitoredFundDetails.append(fund)
            monitoredFundDictionary[fund[SCHEME_NAME_INDEX]] = True

    return monitoredFundDetails

######################################################################################################################
# @name                                 : ValidateMonitoredFunds
#
# @description                          : Checks if all the funds being monitored have been tracked. Displays
#                                         additionaly information if present
#
# @param monitoredFundDictionary        : A dictionary of funds being monitored
# @param status                         : List of status messages to be displayed
#
# @returns                              : Nothing
######################################################################################################################
def DisplayStatus(monitoredFundDictionary, status):
    successCount = 0
    failedCount = 0
    print ("\n")
    print("+------------------------------------------------------------------------------------+")
    print("|                                 S T A T U S                                        |")
    print("+------------------------------------------------------------------------------------+")
    for key, value in monitoredFundDictionary.items():
        if (value == False):
            print ("> Fund info not found  : %s" % (key))
            failedCount = failedCount + 1
        else:
            #print ("Success : %s" % (key))
            successCount = successCount + 1

    if (failedCount == 0):
        print("> Values found for all the Mutual Funds being tracked")


    for msg in status:
        print (">", msg)

######################################################################################################################
# @name                                 : FetchPrevMonitoredFundDetailsFromFile
#
# @description                          : Loads the trackingFile containing details of all the mutual funds previously
#                                          tracked. The data is in CSV format. The format is:
#                                         "Scheme Code";"ISIN Div Payout/ ISIN Growth","ISIN Div Reinvestment";"Scheme Name";"Net Asset Value";"Date"
#
# @param trackingFile                   : File path containing the details of all the previously tracked Mutual Funds.
#
# @returns                              : List of all the entries found in the file
######################################################################################################################
def FetchPrevMonitoredFundDetailsFromFile(trackingFile):
    print("\nFetching previously tracked Funds' details from file [ %s ]" % trackingFile)
    prevMonitoredFundDetails = LoadFundDetailsFile(trackingFile)

    print ("Fetched %d records from previously tracked funds\n" % len(prevMonitoredFundDetails))
    return prevMonitoredFundDetails

######################################################################################################################
# @name                                 : DumpMonitoredFundDetailsToFile
#
# @description                          : Dumps all the detail of all monitored funds to tracking file The data is
#                                         in CSV format. The format is:
#                                         "Scheme Code";"ISIN Div Payout/ ISIN Growth","ISIN Div Reinvestment";"Scheme Name";"Net Asset Value";"Date"
#
# @param monitoredFundDetails           : Mutual funds' whose details have to be dumped
# @param trackingFile                   : File path containing the details of all the previously tracked Mutual Funds.
#
# @returns                              : Nothing
######################################################################################################################
def DumpMonitoredFundDetailsToFile(monitoredFundDetails, trackingFile):
    print ("\nDumping Monitored Funds details to file [ %s ]" % trackingFile)
    file = open(trackingFile, "w")
    if (file):
        # Dump schema
        fieldValueIndex = 0
        for fieldValue in MUTUAL_FUND_FIELDS:
            file.write(fieldValue)
            fieldValueIndex = fieldValueIndex + 1

            if (fieldValueIndex < len(MUTUAL_FUND_FIELDS)):
                file.write(';')

        # New line at the end of the entry
        file.write('\n')

        # Dump actual data
        for fund in monitoredFundDetails:
            dataIndex = 0
            for data in fund:
                file.write(data)
                dataIndex = dataIndex + 1

                if (dataIndex < len(fund)):
                    file.write(';')

            # New line at the end of the entry
            file.write('\n')

        file.close()

######################################################################################################################
# @name                                 : CompareFunds
#
# @description                          : All the logic of comparison of fund performance in comparison to
#                                         previously tracked values
#
# @param prevMonitoredFundDetails       : List of details previously monitored funds
# @param currMonitoredFundDetails       : List of details currently monitored funds
#
# @returns                              : True if differences have been found in the values
######################################################################################################################
def CompareFunds(prevMonitoredFundDetails, currMonitoredFundDetails, status):
    print("\n *** Comparing funds...")

    index = 0
    doComparison = (len(prevMonitoredFundDetails) == len(currMonitoredFundDetails))
    isUpdateRequired = False

    for currFund in currMonitoredFundDetails:
        indicator = ""
        currNav = float(currFund[NAV_INDEX])
        print("+------------------------------------------------------------------------------------+")
        print("| %d) %s" % (index + 1, currFund[SCHEME_NAME_INDEX]))
        print("+------------------------------------------------------------------------------------+")
        print("| %-15s  : %f " % (currFund[DATE_INDEX], currNav))

        # If both schemes are same, then do a comparison
        if (doComparison and
            prevMonitoredFundDetails[index][SCHEME_NAME_INDEX] == currFund[SCHEME_NAME_INDEX]):
            prevNav = float(prevMonitoredFundDetails[index][NAV_INDEX])
            percentChangeInNav = ((currNav - prevNav)/prevNav) * 100
            if (abs(percentChangeInNav) >= float(HIGHLIGHT_THRESHOLD)):
                indicator = "(*)"
                msg = "%s  NAV changed from %f --> %f" % (currFund[SCHEME_NAME_INDEX], prevNav, currNav)
                status.append(msg)

            if (percentChangeInNav != 0.0):
                isUpdateRequired = True

            print("| %-15s  : %f " % (prevMonitoredFundDetails[index][DATE_INDEX], prevNav))
            print("| Percent change   : %f %%  %s" % (percentChangeInNav, indicator))

        index = index + 1

    if (not isUpdateRequired):
        status.append("No change in NAVs since last execution")

    return isUpdateRequired


######################################################################################################################
#    M A I N
######################################################################################################################
status = []
fundsToMonitor = GetFundListToMonitor(FUNDS_TO_MONITOR_FILE)
if (len(fundsToMonitor)):
    monitoredFundDictionary = InitializeMonitoredFundDictionary(fundsToMonitor)

    DownloadFundDetailsFile(FUND_DETAIL_URL, FUND_DETAIL_FILE)
    allMutualFunds = LoadFundDetailsFile(FUND_DETAIL_FILE)
    if (len(allMutualFunds) > 0):
        currMonitoredFundDetails = FetchMonitoredFundDetails(allMutualFunds, fundsToMonitor, monitoredFundDictionary)
        prevMonitoredFundDetails = FetchPrevMonitoredFundDetailsFromFile(PREVIOUS_TRACKED_DETAILS_FILE)

        if (len(prevMonitoredFundDetails) == 0):
            # No previous record found. Simply display the details of all the mutual funds being tracked
            isUpdateRequired = True
            DisplayFundDetails(currMonitoredFundDetails, status)
        else:
            # Display comparison of funds
            isUpdateRequired = CompareFunds(prevMonitoredFundDetails, currMonitoredFundDetails, status)

        # Update PREVIOUS_TRACKED_DETAILS_FILE only if required
        if (isUpdateRequired):
            DumpMonitoredFundDetailsToFile(currMonitoredFundDetails, PREVIOUS_TRACKED_DETAILS_FILE)

        # Display status
        DisplayStatus(monitoredFundDictionary, status)

    else:
        print ("ERROR: Failed to load Mutual Funds details from file. Make sure the schema is as required by this script!!")
else:
    print ("ERROR: No fund found in [ %s ]" % FUNDS_TO_MONITOR_FILE)
