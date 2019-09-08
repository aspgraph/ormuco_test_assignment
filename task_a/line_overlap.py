

# Check if two line segments overlap on the x-axis
# Two line segments overlap, if their most-left and most-right points are in between each other
def check_overlapping(x1, x2, x3, x4):
    return max(x1, x2) >= min(x3, x4) and min(x1, x2) <= max(x3, x4)


# Program entry point
if __name__ == '__main__':
    while True:
        # Reading user input
        user_input = raw_input()
        if user_input == 'stop':
            break
        try:
            # Trying to unpack user input into 4 potentially long numbers
            x11, x12, x21, x22 = [long(num) for num in user_input.split(",")]
        except ValueError:
            # Failure
            print 'Wrong format! should be 4 numbers separated by a comma, e.g. "x1,x2,x3,x4", "stop", or "run_tests".'
        else:
            # Success
            print check_overlapping(x11, x12, x21, x22)

    print 'Stopped'
