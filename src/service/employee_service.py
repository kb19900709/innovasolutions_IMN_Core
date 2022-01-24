from typing import List

from conf.employee_definition import Employee
from utils import get_json_list_by_file


class EmployeeJson(object):
    def __init__(self, id: int, first_name: str, manager: int, salary: int):
        self.id = id
        self.first_name = first_name
        self.manager = manager
        self.salary = salary

    def get_id(self):
        return self.id

    def get_manager(self):
        return self.manager

    def get_first_name(self):
        return self.first_name

    def get_salary(self):
        return self.salary


class EmployeeMapper:
    def __init__(self):
        self._employee_dict = {}

    def map(self, employee_json: EmployeeJson) -> Employee:
        if not employee_json:
            raise ValueError('employee_json shouldn\'t be None')

        if not self._employee_dict.get(employee_json.get_id()):
            self._employee_dict[employee_json.get_id()] = Employee(
                employee_json.get_id()
                , employee_json.get_first_name()
                , employee_json.get_salary())

        return self._employee_dict[employee_json.get_id()]

    def get_employee_list(self) -> List[Employee]:
        if self._employee_dict:
            return list(self._employee_dict.values())

        return []


def get_employee_list(file_name: str) -> List[Employee]:
    employee_json_list = get_json_list_by_file(file_name)
    if not employee_json_list:
        return []

    employee_json_dict = {}
    employee_mapper = EmployeeMapper()

    for employee_json_data in employee_json_list:
        employee_json = EmployeeJson(**employee_json_data)
        employee_json_dict[employee_json.get_id()] = employee_json

    for employee_json in employee_json_dict.values():
        employee = employee_mapper.map(employee_json)
        manager_id = employee_json.get_manager()
        if manager_id:
            manager = employee_mapper.map(employee_json_dict[manager_id])
            employee.set_manager(manager)

    employee_list = employee_mapper.get_employee_list()

    if employee_list:
        _sort_employee_list(employee_list)
        return employee_list

    return []


def _sort_employee_list(employee_list):
    employee_list.sort(key=lambda e: e.get_first_name())
    employee_list.sort(key=lambda e: len(e.get_member_list()), reverse=True)
    employee_list.sort(key=lambda e: e.has_manager())


def print_employee_list(employee_list: List[Employee]):
    if not employee_list:
        return

    for employee in employee_list:
        print_employee(employee)

    total_salary = sum(employee.get_salary() for employee in employee_list)
    print('')
    print('total_salary = ' + str(total_salary))


def print_employee(employee: Employee):
    print(employee.get_first_name())
    if employee.get_member_list():
        print('Employees of ' + employee.get_first_name())
        member_list = employee.get_member_list()
        for member in member_list:
            print('\t' + member.get_first_name())
        print('')
