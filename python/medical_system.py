import datetime
#=======================================================================
#========================== PATIENT CLASS ==============================
#=======================================================================
class Patient:
    def __init__(self, patient_id):
        self.patient_id=patient_id #Patient ID
        self.patient_tests=[]      #Dictionary of tests, where the test name
    def add_test(self): #Function to add a test record
        print("Adding test record ...")
        while True:
            test_name = read_test_name()
            test_unit=check_test_name(test_name)
            if(test_unit==False):
               print("Test does not exist - Please enter a valid test name")
            else:
                break
        test_date=read_test_date()
        for test in self.patient_tests: #Check if a test with same name and test date exist for this patient if yes, then don't add, and tell the user to update it
            if test.test_name == test_name and test.test_date == test_date:
                print("A test with the same name and date already exists. You can update it instead!")
                return #Dont add and go back
        result_val = read_numeric_value()
        result_status=read_status()
        result_date=None
        if result_status == "completed":
            result_date=read_result_date()
        new=Test(test_name,test_date,result_val,test_unit,result_status,result_date,self.patient_id)
        self.patient_tests.append(new)
        print("\n-->Record Added Successfully\n")
    def update_test(self): #Function to update test record
        print("Updating test record ...")
        while True:
            test_name = read_test_name()
            test_unit=check_test_name(test_name)
            if(test_unit==False):
               print("Test does not exist - Please enter a valid test name")
            else:
                break
        test_date = read_test_date()
        for i in range(len(self.patient_tests)):  # Check if a test with same name and test date exist for this patient if yes, then update it, else tell the user that no tests were found
            test=self.patient_tests[i]
            if test.test_name == test_name and test.test_date == test_date:
                new_res=read_numeric_value()
                new_stat=read_status()
                res_date=None
                if new_stat == "completed":
                    res_date=read_result_date()
                self.patient_tests.pop(i) #Remove the previous record
                new=Test(test_name,test_date,new_res,test_unit,new_stat,res_date,self.patient_id)
                self.patient_tests.append(new)#Add the new updated record
                print("\n-->Record Updated Successfully\n")
                return  #If updated then return
        print("Test record not found - Please enter a valid test name and date")
    def delete_test(self): #Function to delete a test record
        while True:
            t_name = read_test_name()
            test_unit = check_test_name(t_name)
            if (test_unit == False):
                print("Test does not exist - Please enter a valid test name")
            else:
                break
        t_date = read_test_date()
        for i in range (len(self.patient_tests)):
            if t_date == self.patient_tests[i].test_date and self.patient_tests[i].test_name == t_name:
                #If the test is found remove it by using pop on the index
                self.patient_tests.pop(i)
                print("\n-->Record Deleted Successfully\n")
                return
        print("Test record not found!")
