from conf.employee_definition import EmployeeJson


def get_employee_json(a_id, a_first_name, a_manager, a_salary):
    return EmployeeJson(id=a_id, first_name=a_first_name, manager=a_manager, salary=a_salary)
