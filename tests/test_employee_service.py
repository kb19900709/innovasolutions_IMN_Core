import pytest

from conf.employee_definition import Employee
from service.employee_service import get_employee_list, get_total_salary, EmployeeJson, EmployeeMapper


def test_get_employee_list_from_empty_file():
    employee_list = get_employee_list('/test/employees-empty.json')
    assert not employee_list


def test_get_employee_list_basic():
    employee_list = get_employee_list('/test/employees-test.json')
    assert len(employee_list) == 5
    assert employee_list[0].get_first_name() == 'Joy'
    assert employee_list[1].get_first_name() == 'Ted'
    assert employee_list[2].get_first_name() == 'David'
    assert employee_list[3].get_first_name() == 'Michael'
    assert employee_list[4].get_first_name() == 'Peter'
    assert get_total_salary(employee_list) == 1093750


def test_get_employee_list_members_relation():
    employee_list = get_employee_list('/test/employees-test.json')

    top_of_employee = employee_list[0]
    assert top_of_employee.get_first_name() == 'Joy'
    assert len(top_of_employee.get_member_list()) == 1

    second_of_employee = top_of_employee.get_member_list()[0]
    assert second_of_employee.get_first_name() == 'Ted'
    assert len(second_of_employee.get_member_list()) == 3
    assert second_of_employee.get_member_list()[0].get_first_name() == 'David'
    assert second_of_employee.get_member_list()[1].get_first_name() == 'Michael'
    assert second_of_employee.get_member_list()[2].get_first_name() == 'Peter'


def test_employee_mapper_set_none_as_mapper_input():
    with pytest.raises(ValueError, match='employee_json shouldn\'t be None'):
        employee_mapper = EmployeeMapper()
        employee_mapper.map(None)


def test_employee_mapper_map_to_employee():
    employee_mapper = EmployeeMapper()
    employee_json = EmployeeJson(1, 'A', 2, 100)
    employee = employee_mapper.map(employee_json)

    assert employee.get_eid() == employee_json.get_id()
    assert employee.get_salary() == employee_json.get_salary()
    assert employee.get_first_name() == employee_json.get_first_name()
    assert not employee.has_manager()


def test_employee_mapper_cache():
    employee_mapper = EmployeeMapper()
    assert not len(employee_mapper.get_employee_list())

    employee_json1 = EmployeeJson(1, 'A', None, 100)
    employee_mapper.map(employee_json1)
    assert len(employee_mapper.get_employee_list()) == 1
    employee_mapper.map(employee_json1)
    assert len(employee_mapper.get_employee_list()) == 1

    employee_json2 = EmployeeJson(2, 'B', None, 100)
    employee_mapper.map(employee_json2)
    assert len(employee_mapper.get_employee_list()) == 2


def test_total_salary():
    employee_list = [Employee(1, 'A', 100), Employee(2, 'B', 200), Employee(3, 'C', 300)]
    assert get_total_salary(employee_list) == 600