#=======================================================================
#============================ TEST CLASS ===============================
#=======================================================================
class Test(Patient):
    def __init__(self, test_name, test_date, result_value, result_unit, result_status, result_date, patient_id):
        super().__init__(patient_id)
        self.test_name=test_name
        self.test_date=test_date
        self.result_value=result_value
        self.result_unit=result_unit
        self.result_status=result_status
        self.result_date=result_date
    def print_record(self): # Print Record with the format
        test_date_str = self.test_date.strftime("%Y-%m-%d %H:%M")
        if self.result_status == "completed":  # If the status is completed, print the result date
            result_date_str = self.result_date.strftime("%Y-%m-%d %H:%M")  # Put the date object into a printable string
            print(f"{self.patient_id}: {self.test_name}, {test_date_str}, {self.result_value}, {self.result_unit}, {self.result_status}, {result_date_str}")
        else:  # Else print the record without the result date
            print(f"{self.patient_id}: {self.test_name}, {test_date_str}, {self.result_value}, {self.result_unit}, {self.result_status}")
    def write_record(self): # Write Record with the format to the file
        test_date_str = self.test_date.strftime("%Y-%m-%d %H:%M")
        fileRecord=open("medicalRecord.txt","a")
        if self.result_status == "completed":  # If the status is completed, print the result date
            result_date_str = self.result_date.strftime("%Y-%m-%d %H:%M")  # Put the date object into a printable string
            fileRecord.write(f"{self.patient_id}: {self.test_name}, {test_date_str}, {self.result_value}, {self.result_unit}, {self.result_status}, {result_date_str}\n")
        else:  # Else print the record without the result date
            fileRecord.write(f"{self.patient_id}: {self.test_name}, {test_date_str}, {self.result_value}, {self.result_unit}, {self.result_status}\n")
        fileRecord.close()
    def write_csv(self): #Write the record with the format to a csv file
        test_date_str = self.test_date.strftime("%Y-%m-%d %H:%M")
        fileRecord = open("medicalRecord.csv", "a")
        if self.result_status == "completed":  # If the status is completed, print the result date
            result_date_str = self.result_date.strftime("%Y-%m-%d %H:%M")  # Put the date object into a printable string
            fileRecord.write(f"{self.patient_id};{self.test_name};{test_date_str};{self.result_value};{self.result_unit};{self.result_status};{result_date_str}\n")
        else:  # Else print the record without the result date
            fileRecord.write(f"{self.patient_id};{self.test_name};{test_date_str};{self.result_value};{self.result_unit};{self.result_status}\n")
        fileRecord.close()
    def checkAbnormal(self): #Check if test is abnormal
        value=float(self.result_value)
        name=self.test_name
        range_str=check_test_for_range(name)
        if range_str.find('<')!=-1 and range_str.find('>')!=-1: #If there is both min and max range then find them both using split
            min=float(range_str.split(',')[0].split(' ')[2])
            max=float(range_str.split(',')[1].strip().split(' ')[1])
            if value >= min and value <= max:
                return False # If val is in range return false not abnormal
            else:
                return True #If val is out of range return true is abnormal
        elif range_str.find('<')!=-1: #Else if there is only a max then find it
            max=float(range_str.split(' ')[2])
            if value > max:
                return True #If val bigger than max return True is abnormal
            else:
                return False #If val not bigger than max return false not abnormal
        else:# there is only a min , find it
            min=float(range_str.split(' ')[2])
            if value >= min:
                return False #If val is bigger than min then return false not abnormal
            else:
                return True #If val is smaller than min return true is abnormal
    def check_tperiod(self,min,max): #Check if turnaround time for the test is in range
        name=self.test_name
        tperiod_string=check_test_for_tperiod(name)
        if tperiod_string >= min and tperiod_string <= max: #If its in range return true
            return True
        else:
            return False #else return false

    @staticmethod
    def validate_range(test_range):
        pieces = test_range.split()
        if len(pieces) == 1:
            piece = pieces[0]
            if (piece[0] == '>' or piece[0] == '<') and piece[1:].replace('.', '', 1).isdigit():
                return True
        elif len(pieces) == 3:
            piece1 = pieces[0]
            piece2 = pieces[2]
            if (piece1[0] == '>' or piece1[0] == '<') and (piece2[0] == '>' or piece2[0] == '<'):
                piece1_value = piece1[1:]
                piece2_value = piece2[1:]
                if piece1_value.replace('.', '', 1).isdigit() and piece2_value.replace('.', '', 1).isdigit():
                    return True
        return False

    @staticmethod
    def validate_unit(unit):
        for char in unit:
            if not (char.isalpha() or char.isspace() or char == '/'):
                return False
        return True

    @staticmethod
    def validate_turnaround(turnaround):
        try:
            # Split the string manually
            parts = turnaround.split('-')
            # Convert parts to integers
            days = int(parts[0])
            hours = int(parts[1])
            minutes = int(parts[2])
            # Validate the ranges
            if 0 <= days < 100 and 0 <= hours < 24 and 0 <= minutes < 60:
                return True
        except Exception:
            pass

        return False

    @staticmethod
    def validate_test_name(test_name):
        for char in test_name:
            if not (char.isalpha() or char.isspace()):
                return False
        return True

    @staticmethod
    def test_name_exists(test_name):
        try:
            with open("medicalTest.txt", "r") as file:
                for line in file:
                    if f"Name: {test_name};" in line:
                        return True
        except Exception:
            print("Error: medicalTest.txt file not found.")
        return False

    @staticmethod
    def add_medical_test():
        print("Adding new medical test...")

        while True:
            test_name = input("Enter Test Name: ")
            if Test.validate_test_name(test_name) and not Test.test_name_exists(test_name):
                break
            print("Invalid test name or test already exists - Please enter a valid and unique test name")

        while True:
            min_value = input("Enter the minimum value of the range: ")
            max_value = input("Enter the maximum value of the range: ")
            if min_value.replace('.', '', 1).isdigit() and max_value.replace('.', '', 1).isdigit():
                test_range = f"> {min_value}, < {max_value}"
                break
            print("Invalid range values - Please enter valid numbers for min and max values")

        while True:
            test_unit = input("Enter the unit : ")
            if Test.validate_unit(test_unit):
                break
            print("Invalid unit format - Please enter a valid unit")

        while True:
            test_code = input("Enter the turnaround time: ")
            if Test.validate_turnaround(test_code):
                break
            print("Invalid turnaround time format - Please enter in DD-hh-mm format")

        with open("medicalTest.txt", "a") as file:
            file.write(f"Name: {test_name}; Range: {test_range}; Unit: {test_unit}, {test_code}\n")
        print("\n--> Medical Test Added Successfully\n")

    @staticmethod
    def update_medical_test():
        print("Updating medical test...")

        while True:
            test_name = input("Enter Test Name: ")
            if Test.validate_test_name(test_name) and Test.test_name_exists(test_name):
                break
            print("Invalid test name or test does not exist - Please enter a valid test name")

        while True:
            min_value = input("Enter the new minimum value of the range: ")
            max_value = input("Enter the new maximum value of the range: ")
            if min_value.replace('.', '', 1).isdigit() and max_value.replace('.', '', 1).isdigit():
                new_range = f"> {min_value}, < {max_value}"
                break
            print("Invalid range values - Please enter valid numbers for min and max values")

        while True:
            new_unit = input("Enter the new unit: ")
            if Test.validate_unit(new_unit):
                break
            print("Invalid unit format - Please enter a valid unit")

        while True:
            new_code = input("Enter the new turnaround time: ")
            if Test.validate_turnaround(new_code):
                break
            print("Invalid turnaround time format - Please enter in DD-hh-mm format")

        with open("medicalTest.txt", "r") as file:
            lines = file.readlines()

        with open("medicalTest.txt", "w") as file:
            for line in lines:
                if f"Name: {test_name};" in line:
                    file.write(f"Name: {test_name}; Range: {new_range}; Unit: {new_unit}, {new_code}\n")
                else:
                    file.write(line)
        print("\n--> Medical Test Updated Successfully\n")
