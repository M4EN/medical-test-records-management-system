TESTSINFO="medicalTest.txt"
RECORDSINFO="medicalRecord.txt"
#===============
# ADD TEST FUNCTION
#===============
addTest () {
#Get the Record values from user
	echo "--> Adding a new medical test record"
	while true 
	do
		printf "Enter Patient ID: "
		read patientID
		printf "\n"
		if [[ ${#patientID} -eq 7 ]]  #Check if patient ID is valid
		then
			if ! echo "$patientID" | grep -q '[^0-9]'  #Check if the ID is made of numbers only
			then
				break   #Valid value, break the loop and go on
			else
			echo "PatientID Invalid, Please Enter a 7-Digit Integer"
			fi
		else
		echo "PatientID Invalid, Please Enter a 7-Digit Integer"
		fi
	done
	while true
	do
		printf "Enter Test Name:" #Check if test exists
		read testName
		printf "\n"
		if  grep -q "^Name: $testName;" "$TESTSINFO"
		then
		testUnit=$(grep "^Name: $testName;" "$TESTSINFO" | cut -d';' -f3 | cut -d':' -f2 | tr -d ' ')
		break
		else
		echo "Test was not found, Please enter a valid test name"
		fi
	done
	while true
	do
		printf "Enter Test Date:" #Check if Date Valid
		read testDate
		printf "\n"
		if [[ "$testDate" =~ ^[0-9]{4}-(0[0-9]|1[0-2])$ ]]
		then
			 break
		else
		echo "Invalid Date Format, Should be YYYY-MM"
		 fi
	done
	while true
	do
		printf "Enter Test Result:"
		read testResult
		printf "\n"
		if echo "$testResult" | grep -q '[^0-9.]' #Check if the Result has anything besides numbers or dots
			then
			echo "Result Invalid, Please Enter a valid float value"
			else
			numOfDots=$(echo "$testResult" | grep -o '\.' | wc -l)
			if [ "$numOfDots" -le 1 ]  #Check the number of dots, it should be less or equal to 1
				then
				break  #Valid value, break the loop an go on
				else
				echo "Result Invalid, Please Enter a valid float value"
			fi
		fi
	done
	while true
	do
	printf "Enter Test Status (p: Pending, c: Completed, r: Reviewed):"
	read testStatusChoice
	case "$testStatusChoice" in  #Choose status
	  p) testStatus=Pending
	  break;;
	  c) testStatus=Completed
	  break;;
	  r) testStatus=Reviewed
	  break;;
	  *) echo "Incorrect Input, Please enter one of the following  [ p / c / r ]" ;;
	esac
	printf "\n"
	done
	echo "Adding Record ..."
	echo "$patientID: $testName, $testDate, $testResult, $testUnit, $testStatus" >> "$RECORDSINFO"
	echo "Record added successfully !"
}
#===============
# DELETE TEST FUNCTION
#===============
deleteRecord () {
echo "--> Deleting a test Record"
while true 
	do
		printf "Enter Patient ID: "
		read patientID
		printf "\n"
		if [[ ${#patientID} -eq 7 ]]  #Check if patient ID is valid
		then
			if ! echo "$patientID" | grep -q '[^0-9]'  #Check if the ID is made of numbers only
			then
				break   #Valid value, break the loop and go on
			else
			echo "PatientID Invalid, Please Enter a 7-Digit Integer"
			fi
		else
		echo "PatientID Invalid, Please Enter a 7-Digit Integer"
		fi
	done
while true
	do
		printf "Enter Test Name:" #Check if test exists
		read testName
		printf "\n"
		if  grep -q "^Name: $testName;" "$TESTSINFO"
		then
		break
		else
		echo "Test was not found, Please enter a valid test name"
		fi
	done
isFound=$(grep "^$patientID: $testName" "$RECORDSINFO")
if [ -n "$isFound" ]
then
sed -i "/^$patientID: $testName/d" "$RECORDSINFO"
echo "--> Record deleted successfully"
else
echo "--> Test record not found"
fi
}
#===============
# UPDATE TEST FUNCTION
#===============
updateRecord () {
echo "--> Updating a test Result"
while true 
	do
		printf "Enter Patient ID: "
		read patientID
		printf "\n"
		if [[ ${#patientID} -eq 7 ]]  #Check if patient ID is valid
		then
			if ! echo "$patientID" | grep -q '[^0-9]'  #Check if the ID is made of numbers only
			then
				break   #Valid value, break the loop and go on
			else
			echo "PatientID Invalid, Please Enter a 7-Digit Integer"
			fi
		else
		echo "PatientID Invalid, Please Enter a 7-Digit Integer"
		fi
	done
while true
	do
		printf "Enter Test Name:" #Check if test exists
		read testName
		printf "\n"
		if  grep -q "^Name: $testName;" "$TESTSINFO"
		then
		testUnit=$(grep "^Name: $testName;" "$TESTSINFO" | cut -d';' -f3 | cut -d':' -f2 | tr -d ' ')
		break
		else
		echo "Test was not found, Please enter a valid test name"
		fi
	done
isFound=$(grep "^$patientID: $testName" "$RECORDSINFO")
if [ -n "$isFound" ]
then
testDate=$(echo "$isFound" | cut -d',' -f2 | tr -d ' ')
sed -i "/^$patientID: $testName/d" "$RECORDSINFO"
while true
	do
		printf "Enter the test's new result:"
		read testResult
		printf "\n"
		if echo "$testResult" | grep -q '[^0-9.]' #Check if the Result has anything besides numbers or dots
			then
			echo "Result Invalid, Please Enter a valid float value"
			else
			numOfDots=$(echo "$testResult" | grep -o '\.' | wc -l)
			if [ "$numOfDots" -le 1 ]  #Check the number of dots, it should be less or equal to 1
				then
				break  #Valid value, break the loop an go on
				else
				echo "Result Invalid, Please Enter a valid float value"
			fi
		fi
	done
	while true
	do
	printf "Enter the Test's new Status (p: pending, c: completed, r: reviewed):"
	read testStatusChoice
	case "$testStatusChoice" in  
	  p) testStatus=Pending
	  break;;
	  c) testStatus=Completed
	  break;;
	  r) testStatus=Reviewed
	  break;;
	  *) echo "Incorrect Input, Please enter one of the following  [ p / c / r ]" ;;
	esac
	printf "\n"
	done
	echo "Updated Record-> $patientID: $testName, $testDate, $testResult, $testUnit, $testStatus"
	echo "$patientID: $testName, $testDate, $testResult, $testUnit, $testStatus" >> "$RECORDSINFO"
	echo "--> Record updated successfully"
	else
	echo "--> Test record not found"
	fi
}
#===============
# SEARCH FUNCTION
#===============
searchRecord () { #Function search record by patient ID
echo "--> Search for a Test by Patient ID"
printf "Enter Patient ID: "
read patientID
printf "\n"
if [[ ${#patientID} -eq 7 ]] && ! echo "$patientID" | grep -q '[^0-9]'
	then
	while true #Print Search Menu
	do
	echo "Select an option:"
	echo "1. Retrieve all patient tests"
	echo "2. Retrieve all abnormal patient tests"
	echo "3. Retrieve all patient tests in a specific period"
	echo "4. Retrieve all patient tests based on test status"
	printf "Enter Option number: "
	read option
	printf "\n"
	case $option in
	1) # Retrieve all patient's tests
		echo "--> Retrieving all tests for Patient ID: $patientID"
		results=$(grep "^$patientID:" "$RECORDSINFO")
		if [ -z "$results" ]; then
			echo "No tests found for Patient ID: $patientID"
		else
			echo "$results"
		fi
		;;
	2) #Retrieve all abnormal patient's tests
		echo "--> Retrieving all abnormal tests for Patient ID: $patientID"
		lines=$(grep "$patientID" "$RECORDSINFO")
		isFoundAB=0
		for line in $(echo "$lines" | cut -d: -f2 | tr -d ' ') #Check line by line for result and check it with its range
			do
			test_name=$(echo "$line" | cut -d, -f1 | tr -d ' ')
			result=$(echo "$line" | cut -d, -f3 | tr -d ' ')
			testLine=$(grep "$test_name" "$TESTSINFO")
			if echo "$testLine" | grep -q '>' && echo "$testLine" | grep -q '<'
			then #when we have min and max
			min=$(echo "$testLine" | grep -o 'Range: > [0-9.]*' | cut -d' ' -f3)
			max=$(echo "$testLine" | cut -d'<' -f2 | cut -d';' -f1 | tr -d ' ')
			ismax=$(echo "$result > $max" | bc -l)
			ismin=$(echo "$result < $min" | bc -l)
			if [ "$ismax" -eq 1 -o "$ismin" -eq 1 ]
			then
			echo "$line"
			isFoundAB=1
			else
			:
			fi
			elif echo "$testLine" | grep -q '<' 
			then #When we have max only
			max=$(echo "$testLine" | grep -o 'Range: < [0-9.]*' | cut -d' ' -f3)
			ismax=$(echo "$result > $max" | bc -l)
			if [ "$ismax" -eq 1 ]
			then
			echo "$line"
			isFoundAB=1
			else
			:
			fi
			elif echo "$testLine" | grep -q '>'
			then #When we have min only
			min=$(echo "$testLine" | grep -o 'Range: > [0-9.]*' | cut -d' ' -f3)
			ismin=$(echo "$result < $min" | bc -l)
			if [ "$ismin" -eq 1 ]
			then
			echo "$line"
			isFoundAB=1
			else
			:
			fi
			else
			echo "Error can't find the range of $test_name, make sure the test info is in correct format"
			fi
			if [ "$isFoundAB" -eq 0 ]
			then
			echo "No abnormal tests were found!"
			fi
			done
		;;
	3) #Retrieve Patient's test based on a specific date period
		while true
			do
			printf "Enter Start Date (YYYY-MM): "
			read startDate
			printf "Enter End Date (YYYY-MM): "
			read endDate
			printf "\n"
			if [[ "$startDate" =~ ^[0-9]{4}-(0[1-9]|1[0-2])$ ]] && [[ "$endDate" =~ ^[0-9]{4}-(0[1-9]|1[0-2])$ ]]
			then
			flagFound=0
			if [[ "$startDate" > "$endDate" ]]
			then
			echo "ERROR - Start Date cant be later than end date."
			else
			break
			fi
			else
			echo "ERROR - Dates must be in the format YYYY-MM and month must be between 01 and 12. Please enter the dates again."
			fi
			done
		echo "--> Retrieving all tests for Patient ID: $patientID between $startDate and $endDate"
		lines=$(grep "$patientID" "$RECORDSINFO")
		for line in $(echo "$lines" | tr -d ' ')
			do
			testDates=$(echo "$line" | cut -d, -f2)
			if [[ "$testDates" < "$endDate" && "$testDates" > "$startDate" ]] #If test is before  end date check if its later than start date if its both before end date and later than 	start date then condition is true
			then
			echo "$line" #Print the test info
			flagFound=1
			elif [[ "$testDates" == "$startDate" ]] #If is not between the dates check If the test date is equal to start date then its in range
			then
			echo "$line" #Print the test info
			flagFound=1
			elif [[ "$testDates" == "$endDate" ]] #If its not equal to start date check If the test date is equal to end date then its in range
			then
			echo "$line" #Print the test info
			flagFound=1
			else #If its not in between and not equal to start or end then its out of range and do nothing
			:
			fi
			done
		if [ "$flagFound" -eq 0 ]
			then
			echo "No tests found in this date period"
			fi
		;;
	4) #Retrieve all patient tests based on status
		while true
			do
			printf "Enter Test Status (p: pending, c: completed, r: reviewed):"
			read testStatusChoice
			echo "$testStatusChoice"
			case "$testStatusChoice" in  
			p) testStatus=Pending
			break;;
			c) testStatus=Completed
			break;;
			r) testStatus=Reviewed
			break;;
			*) echo "Incorrect Input, Please enter one of the following  [ p / c / r ]" ;;
			esac
			printf "\n"
			done
		echo "--> Retrieving all tests with status '$testStatus' for Patient ID: $patientID"
		statusTests=$(grep "^$patientID:" "$RECORDSINFO" | grep  "$testStatus")
		if [ -z "$statusTests" ]; then
		echo "No tests with status '$testStatus' found for Patient ID: $patientID"
		else
		echo "$statusTests"
		fi
		;;
	*) #Default case, if user enters unexpected
		echo "Invalid option, please choose a valid option."
		;;
		esac
		break
		done
		else
		echo "PatientID Invalid, Please Enter a 7-Digit Integer"
		fi
	}
