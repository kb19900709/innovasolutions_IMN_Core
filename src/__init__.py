from service.employee_service import get_employee_list, print_employee_list


def main():
    employee_list = get_employee_list('employees.json')
    print_employee_list(employee_list)


if __name__ == '__main__':
    main()
  employee_list = get_employee_list('employees.json')