#=======================================================================
#================ USER INPUT AND VALIDATION FUNCTIONS ==================
#=======================================================================
def read_patient_id(): #Function to read patient id and check it
    #Read Patient ID
    while True:
        patient_id = input("Enter Patient ID: ")
        if patient_id.isdigit():
            if len(patient_id) == 7:
                break
            else:
                print("Invalid Patient ID - Please enter a 7 digit integer")
        else:
            print("Invalid Patient ID - Please enter a 7 digit integer without characters")
    return patient_id  #Return Patient ID
def read_test_name(): #Function to read string test name
    #Read Test Name
    test_name = input("Enter Test Name: ")
    return test_name
def read_test_date(): #Function to read a date and check it
    #Read Test Date
    condition=True
    while condition:
        test_date_string = input("Enter Test Date (YYYY-MM-DD HH:MM): ")
        test_date_string.strip()
        try:
           test_date = datetime.datetime.strptime(test_date_string, "%Y-%m-%d %H:%M")
           condition=False
        except Exception:
           print("Invalid Date - Please enter a valid date with the following format: YYYY-MM-DD HH:MM")
           condition=True
    return test_date
def read_result_date(): #Function to read a date and check it
    condition=True
    while condition:
        result_date_string = input("Enter Result Date (YYYY-MM-DD HH:MM): ")
        try:
           result_date = datetime.datetime.strptime(result_date_string, "%Y-%m-%d %H:%M")
           condition=False
        except Exception:
           print("Invalid Date - Please enter a valid date with the following format: YYYY-MM-DD HH:MM")
           condition=True
    return result_date
