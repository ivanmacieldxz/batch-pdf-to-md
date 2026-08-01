import sys

def main():
    # If arguments are provided (other than the script name itself), 
    # run the CLI interface.
    if len(sys.argv) > 1:
        from src import cli
        cli.main()
    else:
        # Otherwise, launch the modern GUI.
        from src import gui
        gui.main()

if __name__ == "__main__":
    main()
