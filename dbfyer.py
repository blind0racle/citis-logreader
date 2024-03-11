def date_beautifier(input_string):

    pairs = [input_string[i:i+2] for i in range(0, len(input_string), 2)]
    numbers = [pair.zfill(2) for pair in pairs]

    num_3 = numbers[3]
    num_4 = numbers[4]
    num_5 = numbers[5]
    num_2 = numbers[2]
    num_1 = numbers[1]
    num_0 = '20' + numbers[0]

    # Format the numbers into the desired string format
    formatted_string = f"{num_3}:{num_4}:{num_5} {num_2}/{num_1}/{num_0}"

    # Print the formatted string
    return formatted_string
