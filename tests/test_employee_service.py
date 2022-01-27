from json import JSONDecodeError

import pytest
from pydantic import ValidationError

from conf.employee_definition import Employee, EmployeeJson
from service.employee_service import get_employee_list, get_total_salary, EmployeeMapper


def test_get_employee_list_from_empty_file():
    with pytest.raises(JSONDecodeError):
        employee_list = get_employee_list('/test/employees-empty.json')


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


def test_incorrect_first_name_cases():
    _validate_incorrect_names('123', 'A1', '1B', 'A-B', '$Josh', '_Kerry', ' Space')


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
    employee_json = _get_employee_json(1, 'A', 2, 100)
    employee = employee_mapper.map(employee_json)

    assert employee.get_eid() == employee_json.get_id()
    assert employee.get_salary() == employee_json.get_salary()
    assert employee.get_first_name() == employee_json.get_first_name()
    assert not employee.has_manager()


def test_employee_mapper_cache():
    employee_mapper = EmployeeMapper()
    assert not len(employee_mapper.get_employee_list())

    employee_json1 = _get_employee_json(1, 'A', None, 100)
    employee_mapper.map(employee_json1)
    assert len(employee_mapper.get_employee_list()) == 1
    employee_mapper.map(employee_json1)
    assert len(employee_mapper.get_employee_list()) == 1

    employee_json2 = _get_employee_json(2, 'B', None, 100)
    employee_mapper.map(employee_json2)
    assert len(employee_mapper.get_employee_list()) == 2


def test_total_salary():
    employee_list = [Employee(1, 'A', 100), Employee(2, 'B', 200), Employee(3, 'C', 300)]
    assert get_total_salary(employee_list) == 600


def _validate_incorrect_names(*names):
    for first_name in names:
        with pytest.raises(ValueError) as value_error:
            employee_json = _get_employee_json(1, first_name, 1, 0)

        assert value_error.value.errors() == [
            {'loc': ('first_name',), 'msg': 'first_name must in [A-Za-z]', 'type': 'value_error'}
        ]


def _get_employee_json(a_id: int, a_first_name: str, a_manager: int, a_salary: int):
    return EmployeeJson(id=a_id, first_name=a_first_name, manager=a_manager, salary=a_salary)
