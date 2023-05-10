from ToSheetConverter import *
from Grabber import do_grabbing


def main():
    messages = do_grabbing()
    path_to_sheet = create_xlsx_without_authors(messages)
    print(path_to_sheet)


if __name__ == "__main__":
    main()