def check_test_name(test_name): #Function to read a test name and return the unit if it exists
    #Check if test name exist in medical test information file and retrieve its unit, if the unit found return it, else return False
    medical_info = open("medicalTest.txt", "r")
    test_unit = False
    for x in medical_info:
        if test_name in x:
            test_unit = x.split("Unit:")[1]
            test_unit = test_unit.split(",")[0]
            test_unit = test_unit.strip()
            break
    if test_unit == False:
        print("Test not found - Please enter a valid test name")
    return test_unit
def check_test_for_range(test_name): #Function gets test name and return the range string
    medical_info = open("medicalTest.txt", "r")
    range = False
    for x in medical_info:
        if test_name in x:
            range = x.split(";")[1]
            break
    if range == False:
        print("Test not found- ERROR TEST NOT FOUND IN MEDICAL TEST FILE")
    return range.strip()
def check_test_for_tperiod(test_name): #Function gets test name and return the tperiod
    medical_info = open("medicalTest.txt", "r")
    tperiod = False
    for x in medical_info:
        if test_name in x:
            if x.find('<') != -1 and x.find('>') != -1:
                tperiod = x.split(',')[2].strip()
            else:
                tperiod = x.split(',')[1].strip()
            break
    if tperiod == False:
        print("Test not found- ERROR TEST NOT FOUND IN MEDICAL TEST FILE")
    return tperiod
def read_numeric_value(): #Function to read a positive numeric value (int or float) and check it
    while True:
        numeric_value = input("Enter Result value: ")
        # Initialize dotfound for each new input
        dotfound = 0
        if numeric_value.isdigit():
            return numeric_value
        for char in numeric_value:
            if dotfound == 0 and char == '.':
                dotfound = 1
            elif char.isdigit() == False:
                print("Please enter a valid positive number!")
                break
        else:
            if dotfound == 1 or numeric_value.isdigit():
                return numeric_value
def read_status(): #Function to read a status and check it
    while True:
        status_value = input("Enter a status (Pending, Completed, Reviewed): ")
        status_value = status_value.lower()
        if status_value == "pending":
            return status_value
        elif status_value == "completed":
            return status_value
        elif status_value == "reviewed":
            return status_value
        else:
            print("Please enter a valid status !")
#=======================================================================
#======================= LOAD AND SAVE TO FILES ========================
#=======================================================================
def load_medical_records(patients_dict): #Load medical records to the patients dictionary
    with open('medicalRecord.txt', 'r') as f:
        for line in f:
            if line is None: #Skip empty lines
                continue
            exist = False
            p_id = line.split(":")[0].strip()
            t_name= line.split(":")[1].split(",")[0].strip()
            test_date_string = line.split(",")[1].strip()
            test_date = datetime.datetime.strptime(test_date_string, "%Y-%m-%d %H:%M")
            t_result=line.split(",")[2].strip()
            t_unit = line.split(",")[3].strip()
            t_status = line.split(",")[4].strip()
            result_date=None
            if t_status== "completed":
                result_date_string=line.split(",")[5].strip()
                result_date = datetime.datetime.strptime(result_date_string, "%Y-%m-%d %H:%M")
            if p_id in patients_dict: #Check if the patient already exist in the dictionary
                for test in patients_dict[p_id].patient_tests:  # Check if a test with same name and test date exist for this patient if yes, then don't add,
                    if test.test_name == t_name and test.test_date == test_date:
                        exist = True
                if not exist:  # If a test with that name does not exist then add it
                    new = Test(t_name, test_date, t_result, t_unit, t_status, result_date,p_id)  # If the patient exists then just add the test
                    patients_dict[p_id].patient_tests.append(new)
            else:
                patients_dict[p_id] = Patient(p_id) #If the patient doesn't exist then create an object fot the patient and add it to the dict
                new=Test(t_name,test_date,t_result,t_unit,t_status,result_date,p_id) #If the patient exists then just add the test
                patients_dict[p_id].patient_tests.append(new)
    f.close()
    return patients_dict
