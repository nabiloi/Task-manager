# Command-line Task manager
import os
import sys
import json
import csv

#import time

# File to store tasks
FILE_NAME = "Tasks_list.txt"

# Load tasks from file
def load_tasks():
  tasks = {}
  if os.path.exists(FILE_NAME):
    with open(FILE_NAME, "r") as file:
      for line in file:
        parts = line.strip().split(" | ")
        if len(parts) == 4:
          task_id, title, status, deadline = parts
          tasks[int(task_id)] = {"title": title, "status": status, "deadline": deadline}
        else:
          print(f"Format salah di baris: {line}")
  return tasks

# Save tasks to file
def save_tasks(tasks):
  with open(FILE_NAME, "w") as file:
    for task_id, task in tasks.items():
      file.write(f"{task_id} | {task['title']} | {task['status']} | {task['deadline']}\n")
      
# Add task
def add_task(tasks, title, deadline):
# current_time = time.localtime() # dapatkan waktu saat ini
# timestamp = time.strftime("%H:%M:%S %d-%m-%Y",current_time)
  
  task_id = max(tasks.keys(), default=0) + 1
  tasks[task_id] = {"title": title, "status": "Incomplete", "deadline": deadline}
  print(f"Task '{title}' added.")
  
# View task
def view_task(tasks):
  if not tasks:
    print("No tasks available")
  else:
    for task_id, task in tasks.items():
      print(f"[{task_id}] {task['title']} - {task['status']}")
      
      
def mark_task_complete(tasks, task_id):
  
  if task_id in tasks:
    tasks[task_id]['status'] = "Complete"
    print(f"Task '{tasks[task_id]['title']}' marked as complete.")
  else:
    print("Task ID not found.")
    
def delete_task(tasks, task_id):
  if task_id in tasks:
    """ Kalau tidak ada opsi undo ini bisa
    print(f"Task '{tasks[task_id]['title']}' deleted.")
    del tasks[task_id]
    """ 
    deleted_task = tasks.pop(task_id)
    print(f"Task '{deleted_task['title']}' deleted.")
  else:
    print("Task ID not found.")
    
def importing_json(tasks, json_file="Task_list.json"):
  try:
    with open(file=json_file, mode="w") as file:
      json.dump(tasks, file, indent=4)
      print(f"json file '{json_file}' was created")
  except FileExistsError:
    print("The file already exist")

def importing_csv(tasks, csv_file="Task_list.csv"):
  if not tasks:
    print("Tidak ada tugas untuk diekspor.")
    return
  
  try:
    with open(csv_file, 'w', newline='') as csvfile:
      # Ambil kunci dari salah satu dictionary tugas untuk header kolom.
      # tasks.values() adalah iterable dari dictionary tugas.
      # Kita ambil yang pertama ([0]) untuk mendapatkan kuncinya.

      fieldnames = list(tasks.values())[0].keys()

      writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

      writer.writeheader()  # Tulis header row (nama-nama kolom)
      writer.writerows(tasks.values()) # Tulis semua baris data
      
      print(f"File CSV '{csv_file}' berhasil dibuat.")
      
  except FileExistsError:
    print("File sudah ada")
  except IndexError:
    print("Daftar tugas kosong, tidak ada data untuk diekspor.")
  