#================
# SEARCH ABNORMAL RESULTS FUNCTION
#================
searchAbnormalTests () {
echo "--> Retrieving all abnormal tests. "
isFoundABT=0
ineveryline=" "
lines=$(grep "$ineveryline" "$RECORDSINFO")
	for line in $(echo "$lines" |  tr -d ' ')
		do
		id=$(echo "$line" | cut -d: -f1)
		line=$(echo "$line" | cut -d: -f2)
		test_name=$(echo "$line" | cut -d, -f1 |tr -d ' ')
		result=$(echo "$line" | cut -d, -f3 | tr -d ' ')
		testLine=$(grep "$test_name" "$TESTSINFO")
		if echo "$testLine" | grep -q '>' && echo "$testLine" | grep -q '<'
		then #when we have min and max
		min=$(echo "$testLine" | grep -o 'Range: > [0-9.]*' | cut -d' ' -f3)
		max=$(echo "$testLine" | cut -d'<' -f2 | cut -d';' -f1 | tr -d ' ')
			ismax=$(echo "$result > $max" | bc -l)
		ismin=$(echo "$result < $min" | bc -l)
		if [ "$ismax" -eq 1 -o "$ismin" -eq 1 ]
		then
		echo "$id: $line"
		isFoundABT=1
		else
		:
		fi
		elif echo "$testLine" | grep -q '<' 
		then #When we have max only
		max=$(echo "$testLine" | grep -o 'Range: < [0-9.]*' | cut -d' ' -f3)
		ismax=$(echo "$result > $max" | bc -l)
		if [ "$ismax" -eq 1 ]
		then
		echo "$id: $line"
		isFoundABT=1
		else
		:
		fi
		elif echo "$testLine" | grep -q '>'
		then #When we have min only
		min=$(echo "$testLine" | grep -o 'Range: > [0-9.]*' | cut -d' ' -f3)
		ismin=$(echo "$result < $min" | bc -l)
		if [ "$ismin" -eq 1 ]
		then
		echo "$id: $line"
		isFoundABT=1
		else
		:
		fi
		else
		echo "Error can't find the range of $test_name, make sure the test info is in correct format"
		fi
		done
}
#=================
# AVERAGE VALUE FUNCTION
#=================
averageTestValue() {
while true
do
printf "Enter Test Name:" #Check if test exists
read testName
printf "\n"
	if  grep -q "^Name: $testName;" "$TESTSINFO"
	then
	:
	break
	else
	echo "Test was not found, Please enter a valid test name"
	fi
done
lines=$(grep "$testName" "$RECORDSINFO" | wc -l)
sum=0
for line in $(grep "$testName" "$RECORDSINFO" | cut -d, -f3 | tr -d ' ')
do
add=$line
sum=$(echo "scale=2; $sum + $add" | bc) #We used scale to select how many digits after the . to be shown
done
	if [[ $lines -ne 0 ]]
	then
	avg=$(echo "scale=2; $sum / $lines" | bc)
	echo "Average value of $testName Results is $avg"
	else
	echo "No lines containing $testName found."
	fi
}
#======================================================
# Program Main Code
#======================================================
# Initilizaing Files
echo ""
echo "Initilizaing Test Files.."
#Create medicalTest.txt
if [ -f "$TESTSINFO" ]
then
:
else
touch "$TESTSINFO"
fi
# Fill medicalTest.txt
echo "Name: HGB; Range: > 13.8, < 17.2; Unit: g/dL" > "$TESTSINFO"
echo "Name: BGT; Range: > 70, < 99; Unit: mg/dL" >> "$TESTSINFO"
echo "Name: LDL; Range: < 100; Unit: mg/dL" >> "$TESTSINFO"
echo "Name: Systole; Range: < 120; Unit: mm Hg" >> "$TESTSINFO"
echo "Name: Diastole; Range: < 80; Unit: mm Hg" >> "$TESTSINFO"
#Create medicalRecord.txt
if [ -f "$RECORDSINFO" ]
then
:
else
touch "$RECORDSINFO"
fi
echo "-->Files ready"
echo ""
# Program Main Menu Code
while true
do
	echo ""
	echo "============================="
	echo "========= MAIN MENU ========="
	echo "============================="
	echo "1- Add new medical test record"
	echo "2- Search for a test by patient ID"
	echo "3- Search for abnormal tests"
	echo "4- Update an existing test result"
	echo "5- Delete a test"
	echo "6- Retrieve average test value based on test name"
	echo "7- Exit program"
	echo "Please choose the operation you want to perform using the operation number."
	printf "Enter choice:"
	read choice
	echo ""
	case "$choice" in
		1) addTest ;;  #Call functions
		2) searchRecord ;;
		3) searchAbnormalTests ;;
		4) updateRecord ;;
		5) deleteRecord ;;
		6) averageTestValue ;;
		7)
		echo "Thanks for using our program, Goodbye :)"
		exit ;;  #Exit Program
		*) echo "Incorrect Input, Please choose the operation by writing the operation number(1-7):"
	esac
done
# ======================================
# =========== END OF CODE ==============
# ======================================
