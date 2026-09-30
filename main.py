def show_help(arguments):
    print("Available commands:")
    print("  HELP    - Show available commands")
    print("  STATUS  - Show node status")
    print("  WX <area>  - Show weather for an area")
    print("  QUIT    - Exit the program")


def show_status(arguments):
    print("HawaiiMeshNode is online.")


def quit_program(arguments):
    print("Goodbye.")
    return False

def show_weather(arguments):
    if len(arguments) == 0:
        print("Usage: WX <region>")
        return

    region = arguments[0]

    if region == "OAHU":
        print("Oahu weather: placeholder data.")
    else:
        print(f"Weather region not found: {region}")

def run_command(command_line):
    commands = {
        "HELP": show_help,
        "STATUS": show_status,
        "WX": show_weather,
        "QUIT": quit_program,
    }

    parts = command_line.split()

    command = parts[0]
    arguments = parts[1:]

    action = commands.get(command)

    if action is None:
        print(f"Unknown command: {command}")
        return True

    result = action(arguments)

    if result is False:
        return False

    return True


def main():
    print("HawaiiMeshNode Development Console")
    print("Type HELP for available commands.")

    running = True

    while running:
        command_line = input("> ").strip().upper()

        if command_line == "":
            continue

        running = run_command(command_line)


if __name__ == "__main__":
    main()
