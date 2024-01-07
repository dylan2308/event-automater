import datetime as dt

def is_valid_date(date_string):
    try:
        dt.datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False
        
def is_valid_time(time_string):
    try:
        # Attempt to create a time object from the time string
        dt.datetime.strptime(time_string, '%H:%M:%S')  # Adjust the format as needed
        return True  # Time is valid
    except ValueError:
        return False  # Time is invalid
    
def convert_date_format(date_input):
    # Convert input to datetime object
    date_object = dt.datetime.strptime(date_input, "%d/%m/%Y")
    
    # Convert the datetime object back to a string in the desired format
    converted_date = date_object.strftime("%Y-%m-%d")
    
    return converted_date