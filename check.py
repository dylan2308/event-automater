import datetime

def main():    
    startYear, startMth, startDay, startHr, startMin, startS = [0, 0, 0, 0, 0, 0]
    #endYear, endMth, endDay, endHr, endMin, endS = 0

    # Check valid year
    while startYear < 2024 and startYear > 2100:
        while True:
            try:
                startYear = int(input("Enter a valid start year: "))
                break
            except:
                continue
    # Check valid month i.e. between 1-12
    while startMth not in range(1, 13):
        while True:
            try:
                startMth = int(input("Enter a valid start month: "))
                break
            except:
                continue
    # Check months with 31 days
    if startMth in [1, 3, 5, 7, 8, 10, 12]:
        while startDay not in range(1, 32):
            while True:
                try:
                    startDay = int(input("Enter a valid start day: "))
                    break
                except:
                    continue
    # Check months with 30 days
    elif startMth in [4, 6, 9, 11]:
        while startDay not in range(1, 31):
            while True:
                try:
                    startDay = int(input("Enter a valid start day: "))
                    break
                except:
                    continue
    # Check February
    elif startMth == 2:
        # Leap years are divisible by 4
        if startYear % 4 == 0:
            while startDay not in range(1, 30):
                while True:
                    try:
                        startDay = int(input("Enter a valid start day: "))
                        break
                    except:
                        continue
        else:
            while startDay not in range(1, 29):
                while True:
                    try:
                        startDay = int(input("Enter a valid start day: "))
                        break
                    except:
                        continue
    
    dTime = datetime.datetime(int(startYear), int(startMth), int(startDay))
    print(f"Date chosen was: {dTime}")

if __name__ == "__main__":
    main()