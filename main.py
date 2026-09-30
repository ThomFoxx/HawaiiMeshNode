def show_help():
    print("Available commands:")
    print("  HELP    - Show available commands")
    print("  STATUS  - Show node status")
    print("  QUIT    - Exit the program")


def show_status():
    print("HawaiiMeshNode is online.")


def quit_program():
    print("Goodbye.")
    return False


def run_command(command):
    commands = {
        "HELP": show_help,
        "STATUS": show_status,
        "QUIT": quit_program,
    }

    action = commands.get(command)

    if action is None:
        print(f"Unknown command: {command}")
        return True

    result = action()

    if result is False:
        return False

    return True


def main():
    print("HawaiiMeshNode Development Console")
    print("Type HELP for available commands.")

    running = True

    while running:
        command = input("> ").strip().upper()

        if command == "":
            continue

        running = run_command(command)


if __name__ == "__main__":
    main()