def save_dictionary_to_file(patients_dict): #Function to write records in dictionary to "medicalRecord.txt"
    fileRecord=open("medicalRecord.txt","w")
    fileRecord.close()
    for patient in patients_dict:
            for test in patients_dict[patient].patient_tests:
                test.write_record()
def import_from_csv(patients_dict): #Function to import records to dictionary form import_from_csv
    imported=False
    with open('medicalRecord.csv', 'r') as f:
        for line in f:
            exist=False
            pieces=line.split(';')
            p_id = pieces[0].strip()
            t_name = pieces[1].strip()
            t_date_str=pieces[2].strip()
            t_date = datetime.datetime.strptime(t_date_str, "%Y-%m-%d %H:%M")
            t_res=pieces[3].strip()
            t_unit=pieces[4].strip()
            t_status=pieces[5].strip()
            r_date=None
            if t_status== "completed":
                r_date_str = pieces[6].strip()
                r_date = datetime.datetime.strptime(r_date_str, "%Y-%m-%d %H:%M")
            if p_id in patients_dict: #Check if the patient already exist in the dictionary
                for test in patients_dict[p_id].patient_tests:  # Check if a test with same name and test date exist for this patient if yes, then don't add, and tell the user to update it
                    imported = True
                    if test.test_name == t_name and test.test_date == t_date:
                        exist=True
                if not exist: #If a test with that name does not exist then add it
                    new=Test(t_name,t_date,t_res,t_unit,t_status,r_date,p_id) #If the patient exists then just add the test
                    patients_dict[p_id].patient_tests.append(new)
            else:
                patients_dict[p_id] = Patient(p_id) #If the patient doesn't exist then create an object fot the patient and add it to the dict
                new=Test(t_name,t_date,t_res,t_unit,t_status,r_date,p_id) #If the patient exists then just add the test
                patients_dict[p_id].patient_tests.append(new)
                imported=True
    f.close()
    if imported:
        print("\n--> medicalRecord.csv imported Successfully!\n")
    else:
        print("ERROR - FILE NOT IMPORTED SUCCESSFULLY\n")
    return patients_dict
def export_to_csv(patient_dict): #Export records in patient dictionary to csv file
    f=open("medicalRecord.csv","w")
    f.close()
    for patient in patient_dict:
        for test in patient_dict[patient].patient_tests:
            test.write_csv()
    print("\n--> Records exported to \"medicalRecord.csv\"\n")
#=======================================================================
#=========================== FILTERING =================================
#=======================================================================
def print_filter_criteria(): #Print menu for criteria
    print("")
    print("=== FILTER MEDICAL RECORDS OPTIONS ===")
    print("Please choose the criteria of your filter:")
    print("1. Select Patient ID")
    print("2. Select Test Name")
    print("3. Select Test Result Abnormal")
    print("4. Select Test Period (Start and end Date)")
    print("5. Select Test Status")
    print("6. Select Test turnaround time (min and max)")
    print("7. Save Criteria and search")
    print("8. Return to Main Menu")
    print("")