# Main Menu
def main():
    tasks = load_tasks()

    if len(sys.argv) > 1: # Jika ada argumen baris perintah
        cmd1 = sys.argv[1] # Perintah utama, Urutan : file(0) - cmd1(1) - opsi1(2) - cmd2(3) - opsi2(4)

        # 1. Handle command-line arguments
        if cmd1 == "--help":
            print("'add <Task name> deadline <deadline time>', to add a task and deadline(opsional)\n'delete <task_id>' to delete task(You can see task_id on 'tasks.txt' file)\n'complete <task_id> to mark spesific task to 'complete'\n'view' to view current tasks(use it withhout any value behind 'view')\n'json' to import to json\n'csv' to import to csv")
            return # Keluar dari program setelah menampilkan help

        match cmd1:
            case "add":
                # Contoh: python Task manager.py add "Belajar Python" deadline 2025-12-31
                # sys.argv: [Task manager.py, "add", "Belajar Python", "deadline", "2025-12-31"]
                if len(sys.argv) < 3: # Butuh setidaknya: add <judul>
                    print("Usage: add <task title> [deadline <date>]")
                    return
                
                title = sys.argv[2]
                deadline = "(No deadline)" # Default value

                # Cek apakah ada argumen untuk deadline
                if len(sys.argv) > 3: # Jika ada argumen setelah judul
                    cmd_deadline_marker = sys.argv[3] # Harusnya 'deadline' atau 'dl'
                    if cmd_deadline_marker == "deadline" or cmd_deadline_marker == "dl":
                        if len(sys.argv) > 4: # Pastikan ada nilai deadline-nya
                            deadline = sys.argv[4]
                        else:
                            print("Error: Please provide a value for deadline.")
                            return
                    else:
                        print(f"Warning: Unknown argument '{cmd_deadline_marker}'. Task added without specific deadline keyword.")
                
                add_task(tasks, title, deadline)
                save_tasks(tasks)

            case "delete" | "complete": # Gabungkan karena logikanya mirip
                # Contoh: python Task manager.py delete 5
                # sys.argv: [Task manager.py, "delete", "5"]
                if len(sys.argv) < 3: # Butuh setidaknya: delete <id>
                    print(f"Usage: {cmd1} <task_id>")
                    return
                
                try:
                    task_id = int(sys.argv[2])
                    if cmd1 == "delete":
                        delete_task(tasks, task_id)
                    elif cmd1 == "complete":
                        mark_task_complete(tasks, task_id)
                    save_tasks(tasks)
                except ValueError:
                    print("Error: Task ID must be a number.")
                except IndexError: #Jika sys.argv[2] tidak ada
                    print(f"Error: Missing task ID for '{cmd1}' command.")


            case "view":
                # Contoh: python Task manager.py view
                # sys.argv: [Task manager.py, "view"]
                if len(sys.argv) > 2: # 'view' harusnya tidak punya argumen tambahan
                    print("Usage: view (no additional arguments)")
                    return
                view_task(tasks)
            
            case "json":
              # Contoh: python Task manager.py json
              # sys.argv: [Task manager.py, "json"]
              importing_json(tasks)
              
            case "csv":
              # Contoh: python Task manager.py csv
              # sys.argv: [Task manager.py, "csv"]
              importing_csv(tasks)
            
            case _: # Jika perintah tidak dikenali
                print(f"Invalid command: '{cmd1}'. Use '--help' for usage.")
        
    else: # Jika tidak ada argumen baris perintah, masuk ke menu
        is_running = True
        while is_running:
          
            print("""
            \nTask Manager Menu
            \n1. Add Task
            \n2. View Tasks
            \n3. Mark Task as Complete
            \n4. Delete Task
            \n5. Import to .json
            \n6. Import to .csv
            \n7. Exit
            """)
            choice = input("Enter your Choice: ")
            
            match choice:
                case "1":
                    title = str(input("Enter task title: "))
                    deadline = str(input("Enter a deadline: "))
                    add_task(tasks, title, deadline)
                    
                case "2":
                    view_task(tasks)
                    
                case "3":
                    task_id = int(input("Enter task ID to mark as complete: "))
                    mark_task_complete(tasks, task_id)
                    
                case "4":
                    task_id = int(input("Enter task ID to delete: "))
                    delete_task(tasks, task_id)
                    
                case "5":
                  importing_json(tasks)
                  
                case "6":
                  importing_csv(tasks)
                  
                case "7":
                    save_tasks(tasks)
                    print("Goodbye")
                    is_running = False
                     
                case _:
                    print(f"Input '{choice}' is not valid.")
        
if __name__ == "__main__":
  main()