from json import JSONDecodeError

import pytest
from pydantic import ValidationError

from src.conf.employee_definition import Employee, Manager
from src.service.employee_service import get_employee_list, get_total_salary, EmployeeMapper
from test_utils import get_employee_json


def test_get_employee_list_from_empty_file():
    with pytest.raises(JSONDecodeError):
        employee_list = get_employee_list('/test/employees-empty.json')


def test_get_employee_list_from_empty_array():
    employee_list = get_employee_list('/test/employees-empty-array.json')
    assert not employee_list


def test_get_employee_list_from_nonexistent_file():
    with pytest.raises(FileNotFoundError):
        employee_list = get_employee_list('/test/no_file.json')


def test_incorrect_json_file_with_wrong_type():
    with pytest.raises(ValidationError) as validation_error:
        get_employee_list('/test/employees-test-wrong-type.json')

    assert validation_error.value.errors() == [
        {'loc': ('salary',), 'msg': 'value is not a valid integer', 'type': 'type_error.integer'}
    ]


def test_incorrect_json_file_without_id():
    with pytest.raises(ValidationError) as validation_error:
        get_employee_list('/test/employees-test-no-id.json')

    assert validation_error.value.errors() == [
        {'loc': ('id',), 'msg': 'field required', 'type': 'value_error.missing'}
    ]


def test_incorrect_json_file_without_first_name():
    with pytest.raises(ValidationError) as validation_error:
        get_employee_list('/test/employees-test-no-first-name.json')

    assert validation_error.value.errors() == [
        {'loc': ('first_name',), 'msg': 'field required', 'type': 'value_error.missing'}
    ]


def test_incorrect_json_file_duplicate_id():
    with pytest.raises(ValueError, match='found duplicate id: 1'):
        get_employee_list('/test/employees-test-duplicate-id.json')


def test_incorrect_manager_not_found():
    with pytest.raises(ValueError, match='can\'t find the manager with id: 3'):
        get_employee_list('/test/employees-test-manager-not-found.json')


def test_get_employee_list_basic():
    employee_list = get_employee_list('/test/employees-test.json')
    assert len(employee_list) == 5
    assert employee_list[0].get_first_name() == 'Joy'
    assert employee_list[1].get_first_name() == 'Ted'
    assert employee_list[2].get_first_name() == 'David'
    assert employee_list[3].get_first_name() == 'Michael'
    assert employee_list[4].get_first_name() == 'Peter'

    # assume David and Michale don't have salary, they might be volunteers
    # in employees-test.json, David's salary is null, and Michale's salary is undefined
    assert get_total_salary(employee_list) == 1075000


def test_get_employee_list_members_relation_and_type():
    employee_list = get_employee_list('/test/employees-test.json')

    top_of_employee = employee_list[0]
    assert top_of_employee.get_first_name() == 'Joy'
    assert top_of_employee.get_class_name() == 'Manager'
    assert len(top_of_employee.get_member_list()) == 1

    second_of_employee = top_of_employee.get_member_list()[0]
    assert second_of_employee.get_first_name() == 'Ted'
    assert top_of_employee.get_class_name() == 'Manager'
    assert len(second_of_employee.get_member_list()) == 3

    assert second_of_employee.get_member_list()[0].get_first_name() == 'David'
    assert second_of_employee.get_member_list()[0].get_class_name() == 'Employee'

    assert second_of_employee.get_member_list()[1].get_first_name() == 'Michael'
    assert second_of_employee.get_member_list()[2].get_class_name() == 'Employee'

    assert second_of_employee.get_member_list()[2].get_first_name() == 'Peter'
    assert second_of_employee.get_member_list()[2].get_class_name() == 'Employee'


def test_employee_mapper_map_to_employee_set_none_as_mapper_input():
    with pytest.raises(ValueError, match='employee_json shouldn\'t be None'):
        employee_mapper = EmployeeMapper()
        employee_mapper.map_to_employee(None)


def test_employee_mapper_map_to_manager_set_none_as_mapper_input():
    with pytest.raises(ValueError, match='employee_json shouldn\'t be None'):
        employee_mapper = EmployeeMapper()
        employee_mapper.map_to_manager(None)


def test_employee_mapper_map_to_employee():
    employee_mapper = EmployeeMapper()
    employee_json = get_employee_json(1, 'A', 2, 100)
    employee = employee_mapper.map_to_employee(employee_json)

    assert employee.get_eid() == employee_json.get_id()
    assert employee.get_salary() == employee_json.get_salary()
    assert employee.get_first_name() == employee_json.get_first_name()
    assert not employee.has_manager()


def test_employee_mapper_cache_and_type_transfer():
    employee_mapper = EmployeeMapper()
    assert not len(employee_mapper.get_employee_list())

    employee_json1 = get_employee_json(1, 'A', 3, 100)
    employee_json2 = get_employee_json(2, 'B', 1, 100)
    employee_json3 = get_employee_json(3, 'C', None, 100)

    employee1 = employee_mapper.map_to_employee(employee_json1)
    assert len(employee_mapper.get_employee_list()) == 1

    manager_from_employee_json3 = employee_mapper.map_to_manager(employee_json3)
    assert len(employee_mapper.get_employee_list()) == 2
    employee1.set_manager(manager_from_employee_json3)

    employee2 = employee_mapper.map_to_employee(employee_json2)
    assert len(employee_mapper.get_employee_list()) == 3

    manager_from_employee_json1 = employee_mapper.map_to_manager(employee_json1)
    assert len(employee_mapper.get_employee_list()) == 3
    employee2.set_manager(manager_from_employee_json1)

    employee3 = employee_mapper.map_to_employee(employee_json3)
    assert len(employee_mapper.get_employee_list()) == 3

    employee_list = employee_mapper.get_employee_list()
    employee_list.sort(key=lambda e: e.get_eid())
    assert employee_list[0].get_class_name() == 'Manager'
    assert employee_list[1].get_class_name() == 'Employee'
    assert employee_list[2].get_class_name() == 'Manager'


def test_total_salary():
    employee_list = [Employee(1, 'A', 100), Employee(2, 'B', 200), Manager(Employee(3, 'C', 300))]
    assert get_total_salary(employee_list) == 600
