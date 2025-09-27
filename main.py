import customtkinter as ctk
from DBmanager import DBManager
from config import database

app = ctk.CTk()
app.title("CHECKLIST Manager")
app.geometry("700x500")
app.resizable(False, False)

screen_elements = []

manager = DBManager(database)

def clear_screen():
    for element in screen_elements:
        element.pack_forget()

        element.place_forget()
    screen_elements.clear()

def mainmenu():
    clear_screen()
    header = ctk.CTkLabel(app, text="CHECKLIST Manager", font=ctk.CTkFont(size=20, weight="bold"))
    header.pack(pady=20)
    screen_elements.append(header)

    view_checklists_btn = ctk.CTkButton(app, text="View Checklists", command=View_checklists)
    view_checklists_btn.pack(pady=10)
    screen_elements.append(view_checklists_btn)

    add_checklist_btn = ctk.CTkButton(app, text="Add Checklist", command=Add_checklist)
    add_checklist_btn.pack(pady=10)
    screen_elements.append(add_checklist_btn)

    view_brands_btn = ctk.CTkButton(app, text="View Aircraft Brands", command=View_brands)
    view_brands_btn.pack(pady=10)
    screen_elements.append(view_brands_btn)

    Add_brand_btn = ctk.CTkButton(app, text="Add Aircraft Brand", command=Add_brand)
    Add_brand_btn.pack(pady=10)
    screen_elements.append(Add_brand_btn)

    info_btn = ctk.CTkButton(app, text="Info", command=info)
    info_btn.pack(pady=10)
    screen_elements.append(info_btn)

def View_checklists():
    clear_screen()
    back_btn = ctk.CTkButton(app, text="Back to Main Menu", command=mainmenu)
    back_btn.place(x=10, y=10)
    screen_elements.append(back_btn)

    header = ctk.CTkLabel(app, text="All Checklists", font=ctk.CTkFont(size=20, weight="bold"))
    header.pack(pady=20)
    screen_elements.append(header)

    checklist_frame = ctk.CTkFrame(app, width=600, height=400)
    checklist_frame.pack(pady=50)
    screen_elements.append(checklist_frame)

    checklists = manager.get_checklists()
    for checklist in checklists:
        checklist_label_frame = ctk.CTkFrame(checklist_frame)
        checklist_label_frame.pack(pady=5, padx=10, fill="x")
        screen_elements.append(checklist_label_frame)

        # Normal yazı
        checklist_label = ctk.CTkLabel(
            checklist_label_frame, 
            text=f"ID: {checklist[0]}, Aircraft: {checklist[1]}, Brand ID: {checklist[2]}"
        )
        checklist_label.pack(pady=5, padx=10, side=ctk.LEFT)
        screen_elements.append(checklist_label)

        # "Buraya tıkla" link butonu
        link_button = ctk.CTkButton(
            checklist_label_frame, 
            text="Buraya tıkla", 
            fg_color="transparent", 
            text_color="blue", 
            hover_color="lightblue",
            command=lambda c_id=checklist[0]: open_link(c_id)
        )
        link_button.pack(pady=5, padx=5, side=ctk.LEFT)
        screen_elements.append(link_button)

        delete_button = ctk.CTkButton(
            checklist_label_frame, 
            text="Delete", 
            command=lambda c_id=checklist[0]: delete_checklist(c_id)
        )
        delete_button.pack(pady=5, padx=5, side=ctk.RIGHT)
        screen_elements.append(delete_button)

    def delete_checklist(checklist_id):
        manager.delete_checklist(checklist_id)
        View_checklists()

    def open_link(checklist_id):
        manager.open_checklists(checklist_id)


