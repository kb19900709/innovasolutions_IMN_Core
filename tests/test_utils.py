from conf.employee_definition import EmployeeJson


def get_employee_json(a_id, a_first_name, a_manager, a_salary):
    """
    Get `EmployeeJson` instance

    :param a_id: employee id
    :param a_first_name: employee first_name
    :param a_manager: employee manager's id
    :param a_salary: employee salary
    :return:
    """
    return EmployeeJson(id=a_id, first_name=a_first_name, manager=a_manager, salary=a_salary)
