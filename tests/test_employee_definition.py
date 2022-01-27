import pytest
from pydantic import ValidationError

from conf.employee_definition import Employee, Manager
from test_utils import get_employee_json


def test_employee_set_none_as_manager():
    with pytest.raises(ValueError, match='manager shouldn\'t be None'):
        employee = Employee(1, 'A', 10)
        employee.set_manager(None)


def test_employee_get_member_list_with_five_members_and_sorted_by_name():
    manager = Manager(Employee(1, 'Allen', 100000))
    employee1 = Employee(2, 'Davis', 50000)
    employee2 = Employee(3, 'Eureka', 25000)
    employee3 = Employee(4, 'Bill', 12500)
    employee4 = Employee(5, 'Carter', 6250)
    employee5 = Employee(6, 'Fox', 3125)

    employee1.set_manager(manager)
    employee2.set_manager(manager)
    employee3.set_manager(manager)
    employee4.set_manager(manager)
    employee5.set_manager(manager)

    member_list = manager.get_member_list()

    assert len(member_list) == 5
    _validate_employee_and_manager_available(member_list[0], 4, 'Bill', 12500)
    _validate_employee_and_manager_available(member_list[1], 5, 'Carter', 6250)
    _validate_employee_and_manager_available(member_list[2], 2, 'Davis', 50000)
    _validate_employee_and_manager_available(member_list[3], 3, 'Eureka', 25000)
    _validate_employee_and_manager_available(member_list[4], 6, 'Fox', 3125)


def test_employee_json_with_none_id():
    with pytest.raises(ValidationError) as validation_error:
        get_employee_json(None, 'Allen', None, None)

    assert validation_error.value.errors() == [
        {'loc': ('id',), 'msg': 'none is not an allowed value', 'type': 'type_error.none.not_allowed'}
    ]


def test_incorrect_first_name_cases():
    _validate_incorrect_names('123', 'A1', '1B', 'A-B', '$Josh', '_Kerry', ' Space')


def test_employee_json_with_none_first_name():
    with pytest.raises(ValidationError) as validation_error:
        get_employee_json(1, None, None, None)

    assert validation_error.value.errors() == [
        {'loc': ('first_name',), 'msg': 'none is not an allowed value', 'type': 'type_error.none.not_allowed'}
    ]


def _validate_employee_and_manager_available(employee: Employee, eid: int, first_name: str, salary: int):
    assert employee.get_eid() == eid
    assert employee.get_first_name() == first_name
    assert employee.get_salary() == salary
    assert employee.has_manager()


def _validate_incorrect_names(*names):
    for first_name in names:
        with pytest.raises(ValueError) as value_error:
            employee_json = get_employee_json(1, first_name, 1, 0)

        assert value_error.value.errors() == [
            {'loc': ('first_name',), 'msg': 'first_name must in [A-Za-z]', 'type': 'value_error'}
        ]
