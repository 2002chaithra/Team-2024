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

    def StoreStudentScore(self):
        '''
        It allows the user to enter new student data and stores it to the CSV file.
        This method checks for existing roll numbers to avoid duplicates and validates input
        before saving it. It consists a console menu with the options save and back.
        '''
        logging.debug("Entering into the StoreStudentScore method")
        while True:
            option = input("Select an option\n1. Save\n2. Back\n>>>")
            if option == '1':
                rollno = input("Roll no: ")
                if any(row['Rollno'] == rollno for row in self.csv_reader):
                    print("Roll no already exists!")
                    break
                else:
                    student_name = input("Enter the Student Name: ")
                    english = input("Enter English score: ")
                    maths = input("Enter Maths score: ")
                    science = input("Enter Science score")
                    self.save(rollno, student_name, english, maths, science)
            elif option == '2':
                break
            else:
                logging.warning("Invalid option")
                print("Invalid option")
                input("Press Enter to continue...")

    def save(self,rollno,student_name,english,maths,science):
        '''
        Save a new student's data to the CSV file.
        :param rollno: The rollno of the student.
        :param student_name: The name of the student.
        :param english: The english score of the student.
        :param maths: The maths score of the student.
        :param science: The science score of the student.
        This method appends the new data to the Csv file.
        '''
        logging.debug("Entering into the save method")
        row = {'Rollno':rollno,
               'name':student_name,
               'english':english,
                'maths':maths,
               'science':science
               }
        ls = []
        for key in row:
            if row[key] == '':
                ls.append(key)
        if len(ls) == 0:
            with open(self.file_name,'a+',newline='') as file:
                writer = csv.DictWriter(file, fieldnames=row.keys())
                writer.writerow(row)
                print("Student data stored successfully.")
                logging.info("Student data stored successfully.")
        else:
            print(f"Failed to store data, following parameters are missing : {",".join(ls)}")

    def average(self):
        '''
        Calculates the average store of the student and adds them to the CSV file under a new column Average.
        This method calculates the average of English, Maths, and Science scores for each student
        and adds an 'Average' column to the CSV file. If the 'Average' column already exists, a warning is logged.
        '''
        logging.debug("Entering into the average method")
        if 'Average' not in self.fieldnames:
            self.fieldnames.append('Average')
        else:
            logging.warning("Column already exists")
        reader = csv.DictReader(self.csv_file)
        self.csv_file.seek(0)
        rows = list(reader)
        self.csv_file.seek(0)
        writer = csv.DictWriter(self.csv_file, fieldnames=self.fieldnames)
        writer.writeheader()
        for row in rows:
            avg = (int(row['english']) + int(row['maths']) + int(row['science'])) / 3
            row['Average'] = round(avg,2)
            writer.writerow(row)
        logging.info("Average column is created.")
        print("Average of the three subject is calculated")

    def displayAll(self,header,ascending = True):
        '''
        Display all student records sorted by a specified header.
        :param header: The header by which to sort the records.
        :param ascending: Takes boolean values True or False to sort the records in either ascending or descending
                        order. Default value is True.
        This method sorts and prints all student records based on the specified header. It also updates the
        CSV file with the sorted data.
        '''
        logging.debug("Entering into the displayAll method")
        self.csv_file.seek(0)
        if header not in self.fieldnames:
            print("Header not found")
            logging.warning("Header not found")
            return
        reader = csv.DictReader(self.csv_file)
        rows = list(reader)
        for row in rows:
            if row[header].isdigit():
                rows.sort(key=lambda row: float(row[header]),reverse= not ascending)
            else:
                rows.sort(key=lambda row: row[header],reverse= not ascending)
        for row in rows:
            print(row)
        self.csv_file.seek(0)
        writer = csv.DictWriter(self.csv_file,fieldnames=self.fieldnames)
        writer.writeheader()
        writer.writerows(rows)
        logging.info("Records are sorted")
    def mainMenu(self):
        '''
        Display the main menu and handle user input to perform various operations.
        Consists a console menu with options Retrieve student score, Store student score, Calculate average,
        Sort records and exit.
        '''
        logging.debug("Entering into the mainMenu method")
        while True:
            option = input(
                "Enter the choice\n1. Retrive Student Score\n2. Store Student Score\n3. Calculate average\n4. Sort records\n5. Exit\n>>> ")
            if option == '1':
                rollno = input("Enter the Roll no.: ")
                self.RetrieveStudentScore(rollno)
            elif option == '2':
                self.StoreStudentScore()
            elif option == '3':
                self.average()
            elif option == '4':
                header = input("Enter the header: ")
                ascending = input("Enter True or False: ").capitalize()
                if ascending == 'True':
                    ascending = True
                    self.displayAll(header, ascending)
                elif ascending == 'False':
                    ascending = False
                    self.displayAll(header, ascending)
                else:
                    self.displayAll(header)
            elif option == '5':
                print("Thank you")
                self.csv_file.close()
                sys.exit()
            else:
                print("Invalid choice")

f = StudentScore("student_data.csv")
f.mainMenu()

