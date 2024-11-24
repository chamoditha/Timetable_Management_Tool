from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from timetable.models import Schedule, TimeSlot, Year, Subject, Hall, Lecturer
from .forms import ScheduleForm
from django.db import IntegrityError
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib import messages

def login_view(request):
    error = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_superuser:  # Check if the user is a superuser
                login(request, user)
                return redirect('dashboard')  # Redirect to the dashboard
            else:
                error = "Only superusers are allowed to log in."
        else:
            error = "Invalid username or password."

    return render(request, 'login.html', {'error': error})



def dashboard_view(request):
    # Fetch all required data
    lecturers = Lecturer.objects.all()  # Get all lecturers
    time_slots = TimeSlot.objects.all()
    years = Year.objects.all()
    subjects = Subject.objects.all()
    halls = Hall.objects.all()
    schedules = Schedule.objects.all().order_by('year__name', 'timeslot__start_time')
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

    context = {
        'lecturers': lecturers,  # Pass lecturers to the template
        'time_slots': time_slots,
        'years': years,
        'subjects': subjects,
        'halls': halls,
        'schedules': schedules,
        'days': days,
    }
    return render(request, 'dashboard.html', context)

   



def get_date_from_day(day_name):
    today = datetime.now()
    days_map = {
        "Monday": 0,
        "Tuesday": 1,
        "Wednesday": 2,
        "Thursday": 3,
        "Friday": 4,
    }
    # Find the next occurrence of the selected day
    target_day = days_map[day_name]
    days_ahead = (target_day - today.weekday() + 7) % 7
    return today + timedelta(days=days_ahead)



def add_schedule(request):
    if request.method == 'POST':
        day = request.POST.get('day')
        timeslot_id = request.POST.get('timeslot')
        year_id = request.POST.get('year')
        subject_id = request.POST.get('subject')
        hall_id = request.POST.get('hall')
        lecturer_id = request.POST.get('lecturer')

        try:
            # Attempt to save the schedule
            Schedule.objects.create(
                day=day,
                timeslot_id=timeslot_id,
                year_id=year_id,
                subject_id=subject_id,
                hall_id=hall_id,
                lecturer_id=lecturer_id,
            )
            return redirect('dashboard')  # Redirect to dashboard if successful
        except IntegrityError as e:
            # Handle the unique constraint violation
            error_message = "The selected year already has a lecture at this time.: "
            if 'unique_schedule_per_timeslot' in str(e):
                error_message += "The selected year already has a lecture at this time."
            elif 'unique_lecturer_per_timeslot' in str(e):
                error_message += "The selected lecturer is already teaching another lecture at this time."
            elif 'unique_hall_per_timeslot' in str(e):
                error_message += "The selected hall is already being used for another lecture at this time."
            else:
                error_message += ""

            # Re-render the dashboard with an error message
            return render(request, 'dashboard.html', {
                'error': error_message,
                'days': ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
                'time_slots': TimeSlot.objects.all(),
                'years': Year.objects.all(),
                'subjects': Subject.objects.all(),
                'halls': Hall.objects.all(),
                'lecturers': Lecturer.objects.all(),
                'schedules': Schedule.objects.all(),
            })

def edit_schedule(request):
    if request.method == 'POST':
        schedule_id = request.POST.get('schedule_id')
        schedule = get_object_or_404(Schedule, id=schedule_id)

        # Get new values from the form
        new_subject_id = request.POST.get('subject')
        new_hall_id = request.POST.get('hall')
        new_lecturer_id = request.POST.get('lecturer')

        # Validate conflicts
        day = schedule.day
        timeslot = schedule.timeslot

        # Check if the hall is already assigned
        hall_conflict = Schedule.objects.filter(
            day=day, timeslot=timeslot, hall_id=new_hall_id
        ).exclude(id=schedule_id).exists()

        if hall_conflict:
            messages.error(request, "This hall is already assigned to another lecture in the same time slot.")
            return redirect('dashboard')

        # Check if the lecturer is already assigned
        lecturer_conflict = Schedule.objects.filter(
            day=day, timeslot=timeslot, lecturer_id=new_lecturer_id
        ).exclude(id=schedule_id).exists()

        if lecturer_conflict:
            messages.error(request, "This lecturer is already assigned to another lecture in the same time slot.")
            return redirect('dashboard')

        # Save changes if no conflicts
        schedule.subject_id = new_subject_id
        schedule.hall_id = new_hall_id
        schedule.lecturer_id = new_lecturer_id
        schedule.save()

        messages.success(request, "Schedule updated successfully!")

    return redirect('dashboard')


def register_view(request):
    error = None
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # Check for validation errors
        if password != password2:
            error = "Passwords do not match."
        elif len(password) < 6:
            error = "Password must be at least 6 characters long."
        elif User.objects.filter(username=username).exists():
            error = "Username already exists."
        elif User.objects.filter(email=email).exists():
            error = "Email already exists."
        else:
            # Create the superuser
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            return redirect('login')  # Redirect to login after successful registration

    return render(request, 'register.html', {'error': error})

def logout_view(request):
    """
    Logs out the user and redirects to the login page.
    """
    logout(request)  # Log out the user
    return redirect('/')  # Redirect to the login page

def example_view(request):
    # Some logic here
    messages.success(request, "Your action was successful!")
    messages.error(request, "Something went wrong.")
    return redirect('dashboard')

def workload_monitoring(request):
    # Logic for workload monitoring goes here
    return render(request, 'workload_monitoring.html')

def workload_monitoring(request):
    # Fetch all lecturers
    lecturers = Lecturer.objects.all()

    # Calculate total hours for each lecturer
    lecturer_workload = []
    for lecturer in lecturers:
        # Get all schedules for this lecturer
        schedules = Schedule.objects.filter(lecturer=lecturer)

        # Assume each lecture is 2 hours
        total_hours = len(schedules) * 2

        # Check if workload exceeds 20 hours
        exceeds_limit = total_hours > 20

        # Append the workload details
        lecturer_workload.append({
            'lecturer': lecturer,
            'total_hours': total_hours,
            'exceeds_limit': exceeds_limit
        })

    # Pass the workload data to the template
    context = {
        'lecturer_workload': lecturer_workload
    }
    return render(request, 'workload_monitoring.html', context)

def apply_leave(request):
    lecturers = Lecturer.objects.all()
    time_slots = TimeSlot.objects.all() # Fetch all lecturers

    if request.method == 'POST':
        # Get form data
        lecturer_id = request.POST.get('lecturer')
        day = request.POST.get('day')
        timeslot_id = request.POST.get('timeslot')

        # Fetch the selected lecturer's schedule
        lecturer_schedule = Schedule.objects.filter(lecturer_id=lecturer_id, day=day)

        # Find available lecturers for the selected time slot and day
        unavailable_lecturers = Schedule.objects.filter(day=day, timeslot_id=timeslot_id).values_list('lecturer_id', flat=True)
        available_lecturers = Lecturer.objects.exclude(id__in=unavailable_lecturers)

        return render(request, 'apply_leave.html', {
            'lecturers': lecturers,
            'time_slots': time_slots,
            'selected_lecturer': get_object_or_404(Lecturer, id=lecturer_id),
            'day': day,
            'available_lecturers': available_lecturers,
        })

    return render(request, 'apply_leave.html', {
        'lecturers': lecturers,
        'time_slots': time_slots,
        'available_lecturers': [],
    })