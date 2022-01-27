import glob
from json import JSONDecodeError

from pydantic import ValidationError

from service.employee_service import get_employee_list, print_employee_list
from utils import RESOURCES_DIR


def main():
    _print_file()


def _print_file():
    print('\nplease input one of the following stored in /resources path or press N to exit\n')

    json_files = glob.glob(RESOURCES_DIR + '/*.json')
    json_files.sort(key=lambda file_name: file_name)

    for index, file in enumerate(json_files):
        print(str(index + 1) + '. ' + file.replace(RESOURCES_DIR, ''))

    _print_separated_line()

    input_file_name = str(input())
    if input_file_name.upper() == 'N':
        _exit()

    print('\nstart generating report...\n')
    try:
        employee_list = get_employee_list(input_file_name)
        _print_separated_line()

        print_employee_list(employee_list)
        _print_separated_line()
    except FileNotFoundError:
        print(f"file not found: {input_file_name}\n")
        _print_file()
    except JSONDecodeError:
        print(f"the json file has wrong format: {input_file_name}\n")
        _print_file()
    except (ValueError, ValidationError) as error:
        print(f"something went wrong: {error}\n")
        _print_file()

    print(f"the above is {input_file_name} report\n")
    _proceed_with_printer()


def _print_separated_line():
    print('\n--------------------\n')


def _proceed_with_printer():
    print("continue ? Y/N")
    is_continue = str(input()).upper()
    if 'Y' == is_continue:
        print("********************")
        _print_file()
    elif 'N' == is_continue:
        _exit()
    else:
        _proceed_with_printer()


def _exit():
    print("bye bye")
    exit()


if __name__ == '__main__':
    main()
