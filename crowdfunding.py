import re
import datetime

def read_file(file):
    with open(file, "r") as file:
        return file.read()
def write_file(file, content):
    with open(file, "w") as file:
        file.write(content)

def validate_phone(phone):
    phone_pattern=r"^01[0125][0-9]{8}$"
    return bool(re.fullmatch(phone_pattern,phone))

def validate_email(email):
    email_pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.fullmatch(email_pattern,email))

def validate_name(name):
    name_pattern=r"^[a-zA-Z]{3,}$"
    return bool(re.fullmatch(name_pattern,name))
def validate_date(date):
        try:
            return datetime.datetime.strptime(date, "%d/%m/%Y")
        except ValueError:
            return None


def registration():
    users=read_file("users.txt")
    email = input("enter your email ")
    if not validate_email(email):
        print("invalid email")
        return
    if email in list(map(lambda x: x.split(":")[2],users.split("\n"))):
        print("email already exists")
        return
    
    first_name = input("enter your first name ")
    if not validate_name(first_name):
        print("invalid first name")
        return
    last_name = input("enter your last name ")
    if not validate_name(last_name):
        print("invalid last name")
        return
    password = input("enter your password ").strip()
    if len(password)<4:
        print("password should be at least 4 characters")
    confirm_password = input("confirm your password ")
    if(password != confirm_password):
        print("passwords do not match")
        return
    
    phone = input("enter your mobile number ")
    if not validate_phone(phone):
        print("invalid egyptian phone number")
        return
    users+=f"\n{first_name}:{last_name}:{email}:{password}:{phone}"
    write_file("users.txt",users)
    print("registration successful")
def login():
    users=read_file("users.txt")
    email = input("enter your email ")
    if not validate_email(email):
        print("invalid email")
        return
    if not email in list(map(lambda x: x.split(":")[2],users.split("\n"))):
        print("email is not registered")
        return
    password = input("enter your password ").strip()
    for user in users.split("\n"):
        if user.split(":")[2]==email and user.split(":")[3]==password:
            print("login successful")
            return email
    print("password is incorrect")

def create_project(user_email):
    projects=read_file("projects.txt")
    title=input("enter project title ")
    details=input("enter project details ")
    target=input("enter total target ")
    if not target.isdigit() or int(target)<0:
        print("target amount must be a positive number")
        return
    start_date=input("enter start date (day/month/year) ")
    end_date=input("enter end date (day/month/year): ")
    if not validate_date(start_date) or not validate_date(end_date) or validate_date(start_date) > validate_date(end_date):
        print("invalid date data")
        return
    projects+=f"\n{user_email}:{title}:{details}:{target}:{str(validate_date(start_date))[:11]}:{str(validate_date(end_date))[:11]}"    
    write_file("projects.txt", projects)
    print("project created successfully")

def view_projects():
    projects = read_file("projects.txt")
    if not projects:
        print("projects is empty")
        return
    for project in projects.split("\n"):
        email,title,details,target,start,end=project.split(":")
        print(f"Email: {email}\nTitle: {title}\nDetails: {details}\nTarget amount: {target}\nStart: {start}\nEnd: {end}\n{'*'*50}")

def edit_project(user_email):
    projects = read_file("projects.txt").split("\n")
    title = input("enter the title of the project ")
    index=0
    for project in projects:
        if project.startswith(f"{user_email}:{title}"):
            new_details = input("enter new details ")
            if not new_details:
                new_details=project.split(":")[1]
            new_target = input("enter new target amount ")
            if not new_target:
                new_target=project.split(":")[3]
            elif not new_target.isdigit() or int(new_target)<0:
                print("target amount must be a positive number so it will be the same")
                new_target=project.split(":")[3]
            
            new_start = input("enter new start date (day/month/year) ")
            new_end = input("enter new end date (day/month/year) ")
            if not new_start:
                new_start=project.split(":")[4]
            if not new_end:
                new_end=project.split(":")[5]
            if not validate_date(new_start) or not validate_date(new_end) or validate_date(new_start) > validate_date(new_end):
                print("invalid date data so it will be the same")
                new_start=project.split(":")[4]
                new_end=project.split(":")[5]
            projects[index] = f"{user_email}:{title}:{new_details}:{new_target}:{str(validate_date(new_start))[:11]}:{str(validate_date(new_end))[:11]}"
            write_file("projects.txt", "\n".join(projects))
            print("project updated successfully")
            return
        index+=1
    print("either unauthorized access or project not found")

def delete_project(user_email):
    projects = read_file("projects.txt").split("\n")
    title = input("enter the title of the project ")
    for project in projects:
        if project.startswith(f"{user_email}:{title}"):
            projects.remove(project)
            write_file("projects.txt", "\n".join(projects))
            print("project deleted successfully")
            return
    print("either unauthorized access or project not found")

def search_project_by_date():
    projects = read_file("projects.txt").split("\n")
    date = input("enter the start date (day/month/year) ")
    if not validate_date(date):
        print("invalid date")
        return
    date=str(validate_date(date))[:11]
    found=False
    for project in projects:
        #if project.split(":")[4] <= date <= project.split(":")[5]:
        if project.split(":")[4] == date or project.split(":")[5] == date:
            found=True
            email,title,details,target,start,end=project.split(":")
            print(f"Email: {email}\nTitle: {title}\nDetails: {details}\nTarget amount: {target}\nStart: {start}\nEnd: {end}\n{'*'*50}")
    if not found:
        print("no project found")

while True:    
    choice = input("enter number of your choice\n1.Register\n2.Login\n3.Exit\n")
    match choice:
            case "1":
                registration()
            case "2":
                user_email = login()
                if user_email:
                    while True:
                        action = input("choose action\n1.Create Project\n2.View Projects\n3.Edit Project\n4.Delete Project\n5.Search by Date\n6.Logout\n")
                        match action:
                            case "1":
                                create_project(user_email)
                            case "2": 
                                view_projects()
                            case "3": 
                                edit_project(user_email)
                            case "4": 
                                delete_project(user_email)
                            case "5": 
                                search_project_by_date()
                            case "6": 
                                break
            case "3":
                break
            case _:
                print("unsupported choice")
