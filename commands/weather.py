def show_weather(arguments):
    if len(arguments) == 0:
        print("Usage: WX <region>")
        return

    region = arguments[0]

    if region == "OAHU":
        print("Oahu weather: placeholder data.")
    else:
        print(f"Weather region not found: {region}")