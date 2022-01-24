import pytest

from conf.employee_definition import Employee


def test_employee_get_member_list_with_no_one():
    employee = Employee(1, 'A', 10)
    assert len(employee.get_member_list()) == 0


def test_employee_set_none_as_manager():
    with pytest.raises(ValueError, match='manager shouldn\'t be None'):
        employee = Employee(1, 'A', 10)
        employee.set_manager(None)


def test_employee_get_member_list_with_five_members_and_sorted_by_name():
    manager = Employee(1, 'Allen', 100000)
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
    validate_employee_with_manager_available(member_list[0], 4, 'Bill', 12500)
    validate_employee_with_manager_available(member_list[1], 5, 'Carter', 6250)
    validate_employee_with_manager_available(member_list[2], 2, 'Davis', 50000)
    validate_employee_with_manager_available(member_list[3], 3, 'Eureka', 25000)
    validate_employee_with_manager_available(member_list[4], 6, 'Fox', 3125)


def validate_employee_with_manager_available(employee: Employee, eid: int, first_name: str, salary: int):
    assert employee.get_eid() == eid
    assert employee.get_first_name() == first_name
    assert employee.get_salary() == salary
    assert employee.has_manager()
