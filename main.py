
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import openpyxl


subjects = ["Urdu", "Mathematics", "Physics", "English",
    "Computer Science", "Biology", "Chemistry",
    "Islamiyat", "Tarjamat ul Qur'an"]


root = tk.Tk()

root.title('Students Score Calculator')
root.geometry('1920x1280')
root.configure(bg='lightblue')

uploaded_data = None
pd.DataFrame(uploaded_data)

# If user want to see already created CSV file.

def load_file():
    global uploaded_data

    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx")])

    if file_path.endswith('.csv'):
        uploaded_data = pd.read_csv(file_path)
        uploaded_data = pd.DataFrame(uploaded_data)

    elif file_path.endswith('.xlsx'):
        uploaded_data = pd.read_excel(file_path, engine='openpyxl')
        uploaded_data =  pd.DataFrame(uploaded_data)
    else:
        messagebox.showerror('Please upload only the CSV and MS Excel files')
        return

    if uploaded_data.empty:
        print("The DataFrame is empty.")
        return
    else:
        print(uploaded_data.head())
        return


def save_results():
    try:
        # Open file save dialog
        save_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx")])

        if save_path:  # Proceed only if a file path is chosen
            if save_path.endswith('.csv'):
                students_data.to_csv(save_path, index=False)
            elif save_path.endswith('.xlsx'):
                students_data.to_excel(save_path, index=False,
                                      engine='openpyxl')
            else:
                messagebox.showerror("Error", "Invalid file format selected.")
                return

            # Success message
            messagebox.showinfo("Success", "Results saved successfully!")
        else:
            messagebox.showinfo("Cancelled", "Save operation cancelled.")
    except Exception as e:
        # Error handling
        messagebox.showerror("Error",
                             f"An error occurred while saving the file:\n{e}")


tk.Button(root, text="Upload File", command=load_file, font=("Poppins", 10), bg='dark blue', fg='white', width=10, height=2).place(relx=0.5,
                                        rely=0.2, anchor='center')

save_button= tk.Button(root, text="Save Results", command=save_results,font=("Poppins", 10), bg='dark blue', fg='white', width=10, height=2)
save_button.place(relx=0.5, rely=0.7, anchor='center')

plot_frame = tk.Frame(root, bg='gray')
plot_frame.grid(sticky="nsew")
def display_file_data(data1=None):

    for widget in plot_frame.winfo_children():
        widget.destroy()

    tree = ttk.Treeview(plot_frame, columns=list(data1.columns))
    total_width = tree.winfo_width()
    column_width = total_width // (len(tree["columns"]) + 1)
    tree.column("#0", width=column_width, stretch=True)

    for col in data1.columns:
        tree.heading(col, text=col)
        tree.column(col, width=70, anchor='center')
        # tree.place(relx=0.4, rely=0.7)

    for _, row in data1.iterrows():
        tree.insert("", tk.END, values=list(row))
    tree.grid(sticky="nsew")


button4 = tk.Button(root, text="Display File Data", command=lambda: display_file_data(uploaded_data),
                   font=("Poppins", 10), width=15, height=2, bg='dark blue', fg='white')
button4.place(relx=0.3, rely=0.7, anchor="center")


def plot_graph():
    global students_data
    fig, ax = plt.subplots(figsize=(8,5))
    ax.bar(students_data['Name'], students_data['Percentage'], color='blue')
    plt.title("Student Performance")
    plt.xlabel("Students")
    plt.ylabel("Percentage")
    plt.show()

    for widget in frame_graph.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=frame_graph)
    canvas.draw()
    canvas.get_tk_widget().grid()

    for widget in frame_graph.winfo_children():
        widget.destroy()

button6 = (tk.Button(root, text="Show Graph", command=plot_graph, font=('Poppins',10), width=10, height=2,
                     bg='dark blue', fg='white'))
button6.place(relx=0.6, rely=0.7, anchor='center')
frame_graph = tk.Frame(root, bg='gray')
frame_graph.grid(sticky="nsew")


frame_table = tk.Frame(root, bg='black')
# frame_table.grid(sticky="nsew")
frame_table.place(relx=0.8, rely=0.1, anchor='n')

