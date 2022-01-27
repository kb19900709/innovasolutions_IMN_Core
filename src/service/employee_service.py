from typing import List

from conf.employee_definition import Employee, EmployeeJson, Manager
from utils import get_json_list_by_file


class EmployeeMapper:
    def __init__(self):
        self._employee_dict = {}

    def map_to_employee(self, employee_json: EmployeeJson) -> Employee:
        if not employee_json:
            raise ValueError('employee_json shouldn\'t be None')

        if employee_json.get_id() not in self._employee_dict:
            self._employee_dict[employee_json.get_id()] = Employee(
                employee_json.get_id()
                , employee_json.get_first_name()
                , employee_json.get_salary())

        return self._employee_dict[employee_json.get_id()]

    def map_to_manager(self, employee_json: EmployeeJson) -> Manager:
        if not employee_json:
            raise ValueError('employee_json shouldn\'t be None')

        if employee_json.get_id() not in self._employee_dict:
            self._employee_dict[employee_json.get_id()] = Manager(self.map_to_employee(employee_json))
            return self._employee_dict[employee_json.get_id()]

        employee = self._employee_dict[employee_json.get_id()]
        if type(employee) == Employee:
            manager = Manager(employee)
            self._employee_dict[employee_json.get_id()] = manager

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
        if employee_json.get_id() in employee_json_dict:
            raise ValueError(f"found duplicate id: {employee_json.get_id()}")
        employee_json_dict[employee_json.get_id()] = employee_json

    for employee_json in employee_json_dict.values():
        employee = employee_mapper.map_to_employee(employee_json)
        manager_id = employee_json.get_manager()
        if manager_id:
            if manager_id not in employee_json_dict:
                raise ValueError(f"can't find the manager with id: {manager_id}")

            manager = employee_mapper.map_to_manager(employee_json_dict[manager_id])
            employee.set_manager(manager)

    employee_list = employee_mapper.get_employee_list()
    employee_list.sort(key=lambda e: e.get_first_name())
    employee_list.sort(key=lambda e: type(e) == Manager, reverse=True)
    employee_list.sort(key=lambda e: e.has_manager())

    return employee_list


def print_employee_list(employee_list: List[Employee]):  # pragma: no cover
    if not employee_list:
        print('input employee list is empty')
        return

    for employee in employee_list:
        employee.print_info()
        print('----------')

    total_salary = get_total_salary(employee_list)
    print('\ntotal_salary = ' + str(total_salary))


def get_total_salary(employee_list: List[Employee]):
    return sum(employee.get_salary() for employee in employee_list if employee.get_salary())