def filter_test_records(patients_dict): #Functions to filter test records based on criteria and print the result
    #Check if there are any records
    #Create a list of patient keys to have list of ids
    patient_id_list = list(patients_dict.keys())
    if len(patient_id_list) == 0:
        print("There are no records in the system - Empty")
        return
    #Set all values of possible criteria to none
    p_id=None
    t_name=None
    abnormal=False
    start_date=None
    end_date=None
    status_val=None
    min_time=None
    max_time=None
    #Get the criteria from the user
    while True:
        print_filter_criteria()
        choice = input("Please select a criteria to adjust: ")
        if choice == "1": #Read Patient ID
            p_id = read_patient_id()
        elif choice == "2": #Read Test Name
            t_name = read_test_name()
        elif choice == "3": #Check if the user want abnormal
            abnormal = input("Do you want to search for abnormal tests? (y/n): ")
            if abnormal.lower() == "y":
                abnormal = True
            else:
                abnormal = False
        elif choice == "4": #Check if the user want start and end date
            while True:
                print("Enter Start Date:")
                start_date = read_test_date()
                print("Enter End Date:")
                end_date = read_test_date()
                if start_date > end_date:
                    print("Please enter a valid date - Start date cant be later than end date!")
                else:
                    break
        elif choice == "5": #Check if the user want status
            status_val=read_status()
        elif choice == "6": #Check if the user want a specific turnaround time
            while True:
                min_time = input("Enter the minimum turnaround time: ")
                if Test.validate_turnaround(min_time):
                    break
                print("Invalid turnaround time format - Please enter in DD-hh-mm format")
            while True:
                max_time = input("Enter the maximum turnaround time: ")
                if Test.validate_turnaround(max_time):
                    break
                print("Invalid turnaround time format - Please enter in DD-hh-mm format")
        elif choice == "7": #Save criteria and Search
            break #Break out of the criteria loop and go to filter algorithm
        elif choice == "8":
            print("\nReturning to Main Menu ...\n")
            return #Return to main menu without performing search
        else:
            print("Please select a valid criteria option!")
    # Here the search algorithm Starts
    found=0
    for index in range(len(patient_id_list)):
        id=patient_id_list[index]
        if id != p_id and p_id is not None: # If the criteria p_id is set, and not equal to this patient then skip this patient
            continue
        #If it is equal or no p_id is set in criteria then search in this patients tests
        for test in patients_dict[id].patient_tests:
            #Check if test name is set,
            if (t_name is not None) and t_name != test.test_name: # If a test name is set and its not equal to the criteria name then skip this test
                continue
            if (start_date is not None) and (end_date is not None) and (start_date > test.test_date or end_date < test.test_date):
                #If start and end date is set, and the test date is later then end date or before start date then skip this test
                continue
            if (status_val is not None) and status_val!=test.result_status: #If status value is set and it is not equal to this test status then skip this test
                continue
            #Here check if abnormal is true(then we are looking for abnormal test), and check if is normal then skip this test
            if (abnormal is True) and test.checkAbnormal() is False:
                continue
            #Here check if min and max is none for turnaround time, then check if its in the wrong range then skip this test
            if (min_time is not None) and (max_time is not None) and test.check_tperiod(min_time, max_time) is False:
                continue
            #If the program reaches this point then this test is according to criteria and print it
            found=1
            test.print_record()
    if found==0:
        print("There are no records in the system with this criteria - Empty\n")
    print("")
