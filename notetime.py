import sys
from cli import run_cli
from gui import run_gui

if __name__ == "__main__":
    if "--gui" in sys.argv:
        run_gui()
    else:
        run_cli()
