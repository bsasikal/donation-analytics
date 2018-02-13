# Donation-Analytics - Business Logic

The application code is developed in Python. No additional libraries are used.

To run the application, python installation is essential.

Below is the high level overview on how the application works.

1) Reads input file one line at a time

2) Validates input record according to the business requirements
* Transaction Date is expected to be in YYYYMMDD format
*  Donation Amount value is assumed to be a rounded integer (no precision point calculation)

3) Any invalid record will be ignored.

4) Two global dictionaries are maintained
* `donor_rec`: one to track the donor contributions details (repeat vs single donor, marked by a boolean "Y" - repeat donor or "N")
* `recep_rec`: another to track the contributions received for the candidate/recipient (grouped by candidate id, zipcode and year)

5) Boolean value in contrib_rec will be initially set to "N". Only if the donor has donated in consecutive years and if the consecutive years are in chronological order, boolean is set to "Y". Otherwise the records are ignored and the donor is not considered as a repeat donor.

6) For every repeat donor, perform the following
* Append donation amount to the list in recep_rec dict for the key grouped by candidate id, zipcode and year.
* Perform percentile calculation for the list of donation amount values in recep_rec for that candidate id, zipcode and year.
* Write to output file.

