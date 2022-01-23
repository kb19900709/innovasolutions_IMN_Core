from typing import List


class EmployeeBase:
    def __init__(self, eid: int, first_name: str, salary: int):
        self._eid = eid
        self._first_name = first_name
        self._salary = salary

    def get_eid(self):
        return self._eid

    def get_first_name(self):
        return self._first_name

    def get_salary(self):
        return self._salary


class Employee(EmployeeBase):
    def __init__(self, eid: int, first_name: str, salary: int):
        super(Employee, self).__init__(eid, first_name, salary)
        self._manager = None
        self._member_list: List['Employee'] = []

    def get_member_list(self) -> List['Employee']:
        if self._member_list:
            self._member_list.sort(key=lambda e: e.get_first_name())

        return self._member_list

    def set_manager(self, manager: 'Employee'):
        if not manager:
            raise ValueError('manager shouldn\'t be None')

        self._manager = manager
        manager._register(self)

    def _register(self, member: 'Employee'):
        self._member_list.append(member)

    def has_manager(self):
        return self._manager is not None
