def yes_or_no(request):
    response = input(request + f" [Y/N]: \n")
    if response.lstrip().upper()[0] == "Y":
        return True
    else:
        return False

def multiple_chances(func, *args, **kwargs):
    while True:
        try:
            result = func(*args, **kwargs)
        except Exception as err:
            print(f"Unexpected error: {err}")
            if yes_or_no("Would you like to try again?"):
                continue
            else:
                return False
        return result