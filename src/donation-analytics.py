import sys
import datetime
import re
import collections
import decimal
from decimal import Decimal
from datetime import datetime as dt
from collections import defaultdict

donor_rec = collections.defaultdict(dict)
recep_rec = defaultdict(list)

input_file_path = None
percentile_file = None
outfile = None

tmp_percentile = 0
percentile_list=[]

# percentile_calc
def calc_percentile(percentile_list):

    if percentile_list:
        percentile_list.sort()

        calc_perc = (float(tmp_percentile) / 100) * len(percentile_list)
        calc_perc = round(calc_perc, 0)

        if calc_perc == 0:
            return percentile_list[int(calc_perc)]

        return percentile_list[int(calc_perc)-1]

#parse record for values and validate them
def parse_record_and_validate(line):
    record = {}

    if not line or line == "\n":
        return {}

    # get the host by splitting the record for space and get the first indexed item
    tokens = line.split("|")

    chk_pattern = '[^a-zA-Z\ \,]'
    if tokens[15] == '' and tokens[0].isalnum() and tokens[10].isdigit() and not(re.search(chk_pattern, tokens[7])):
        try:
            datetime.datetime.strptime(tokens[13], '%m%d%Y')
            decimal.Decimal(tokens[14])
        except ValueError:
            return {}
        except decimal.InvalidOperation:
            return {}

        record["CMTE_ID"] = tokens[0]
        record["NAME"] = tokens[7]
        record["ZIPCODE"] = tokens[10][0:5]
        record["TRANSACTION_DATE"] = tokens[13][4:8]
        record["TRANSACTION_AMT"] = tokens[14]
        record["OTHER_ID"] = tokens[15]
        return record
    else:
        return{}

#Calculation of Donation Analytics
def calc_donation_analytics(record):
        Tmp_Donation = decimal.Decimal(record["TRANSACTION_AMT"])

        Name_Zip = record["NAME"] + "|" + record["ZIPCODE"]
        Recep_Zip_Year = record["CMTE_ID"] + "|" + record["ZIPCODE"] + "|" + record["TRANSACTION_DATE"]

        if donor_rec.has_key(Name_Zip):

            #repeat_donors - donors who has contributed more than once in consecutive years
            if record["TRANSACTION_DATE"] > (donor_rec[Name_Zip].keys()[0]):
                donor_rec[Name_Zip][record["TRANSACTION_DATE"]] = "Y"

            #If the donor is a repeat donor and is contributing more than once in current year
            if record["TRANSACTION_DATE"] >= donor_rec[Name_Zip].keys()[0] and (donor_rec[Name_Zip][record["TRANSACTION_DATE"]] == "Y"):
                recep_rec[Recep_Zip_Year].append(Tmp_Donation)

                num_contrib = 0
                percentile_list = []

                total_donation = sum(recep_rec[Recep_Zip_Year])

                percentile_list = recep_rec[Recep_Zip_Year]
                #Call the function to calculate percentile
                calc_perc = calc_percentile(percentile_list)
                num_contrib = len(percentile_list)

                outfile.write(Recep_Zip_Year + "|" + str(calc_perc) + "|" + str(total_donation) + "|" + str(num_contrib) + "\n")
        else:
            donor_rec[Name_Zip][record["TRANSACTION_DATE"]] = "N"

def read_input_file():
#   iterate through input file, line by line
    with open(input_file_path) as fileobject:
        for line in fileobject:

            #parse record for values and to validate
            record = parse_record_and_validate(line)

            if (record):
                #Calculation of Donation Analytics
                calc_donation_analytics(record)

def main():
    global input_file_path
    global outfile
    global percentile_file
    global tmp_percentile

    print "application started " + str(dt.now())

    if len(sys.argv) != 4:
        print len(sys.argv)
        print 'Usage: donation-analytics.py <input_file1> <input_file2> <output_file>'
        sys.exit()

    input_file_path = sys.argv[1]
    percentile_file_path = sys.argv[2]
    output_file_path = sys.argv[3]

    percentile_file = open(percentile_file_path, "r")

    tmp_percentile = int(percentile_file.readline())
    if tmp_percentile <= 0 or tmp_percentile > 100:
        percentile_file.close()
        print "Percentile value is invaild"
        print "application ended " + str(dt.now())
        exit()

    outfile = open(output_file_path, "w")

    read_input_file()

    outfile.close()
    percentile_file.close()
    print "application ended " + str(dt.now())

if __name__ == "__main__":
    main()
