# Asset Control System

## Project Description

The goal of this project is to develop a software solution for the company "Los Tres Patitos" to control and manage assets. The system will handle the administration of departments, employees, assets, and the processes of assigning and unassigning assets. It will also generate reports and ensure security through a login system.

## Requirements

1. **Login**
   - Login screen.
   - User validation via files.
   - Predefined administrator user and the ability to create new users.

2. **Main Interface (MDI)**
   - Main window to manage the various functionalities of the application.

3. **Main Menu**
   - Navigation between application windows through a main menu in the MDI.

4. **User Management Screen**
   - Manage users (CRUD).
   - Predefined administrator user.

5. **Employee Management Screen**
   - Manage employee information (CRUD).
   - Required information: ID number, name, surname, phone, address, position, hire date, and whether they are a manager.

6. **Department Management Screen**
   - Manage department information (CRUD).
   - Required information: code, name (unique), and manager (employee who can be a manager).

7. **Asset Management Screen**
   - Manage asset information (CRUD).
   - Required information: asset tag (format AA-1234), name, category, description, and status (Assignable, Exclusion, Repair).

8. **Asset Assignment Screen**
   - Assign assets to employees.
   - Only assets with status "Assignable" can be assigned.

9. **Asset Unassignment Screen**
   - Unassign assets from employees.
   - View and remove assigned assets.

10. **Reports**
    - **Assets Assigned to an Employee**: Report showing assets assigned to a selected employee.
    - **Assets That Cannot Be Assigned**: Report of assets with a status other than "Assignable".
    - **List of Employees by Department**: Report showing employees assigned to a selected department.
    - **Asset Status Chart**: Chart showing the number of assets in each status.
    - **Employees by Department Chart**: Chart showing the number of employees in each department.

11. **Data Storage**
    - Persistent data storage using files.

## Implementation

- **Object-Oriented Programming**: The solution will be developed using object-oriented programming principles.
- **Class Diagram**: A class diagram will be included in the documentation.

## Technical Requirements

- **Programming Language**: Python.
- **Development Environment**: VisualStudioCode, MongoDB.
- **Dependencies**: PyQt, matplotlib, pymongo.

## Installation and Usage

1. **Clone the Repository**
    ```bash
    git clone https://github.com/your-username/your-repository.git
    ```

2. **Install Dependencies**
    [Instructions for installing dependencies].

3. **Run the Application**
    [Instructions for running the application].

4. **Access the Application**
   

## License

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

