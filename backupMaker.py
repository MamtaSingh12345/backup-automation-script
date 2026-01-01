import os, shutil
from DirDialogBox import loc_browser

# Create SuccessfulBackup directory if missing
if not os.path.isdir("SuccessfulBackup"):
    os.makedirs("SuccessfulBackup")

suc_backup = os.path.join(os.getcwd(), "SuccessfulBackup")

# Create bulocks file + add first backup location if missing
if not os.path.isfile("bulocks.txt"):
    print("No backup location found, please select one")
    added_loc = loc_browser()
    print("Added new location:", added_loc)

def read_bulocks():
    global list_loc
    with open("bulocks.txt", "r") as locations:
        list_loc = [loc.strip() for loc in locations]

def backup_process():

    # Folders & files we should NOT back up
    skip_items = {
        "SuccessfulBackup",
        "BackupMaker.py",
        "DirDialogBox.py",
        "bulocks.txt",
        "BackupMaker.exe",
        "__pycache__",
        ".git"                 # <-- IMPORTANT FIX
    }

    for each_file in os.listdir():

        if each_file in skip_items:
            continue

        print(each_file)

        for each_loc in list_loc:

            # Copy file
            if os.path.isfile(each_file):
                shutil.copy(each_file, each_loc)

            # Copy folder safely
            else:
                dest_path = os.path.join(each_loc, each_file)

                try:
                    shutil.copytree(each_file, dest_path)

                # If folder already exists → replace it
                except FileExistsError:
                    shutil.rmtree(dest_path)
                    shutil.copytree(each_file, dest_path)

        # Move original file/folder into SuccessfulBackup
        src = os.path.join(os.getcwd(), each_file)
        dst = os.path.join(suc_backup, each_file)
        os.replace(src, dst)

def re_backup(new_loc):

    for each_file in os.listdir(suc_backup):

        original = os.path.join(suc_backup, each_file)

        if os.path.isfile(original):
            shutil.copy(original, new_loc)
        else:
            dest = os.path.join(new_loc, each_file)

            try:
                shutil.copytree(original, dest)
            except FileExistsError:
                shutil.rmtree(dest)
                shutil.copytree(original, dest)

def instruction():
    print("************************************************************************")
    print("For Creating backup press 1")
    print("For adding new back up location press 2")
    print("To exit press 3\n")

instruction()

while True:
    user_input = input()

    # Create backup
    if user_input == "1":
        read_bulocks()
        if not list_loc:
            print("No backup location found, please select one")
            loc_browser()
            instruction()
            continue

        backup_process()
        print("Back up completed!")

    # Add new backup location
    if user_input == "2":
        new_loc = loc_browser()
        print("Added new location:", new_loc)

        user_input2 = input("Do you want to make backup to this new location? (y/n): ")

        if user_input2.lower() == "y":
            re_backup(new_loc)
            print("Back up completed!")
        else:
            print("Back up aborted!")

    instruction()

    # Exit
    if user_input == "3":
        break