def Add_checklist():
    clear_screen()
    back_btn = ctk.CTkButton(app, text="Back to Main Menu", command=mainmenu)
    back_btn.place(x=10, y=10)
    screen_elements.append(back_btn)

    header = ctk.CTkLabel(app, text="Add New Checklist", font=ctk.CTkFont(size=20, weight="bold"))
    header.pack(pady=20)
    screen_elements.append(header)

    add_frame = ctk.CTkFrame(app, width=600, height=400)
    add_frame.pack(pady=50)
    screen_elements.append(add_frame)

    name_entry = ctk.CTkEntry(add_frame, placeholder_text="Aircraft Name")
    name_entry.pack(pady=5)
    screen_elements.append(name_entry)

    brand_entry = ctk.CTkEntry(add_frame, placeholder_text="Aircraft Brand")
    brand_entry.pack(pady=5)
    screen_elements.append(brand_entry)

    checklist_entry = ctk.CTkEntry(add_frame, placeholder_text="Checklist")
    checklist_entry.pack(pady=5)
    screen_elements.append(checklist_entry)

    def submit_checklist():
        manager.add_checklist(name_entry.get(), brand_entry.get(), checklist_entry.get())
        name_entry.delete(0, ctk.END)
        brand_entry.delete(0, ctk.END)
        checklist_entry.delete(0, ctk.END)

    submit_btn = ctk.CTkButton(add_frame, text="Add Checklist", command=submit_checklist)
    submit_btn.pack(pady=10)
    screen_elements.append(submit_btn)

def View_brands():
    clear_screen()
    back_btn = ctk.CTkButton(app, text="Back to Main Menu", command=mainmenu)
    back_btn.place(x=10, y=10)
    screen_elements.append(back_btn)

    header = ctk.CTkLabel(app, text="All Aircraft Brands", font=ctk.CTkFont(size=20, weight="bold"))
    header.pack(pady=20)
    screen_elements.append(header)

    brand_frame = ctk.CTkFrame(app, width=600, height=400)
    brand_frame.pack(pady=50)
    screen_elements.append(brand_frame)

    brands = manager.get_brands()
    for brand in brands:
        brand_label_frame = ctk.CTkFrame(brand_frame)
        brand_label_frame.pack(pady=5)
        screen_elements.append(brand_label_frame)

        brand_label = ctk.CTkLabel(brand_label_frame, text=f"ID: {brand[0]}, Name: {brand[1]}")
        brand_label.pack(pady=5, padx=10, side=ctk.LEFT)
        screen_elements.append(brand_label)

        delete_button = ctk.CTkButton(brand_label_frame, text="Delete", command=lambda b_id=brand[0]: delete_brand(b_id))
        delete_button.pack(pady=5, padx=5,side=ctk.RIGHT)
        screen_elements.append(delete_button)

        def delete_brand(brand_id):

            manager.delete_brand(brand_id)
            manager.cursor.execute('DELETE FROM checklists WHERE aircraft_brand_id = ?', (brand_id,))
            View_brands()

    

def Add_brand():
    clear_screen()
    back_btn = ctk.CTkButton(app, text="Back to Main Menu", command=mainmenu)
    back_btn.place(x=10, y=10)
    screen_elements.append(back_btn)

    header = ctk.CTkLabel(app, text="Add New Aircraft Brand", font=ctk.CTkFont(size=20, weight="bold"))
    header.pack(pady=20)
    screen_elements.append(header)

    add_frame = ctk.CTkFrame(app, width=600, height=400)
    add_frame.pack(pady=50)
    screen_elements.append(add_frame)

    brand_entry = ctk.CTkEntry(add_frame, placeholder_text="Aircraft Brand Name")
    brand_entry.pack(pady=5)
    screen_elements.append(brand_entry)

    def submit_brand():
        manager.add_brand(brand_entry.get())
        brand_entry.delete(0, ctk.END)

    submit_btn = ctk.CTkButton(add_frame, text="Add Aircraft Brand", command=submit_brand)
    submit_btn.pack(pady=10)
    screen_elements.append(submit_btn)

def info():
    clear_screen()
    back_btn = ctk.CTkButton(app, text="Back to Main Menu", command=mainmenu)
    back_btn.place(y=10)
    screen_elements.append(back_btn)

    header = ctk.CTkLabel(app, text="About CHECKLIST Manager", font=ctk.CTkFont(size=20, weight="bold"))
    header.pack(pady=20)
    screen_elements.append(header)

    info_text = "CHECKLIST Manager v1.0"
    info_text += "\nManage your aircraft checklists easily!"
    info_text += "\nYou can view, add, and delete your checklists and aircraft brands."
    info_text += "\nWhen you are adding new checklist, if the brand does not exist,\nit will be created automatically."
    info_text += "\nYou should add a link or file path in to the checklist field\nwhen you are creating a new checklist."
    info_text += "\nAll checklist of that brand will be delete, when you are delete a brand"

    info_label = ctk.CTkLabel(app, text=info_text, font=ctk.CTkFont(size=18))
    info_label.pack(pady=20)
    screen_elements.append(info_label)

mainmenu()

app.mainloop()