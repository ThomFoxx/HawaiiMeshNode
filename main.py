from commands.help import show_help
from commands.status import show_status
from commands.weather import show_weather
from commands.admin import show_popular_zips

def quit_program(arguments):
    print("Goodbye.")
    return False

def run_command(command_line):
    commands = {
    "HELP": show_help,
    "STATUS": show_status,
    "WX": show_weather,
    "ZIPS": show_popular_zips,
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