def display_data(data=None):

    for widget in frame_table.winfo_children():
        widget.destroy()

    tree = ttk.Treeview(frame_table, columns=list(data.columns))
    total_width = tree.winfo_width()
    column_width = total_width // (len(tree["columns"]) + 1)
    tree.column("#0", width=column_width, stretch=True)
    for col in data.columns:
        tree.heading(col, text=col)
        tree.column(col, width=70, anchor='center')
        # tree.place(relx=0.4, rely=0.7)

    for _, row in data.iterrows():
        tree.insert("", tk.END, values=list(row))
    tree.grid(sticky="nsew")


button4 = tk.Button(root, text="Display", command=lambda: display_data(students_data),
                   font=("Poppins", 10), width=10, height=2, bg='dark blue', fg='white')
button4.place(relx=0.4, rely=0.7, anchor="center")



# If user write students data manually in GUI.
# Creates an empty dataframe.
students_data = pd.DataFrame(columns=[])


def add_student():
 global students_data
 name = entry_name.get()
 subject = subject_combobox.get()
 marks_obtained = entry_marks.get()
 total_marks = entry_total.get()

 if not marks_obtained or not total_marks:
     messagebox.showerror("Missing Information",
                          "Marks fields cannot be empty.")
     return

 try:
     marks_obtained = float(marks_obtained)  # Convert to float after checking for empty string
     total_marks = float(total_marks)
 except ValueError:
     messagebox.showerror("Invalid Input", "Marks must be numbers.")
     return

 if not name or not subject:
        messagebox.showerror("Missing Information", "Please fill all fields.")
        return

 percentage = (marks_obtained / total_marks) * 100
 grade = "A+" if percentage >= 90 else "A" if percentage >= 75 else "B" if percentage >= 65 else "C" if percentage >= 45 else "Fail"

 new_row = pd.DataFrame([{"Name": name, "Subjects": subject,
                         "Marks_Obtained": marks_obtained, "Total_Marks":total_marks,
            "Percentage": percentage, "Grade": grade}])

 if not new_row.dropna(how="all").empty:
     students_data = pd.concat([students_data, new_row], ignore_index=True)
 else:
     print(
         "Warning: The new row is empty or contains only NA values and was not added.")

 subject_combobox.set("")

 print(students_data)
 display_data(students_data)
 messagebox.showinfo("Success", "Student added successfully!")



frame_input = tk.Frame(root, width=400, height=300, bg='lightgray')
# frame_input.grid(row=0, column=0, pady=10)
frame_input.place(relx=0.5, rely=0.5, anchor='center', bordermode='outside')

frame_input.grid_columnconfigure(0, weight=1)

center_frame = tk.Frame(root, bg="white", relief="solid", width=90, height=44.5, bd=1)
center_frame.place(relx=0.7, rely=0.5, anchor='center',)


tk.Label(frame_input, text="Name", bg='yellow').grid(row=0, column=0, pady=10)
entry_name = tk.Entry(frame_input)
entry_name.grid(row=0, column=1, pady=10)

tk.Label(frame_input, text="Subject", bg='yellow').grid(row=1, column=0, pady=10)
subject_combobox = ttk.Combobox(frame_input, values=subjects, state='normal')
subject_combobox.grid(row=1, column=1, pady=10, sticky="ew")
# entry_subject = tk.Entry(frame_input)
# entry_subject.grid(row=1, column=1)

tk.Label(frame_input, text="Marks Obtained", bg='yellow').grid(row=2, column=0)
entry_marks = tk.Entry(frame_input)
entry_marks.grid(row=2, column=1, pady=10)

tk.Label(frame_input, text="Total Marks", bg='yellow').grid(row=3, column=0)
entry_total = tk.Entry(frame_input)
entry_total.grid(row=3, column=1, pady=10)

button5 = tk.Button(center_frame, text="Add Student", command=add_student, font=('Poppins',10), width=10, height=2,
          bg='brown', fg='white')
button5 = button5.place(relx=0.5, rely=0.5, anchor="center")



tk.Button(root, text="Quit", command=root.quit,font=("Poppins", 10), width=10, height=2, bg='Black', fg='white').place(
    relx=0.3,  rely=0.5, anchor='center')




root.mainloop()