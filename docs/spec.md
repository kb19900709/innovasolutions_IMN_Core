## packages
| package | usage                                                                                  |
|---------|----------------------------------------------------------------------------------------|
| conf    | object definition, it's usually fixed and able to be utilized in other packages        |
| service | implementation of business requirements, associate with conf package to solve problems |

## modules
## utils
- get_json_list_by_file

Get json list from resource. It'll find the file from `/resources/` path by the input file name. If it goes wrong, it'll
return an empty list.

### conf.employee_definition
- EmployeeBase
- Employee

**EmployeeBase** defines some intrinsic attributes, like `id`, `first_name`, and `salary`. In general, all the employees will 
have these attributes. In terms of **Employee**, it extends **EmployeeBase** and has two additional attributes which are 
`manager` and `member_list`. If A is B's manager, then B has to set up the relation via `set_manager`. This function will 
also register B as one of A's members. Afterward, the result will be true if B invokes has_manager. Noticed that 
`get_member_list` will return members alphabetically.

### service.employee_service
- EmployeeJson
- EmployeeMapper
- get_employee_list
- print_employee_list
- get_total_salary

**EmployeeJson** is the data transfer object from json list loaded by `utils.get_json_list_by_file`.
<br/><br/>
**EmployeeMapper** aims to transfer **EmployeeJson** to **Employee**. There's an instance cache to save **Employee** by
its id. Regardless of how many times we map **EmployeeJson**, if the id exists in the cache, it'll return the same 
**Employee**. We can also get all the **Employee** created in that process by `EmployeeMapper.get_employee_list`.
<br/><br/>
**get_employee_list** is the main function of this module. It'll get json list by the input file name and transfer the list
to **Employee** from **EmployeeJson** by **EmployeeMapper** In the end, it'll sort the list by the following conditions
1. **Employee**.get_first_name
2. If the **Employee** has members, move to the top
3. If the **Employee** has no manager, move to the top

**print_employee_list** prints **Employee** list. Show the **Employee**'s name, if the **Employee** has members, it'll print 
each member's name as well.
<br/><br/>
**get_total_salary** sums the total salary from the input **Employee** list.