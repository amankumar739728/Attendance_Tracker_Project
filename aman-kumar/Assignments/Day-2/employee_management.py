class Employee:
    def __init__(self,empid,empname,domain,location):
        self.empid = empid
        self.empname = empname
        self.domain = domain
        self.location = location
        
    def to_dict(self):
        return {
            'empid': self.empid,
            'empname': self.empname,
            'domain': self.domain,
            'location': self.location
        }
    
    def display_info(self):
        return f"ID: {self.empid}, Name: {self.empname}, Domain: {self.domain}, Location: {self.location}"
        
        
class EmployeeManagement:
    def __init__(self):
        self.stored_employees = []
    
    def add_employee(self, employee):
        # Check if employee with same ID already exists
        for emp in self.stored_employees:
            if emp['empid'] == employee.empid:
                return f"Employee with ID {employee.empid} already exists!"
        
        # Add new employee dictionary to the list
        self.stored_employees.append(employee.to_dict())
        return f"Employee {employee.empname} added successfully!"
        
    def get_employee(self, empid):
        #Get employee by ID
        for emp in self.stored_employees:
            if emp['empid'] == empid:
                return emp
        return f"Employee with ID {empid} not found!"
        
    def update_employee(self, empid, key, value):
        #Update employee information
        for emp in self.stored_employees:
            if emp['empid'] == empid:
                if key in emp:
                    emp[key] = value
                    return f"Employee ID {empid} updated successfully!"
                else:
                    return f"Invalid key: {key}"
        return None
        
        
    def delete_employee(self, empid):
        #Delete an employee from the system
        for i, emp in enumerate(self.stored_employees):
            if emp['empid'] == empid:
                del self.stored_employees[i]
                return f"Employee with ID {empid} deleted successfully!"
        return f"Employee with ID {empid} not found!"
    
    def display_all_employees(self):
        #Display all employees in the system
        if not self.stored_employees:
            return []
        
        return self.stored_employees
            


if __name__ == "__main__":
    # Create the employee management system
    em = EmployeeManagement()
    
    # Add employees
    emp1 = Employee(1398, 'Aman Kumar', 'Data Analytics', 'Bangalore')
    emp2 = Employee(2471, 'Priya Sharma', 'Machine Learning', 'Hyderabad')
    emp3 = Employee(3562, 'Rahul Singh', 'Web Development', 'Delhi')
    
    print(em.add_employee(emp1))
    print(em.add_employee(emp2))
    print(em.add_employee(emp3))
    
    # Get an employee by ID
    empid = int(input("Enter employee EmpID: "))
    print(f"Employee with ID {empid}: {em.get_employee(empid)}")
    
    # Display all employees
    print("\nEmployee List:")
    employees = em.display_all_employees()
    print(employees)
    
    # Update an employee
    print(em.update_employee(1398, 'domain', 'Big Data'))
    
    # Display the updated employee list
    print("\nUpdated Employee List:")
    updated_employees = em.display_all_employees()
    print(updated_employees)
    
    # Delete an employee
    print(em.delete_employee(2471))
    
    # Display the final employee list
    print("\nFinal Employee List:")
    final_employees = em.display_all_employees()
    print(final_employees)
