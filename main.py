from dbfyer import date_beautifier
def reader(line_number,path):
    with open(path, "r") as file:
        # Read the file line by line
        for index, line in enumerate(file, start=1):
            if index == line_number:
                # Split the line into parts based on spaces
                parts = line.split()

                # Check if there are enough elements in the parts list
                status = "verified" if parts[0] == "V" else "revoked"
                date1 = date_beautifier(parts[1][:-1])
                if len(parts) == 6:
                    # Extract the required information if there are enough elements
                    date2 = date_beautifier(parts[2][:-1])
                    cn = parts[5].split("=")[6].split("/")[0]
                    email = parts[5].split("=")[8]
                else:
                    date2 = "NS"
                    cn = parts[4].split("=")[6].split("/")[0]
                    email = parts[4].split("=")[8]
                return status, date1, date2, cn, email
        else:
            print("Line number not found in the log file.")