#========================================================================
#================= GENERATE TEXTUAL SUMMARY REPORTS =====================
#========================================================================
def generate_sum_report(patients_dict): #Function to generate a textual summary report
    print("=========================================")
    print("======== GENERATE SUMMARY REPORT ========")
    print("=========================================")
    # Check if there are any records
    # Create a list of patient keys to have list of ids
    patient_id_list = list(patients_dict.keys())
    if len(patient_id_list) == 0:
        print("There are no records in the system - Empty\n")
        return
    #Criteria to print:
    test_name_list=list()
    min_val=None
    max_val=None
    counter=0
    sum=0
    # Set all values of possible criteria to none
    p_id = None
    t_name = None
    abnormal = False
    start_date = None
    end_date = None
    status_val = None
    min_time = None
    max_time = None
    # Get the criteria from the user
    while True:
        print_filter_criteria()
        choice = input("Please select a criteria to adjust: ")
        if choice == "1":  # Read Patient ID
            p_id = read_patient_id()
        elif choice == "2":  # Read Test Name
            t_name = read_test_name()
        elif choice == "3":  # Check if the user want abnormal
            abnormal = input("Do you want to search for abnormal tests? (y/n): ")
            if abnormal.lower() == "y":
                abnormal = True
            else:
                abnormal = False
        elif choice == "4":  # Check if the user want start and end date
            while True:
                print("Enter Start Date:")
                start_date = read_test_date()
                print("Enter End Date:")
                end_date = read_test_date()
                if start_date > end_date:
                    print("Please enter a valid date - Start date cant be later than end date!")
                else:
                    break
        elif choice == "5":  # Check if the user want status
            status_val = read_status()
        elif choice == "6":  # Check if the user want a specific turnaround time
            while True:
                min_time = input("Enter the minimum turnaround time: ")
                if Test.validate_turnaround(min_time):
                    break
                print("Invalid turnaround time format - Please enter in DD-hh-mm format")
            while True:
                max_time = input("Enter the maximum turnaround time: ")
                if Test.validate_turnaround(max_time):
                    break
                print("Invalid turnaround time format - Please enter in DD-hh-mm format")
        elif choice == "7":  # Save criteria and Search
            break  # Break out of the criteria loop and go to filter algorithm
        elif choice == "8":
            print("Returning to Main Menu ...")
            return  # Return to main menu without performing search
        else:
            print("Please select a valid criteria option!")
    # Here the search algorithm Starts
    found = 0
    for index in range(len(patient_id_list)):
        id = patient_id_list[index]
        if id != p_id and p_id is not None:  # If the criteria p_id is set, and not equal to this patient then skip this patient
            continue
        # If it is equal or no p_id is set in criteria then search in this patients tests
        for test in patients_dict[id].patient_tests:
            # Check if test name is set,
            if (t_name is not None) and t_name != test.test_name:  # If a test name is set and its not equal to the criteria name then skip this test
                continue
            if (start_date is not None) and (end_date is not None) and (
                    start_date > test.test_date or end_date < test.test_date):
                # If start and end date is set, and the test date is later then end date or before start date then skip this test
                continue
            if (status_val is not None) and status_val != test.result_status:  # If status value is set and it is not equal to this test status then skip this test
                continue
            # Here check if abnormal is true(then we are looking for abnormal test), and check if is normal then skip this test
            if (abnormal is True) and test.checkAbnormal() is False:
                continue
            # Here check if min and max is none for turnaround time, then check if its in the wrong range then skip this test
            if (min_time is not None) and (max_time is not None) and test.check_tperiod(min_time, max_time) is False:
                continue
            # If the program reaches this point then this test is according to criteria and check it against min
            found = 1
            test_val = float(test.result_value)
            if min_val is None or test_val < min_val:
                min_val = test_val
            if max_val is None or test_val > max_val:
                max_val = test_val
            counter+= 1
            sum=sum+test_val
            test_name_list.append(test.test_name)
    if found == 0:
        print("There are no records in the system with this criteria - Empty")
    else:
        days=0
        hours=0
        minutes=0
        counter_tper=0
        max_ttime=None
        min_ttime=None
        for name in test_name_list:
            tper=check_test_for_tperiod(name)
            day_in_t=float(tper.split('-')[0])
            hour_in_t=float(tper.split('-')[1])
            minutes_in_t=float(tper.split('-')[2])
            days=days+day_in_t
            hours=hours+hour_in_t
            minutes=minutes+minutes_in_t
            counter_tper=counter_tper+1
            if min_ttime is None or tper < min_ttime:
                min_ttime=tper
            if max_ttime is None or tper > max_ttime:
                max_ttime=tper
        total_minutes=(days*24*60)+(hours*60)+(minutes)
        avg_minutes=total_minutes/counter_tper #After calculating average minutes for tperiod - put it back into the format
        numberofdays=int(avg_minutes/(24*60))
        remainder=int(avg_minutes%(24*60))
        numberofhours=int(remainder/(60))
        numberofminutes=int(remainder%(60))
        print("=========================================")
        print("======== TEXTUAL SUMMARY REPORT =========")
        print("=========================================\n")
        print(f"- Maximum Test value is: {max_val}")
        print(f"- Average Test value is: {sum/counter}")
        print(f"- Minimum Test value is: {min_val}")
        print("=========================================")
        print(f"- Maximum Turnaround time is: {max_ttime}")
        print(f"- Average Turnaround time is: {numberofdays}-{numberofhours}-{numberofminutes}")
        print(f"- Minimum Turnaround time is: {min_ttime}")
        print("=========================================\n")

