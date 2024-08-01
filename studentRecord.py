import csv
import sys
import logging
logging.basicConfig(format='%(asctime)s %(levelname)s : %(message)s', filemode='w', filename='studentLog.log',level=logging.DEBUG)

class StudentScore:

    def __init__(self,file_name):
        '''
        Initialize the StudentScore class.
        :param file_name: The name of the CSV file.
        It reads the CSV file and initializes the CSV reader with the data,
        as well as extracts the fieldnames from the first row of the CSV file.
        '''
        self.file_name = file_name
        try:
            self.csv_file = open(file_name,'r+',newline='')
            self.csv_reader = csv.DictReader(self.csv_file)
            self.fieldnames = self.csv_reader.fieldnames
        except:
            print("Error in retrieving the data")
            logging.error("Error in retrieving the data")
            sys.exit()

    def RetrieveStudentScore(self,rollno):
        '''
        Retrieves and prints the student data for a given rollno.
        :param rollno: The rollno of the student whose data is to be retrieved.
        :return: This method return the row and outputs the dict object.
        '''
        logging.debug("Entering into the RetrieveStudentScore method")
        self.csv_reader = csv.DictReader(self.csv_file)
        self.csv_file.seek(0)
        found = False
        for row in self.csv_reader:
            if row['Rollno'] == rollno:
                found = True
                print(row)
                logging.info(f"Records for rollno {rollno} is found")
                break
        if not found:
            print(f"No records found for rollno {rollno}")
            logging.warning(f"No records found for rollno {rollno}")

f = StudentScore("student_data.csv")
rollno = input("Enter the Roll no.: ")
f.RetrieveStudentScore()

