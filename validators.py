def is_int(num):
    try:
        int(num)
        return True
    except ValueError:
        return False

def is_valid_input(num, options):
    if is_int(num):
        return True if int(num) in options else False
    return False