# =======================================================================
# ======================== PROGRAM MAIN CODE ============================
# =======================================================================
def main(): #Main code of the program to be executed, we put it like this just for organization
    patients_dict={}
    print("--> Loading medical records ...\n")
    patients_dict=load_medical_records(patients_dict)
    print("")
    print("=======================================")
    print("Medical Tests Records Management System")
    print("=======================================")
    print("")
    while True:
        print("Choose on the following options:")
        print("1. Add Medical Record for a patient")
        print("2. Update a patient's medical record")
        print("3. Delete a patient's medical record")
        print("4. Add Medical Test to file")
        print("5. Update Medical Test in file")
        print("6. Filter Medical Test Records")
        print("7. Generate textual summary reports")
        print("8. Import from csv file")
        print("9. Export to csv file")
        print("10. Exit")
        choice = input("Enter your choice: ")
        if choice == "1": #Add Test Record
            patient_id = read_patient_id()
            if patient_id in patients_dict: #Check if the patient already exist in the dictionary
                patients_dict[patient_id].add_test() #If the patient exists then just add the test
            else:
                patients_dict[patient_id] = Patient(patient_id) #If the patient doesn't exist then create an object fot the patient and add it to the dict
                patients_dict[patient_id].add_test() #then add the test to that patient
            save_dictionary_to_file(patients_dict)
        elif choice == "2": #Update record
            patient_id=read_patient_id()
            if patient_id in patients_dict: #If the patient exist call the update method, else print patient not found
                patients_dict[patient_id].update_test()
            else:
                print("Patient not found !")
            save_dictionary_to_file(patients_dict)
        elif choice == "3": #Delete record
            patient_id=read_patient_id()
            if patient_id in patients_dict:  # If the patient exist call the delete method, else print patient not found
                patients_dict[patient_id].delete_test()
            else:
                print("Patient not found !")
            save_dictionary_to_file(patients_dict)
        elif choice == "4": #Add medical Test Info
            Test.add_medical_test()
        elif choice == "5": #Update existing medical test
            Test.update_medical_test()
        elif choice == "6": #Filter medical records according to critera
            filter_test_records(patients_dict)
        elif choice == "7": #Genearte a summary report performed on filtered medical records to criteria
            generate_sum_report(patients_dict)
        elif choice == "8": #Import from csv file
            patients_dict=import_from_csv(patients_dict)
            save_dictionary_to_file(patients_dict)
        elif choice == "9": #Export to csv file
            export_to_csv(patients_dict)
        elif choice == "10": #Exit Program
            print("Thanks for using our program, Goodbye!\n")
            return 0
        elif choice == "100": #Test case to print the whole dictionary used by us for testing
            for p in patients_dict:
                for r in patients_dict[p].patient_tests:
                    r.print_record()
        else:
            print("Please enter a valid choice")
main()
#======================================
#======== END OF CODE =================
#======================================