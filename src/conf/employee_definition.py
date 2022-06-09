import re
from abc import abstractmethod, ABC
from typing import List, Optional

from pydantic import BaseModel, validator

pattern = re.compile("[A-Za-z]+")


class EmployeeBase(ABC):
    """
    This abstract class defines some intrinsic fields, like `eid`, `first_name`. In general, all the employees will
    have these fields. The only abstract method is `print_info`.
    """

    def __init__(self, eid: int, first_name: str):
        self._eid = eid
        self._first_name = first_name

    def get_eid(self):
        return self._eid

    def get_first_name(self):
        return self._first_name

    @abstractmethod
    def print_info(self):  # pragma: no cover
        # just for printing object information, no need to take care about in coverage report
        pass

    def get_class_name(self):
        return type(self).__name__


class Employee(EmployeeBase):
    """
    This class extends `EmployeeBase` and has two more fields, `salary` and `manager`. If an employee has to set up
    a manager, invoke `set_manager` to bind the relation, `set_manager` will invoke `Manager.register(Employee)` as well
    . About `Manager.register(Employee)`, the input employee will be regarded as one of the members of the Manager.
    """

    def __init__(self, eid: int, first_name: str, salary: int):
        super(Employee, self).__init__(eid, first_name)
        self._salary = salary
        self._manager = None

    def get_salary(self):
        return self._salary

    def get_manager(self):
        return self._manager

    def set_manager(self, manager: 'Manager'):
        if not manager:
            raise ValueError('manager shouldn\'t be None')
        self._manager = manager
        manager.register(self)

    def has_manager(self):
        return self._manager is not None

    def print_info(self):  # pragma: no cover
        # just for printing object information, no need to take care about in coverage report
        print(self.get_first_name())


class Manager(Employee):
    """
    This class extends `Employee` and has one more field, `_member_list`. `register` allows to add the input
    `Employee` to be one of the members it has.
    """

    def __init__(self, employee: Employee):
        """
        Any new `Manager` must be created by an existing `Employee` instance. Pay attention on `has_manager` inspection
        here, if the input `Employee` has already had a `Manager`, the new `Manager` instance will invoke `set_manager`
        to the `Manager` from input `Employee` again.

        :param employee:  reference for the `Manager`
        """
        super().__init__(employee.get_eid(), employee.get_first_name(), employee.get_salary())
        self._member_list: List[Employee] = []

        if employee.has_manager():
            manager = employee.get_manager()
            self.set_manager(manager)

    def register(self, member: Employee):
        """
        Assume an `Employee` suddenly has a new identity, it has to manage a new member, so the `Employee` should be
        a `Manager`. But the new `Manager` might have a `Manager` already. During the construction time in `__init__`,
        the new `Manager` will invoke `set_manager`, then here comes a problem, **duplicate register** to the same
        `Manager`. To deal with this case, before the input `Employee` add to the `_member_list`, it'll scan the current
        `_member_list` to check if there's the same id exists in the list. If so, remove the instance. Lastly, the input
        `Employee` will be added to the `_member_list`.

        :param member: the input Employee is one of the members the manager has
        :return: None
        """

        for m in self._member_list:
            if m.get_eid() == member.get_eid():
                self._member_list.remove(m)
                break

        self._member_list.append(member)

    def get_member_list(self) -> List['Employee']:
        if self._member_list:
            # Based on the requirement, here will sort the members by their `first_name` before it returns
            self._member_list.sort(key=lambda e: e.get_first_name())

        return self._member_list

    def print_info(self):  # pragma: no cover
        # just for printing object information, no need to take care about in coverage report
        super().print_info()
        if self._member_list:
            print('Employees of ' + self.get_first_name())
            for member in self.get_member_list():
                print('\t' + member.get_first_name())


class EmployeeJson(BaseModel):
    """
    It implements pydantic. Most of the validations have been done by pydantic, like properties' name check, type check.
    For `manager` and `salary`, Optional[int] indicates that undefined property or null is allowed for the corresponding
    field. If we want to have advanced validation, take `first_name_must_be_english_letter` as your reference.
    """
    id: int
    first_name: str
    manager: Optional[int] = None
    salary: Optional[int] = None

    @validator('first_name')
    def first_name_must_be_english_letter(cls, v):
        """
        Assume the input value is able to match the pattern [A-Za-z], otherwise raise a `ValueError`.

        :param v: first_name
        :return: valid first_name
        """
        if pattern.fullmatch(v):
            return v
        raise ValueError('first_name must in [A-Za-z]')

    def get_id(self):
        return self.id

    def get_manager(self):
        return self.manager

    def get_first_name(self):
        return self.first_name

    def get_salary(self):
        return self.salary
