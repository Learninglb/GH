''' Takes a csv file from metering and
    breaks it down to generate .dat files
    needed for import. '''

import csv
import glob

FIRST = ['BATCH']
SECOND = ['ADD']
THIRD = ['PATH']
FOURTH = ['LAKESIDE']
FIFTH = ['All']
SIXTH = ['ALL']
SEVENTH = ['ALL']
EIGHTH = ['LG']
NINTH = ['ALL']


# Create a list of only the serial number column from csv
UPLOAD_FOLDER = glob.glob("c:/GH/my_webapps/app/static/csv/uploads/*")

for file in UPLOAD_FOLDER:
    data = pd.read_csv(file)
    data.columns = ["Meter_#", "Sec_Meter_#", "Serv_Addr", "Stat", "Meter_Type", "Account",
                    "Serv_Loc_#", "Name", "Service_Use_Type", "AMR_Transponder_ID"]
    nbr_list = list(data.AMR_Transponder_ID)

    # create new file
    for value in nbr_list:
        with open('newLines.csv', 'a', newline='') as file:
            text = FIRST + SECOND + THIRD + \
                [value] + FOURTH + FIFTH + SIXTH + SEVENTH + EIGHTH + NINTH
            writer = csv.writer(file)
            writer.writerow(text)

    # create .dat files with 150 lines each
    csvfile = open('newLines.csv', 'r').readlines()
    filename = 1
    for i in range(len(csvfile)):
        if i % 150 == 0:
            open("c:/GH/my_webapps/app/static/client/dat" +
                 str(filename) + '.dat', 'w+').writelines(csvfile[i:i+150])
            filename += 1

# Clean up files
# os.remove("c:/GH/my_webapps/newLines.csv")
# for file in upload_folder:
#    try:
#        os.remove(file)
#    except:
#        Print("Error while deleting")
