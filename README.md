# Time Table Management System
A web-based Time Table Management System built using the Django framework. This system is designed for managing lecture schedules, monitoring lecturer workloads, and applying for leave, with features to ensure smooth and efficient academic management.

## Features

- **Dynamic Time Table Management**:
  - Add and edit schedules with conflict resolution.
  - Color-coded schedule tiles for different years.
  - Interactive calendar view for better visualization.

- **Lecturer Workload Monitoring**:
  - Displays the total lecture hours for each lecturer.
  - Highlights lecturers exceeding the workload limit of 20 hours.

- **Leave Application System**:
  - Allows lecturers to apply for leave.
  - Displays available lecturers for replacement based on day and time slot.

- **User Management**:
  - Admin login for managing schedules and users.
  - user registration via the application.
  - User authentication with a limit on login attempts for security.
   
## Technologies Used

- **Backend**: Python, Django
- **Frontend**: HTML, CSS, Bootstrap
- **Version Control**: Git, GitHub

   ## Installation and Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/time-table-management-system.git
   
2.Create a virtual environment and activate it:
 ```bash
 python -m venv venv
 source venv/bin/activate  # For Linux/Mac
 venv\Scripts\activate
 ````

3.Install dependencies:
 ```bash
 pip install django
 ```

4.Apply migrations:
 ```bash
 py manage.py makemigrations
 py manage.py migrate
 ```
5.Run the development server:
 ```bash
 py manage.py runserver
 ```
## Admin Features
Manage schedules and monitor lecturer workloads via the admin panel.
Register and manage lecturers, halls, and subjects.
Apply for leave and view available lecturers for replacement.
Monitor personal workloads.


## Screenshots
<img width="1600" alt="Screenshot 2024-11-25 at 4 58 42 PM" src="https://github.com/user-attachments/assets/d5c00f97-75b0-4393-8569-73614cb9b3c7">
<img width="1600" alt="Screenshot 2024-11-25 at 4 58 18 PM" src="https://github.com/user-attachments/assets/52bfe2d6-f39f-4765-8cb0-5d6d0ad83bb8">


**Dashboard**
<img width="1600" alt="Screenshot 2024-11-25 at 4 58 54 PM" src="https://github.com/user-attachments/assets/1c04a958-6d33-4f21-8549-57bd4e3f038e">
<img width="1600" alt="Screenshot 2024-11-25 at 4 59 01 PM" src="https://github.com/user-attachments/assets/e62e7cbc-a785-43bc-bbf3-7baa604d01df">
<img width="1600" alt="Screenshot 2024-11-25 at 4 58 49 PM" src="https://github.com/user-attachments/assets/88515226-98bf-4b68-95aa-e7a64ba31487">


**Workload Monitoring**
<img width="1600" alt="Screenshot 2024-11-25 at 4 59 08 PM" src="https://github.com/user-attachments/assets/89cf5442-261a-4ded-8493-5a8bc9fff2e5">


**Apply Leave**
<img width="1600" alt="Screenshot 2024-11-25 at 4 59 04 PM" src="https://github.com/user-attachments/assets/b9e97152-5f27-4268-b48d-ec467dce6b40">

