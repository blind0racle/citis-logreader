from datetime import datetime
line_number = int(input("Enter the line number to read: "))

# Open the log file for reading
with open("demo.txt", "r") as file:
    # Read the file line by line
    for index, line in enumerate(file, start=1):
        if index == line_number:
            # Split the line into parts based on spaces
            parts = line.split()

            # Check if there are enough elements in the parts list
            status = "verified" if parts[0] == "V" else "revoked"
            date1_string = parts[1][:-1]
            if len(parts) == 6:
                # Extract the required information if there are enough elements
                date2_string = parts[2][:-1]
                cn = parts[5].split("=")[6].split("/")[0]
                email = parts[5].split("=")[8]
            else:
                date2 = "NS"
                cn = parts[4].split("=")[6].split("/")[0]
                email = parts[4].split("=")[8]

            date_format = "%y%m%d%H%M%S"
            date1 = datetime.strptime(date1_string, date_format).strftime("%y%m%d%H%M%S")
            date2 = datetime.strptime(date2_string, date_format).strftime(
                "%y%m%d%H%M%S") if date2_string != "NS" else "NS"

            print(f"Status: {status}, First date: {date1}, Second date: {date2}, CN: {cn}, Email: {email}")
            break
    else:
        print("Line number n  ot found in the log file.")


