from stix2validator import validate_file, print_results

if __name__ == "__main__":
    filepath = input(f"Please provide a filepath to the json: \n")
    results = validate_file(filepath)
    print_results(results)