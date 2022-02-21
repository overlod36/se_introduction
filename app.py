from tkinter import *
from tkinter import ttk
import datetime
import sqlite3

def time_ch():
    return str(str(datetime.datetime.now()).split()[0] + " " + str(datetime.datetime.now()).split()[1][:8])

def keys_delete(k):
    ms = list(db.execute(f"SELECT * FROM cards WHERE card_id == ?", (k.get())))
    if (len(ms) != 0):
        db.execute(f"UPDATE cards SET activity = ? WHERE card_id == ?", ("Не действителен", k.get()))
        db.commit()

def employee_add(name, s_name, pos, i):
    db.execute(f"INSERT INTO employees(employee_name,employee_surname, employee_position) VALUES (?, ? ,?)", (name.get(), s_name.get(), pos.get()))
    db.commit()
    sd = sql.execute("SELECT employee_id FROM employees").fetchall()
    i.config(state="normal")
    i.insert(0, sd[len(sd) - 1][0])
    i.config(state="disable")

def keys_add(e, t, c):
    ms = list(db.execute(f"SELECT * FROM employees WHERE employee_id == ?", (e.get())))
    if (len(ms) != 0):
        db.execute(f"INSERT INTO cards(release_date,validity,emp_id, activity) VALUES (?, ?, ?, ?)", (str(datetime.datetime.now()).split()[0], t.get(), e.get(), "Действителен"))
        db.commit()
        sd = sql.execute("SELECT card_id FROM cards").fetchall()
        c.config(state="normal")
        c.insert(0, sd[len(sd)-1])
        c.config(state="disable")
    else:
        c.config(state="normal")
        c.insert(0, "Такого человека нет!")
        c.config(state="disable")

def admin_keys_show(text, ent, attend):
    cm1_1 = list(db.execute(f"SELECT * FROM cards WHERE card_id == ?", (ent.get())).fetchall())
    if (len(cm1_1) != 0):
        cm0 = list(db.execute(f"SELECT emp_id FROM cards WHERE card_id == ?", (ent.get())))
        cm1_2 = list(db.execute(f"SELECT * FROM employees WHERE employee_id == ?", str(cm0[len(cm0)-1][0])))
        print(cm1_1)
        res1 = "Пропуск [{0}]. ID пропуска - {1}, дата активации - {2}, cрок действия - {3} месяцев. Фамилия владельца - {4}, имя владельца - {5}, должность владельца - {6}".format(cm1_1[0][3], cm1_1[0][0], cm1_1[0][1], cm1_1[0][2], cm1_2[0][2], cm1_2[0][1], cm1_2[0][3])
        cm2_1 = list(db.execute(f"SELECT ev_id FROM attendance_log WHERE c_id == ?", (ent.get())).fetchall())
        print(cm1_1, cm1_2)
        attend.delete('1.0', END)
        for i in range(len(cm2_1)):
            cm2_2 = list(
                db.execute(f"SELECT event_type, ev_place, event_date FROM events WHERE event_id == ?",
                           (cm2_1[i])).fetchall())
            if (cm2_2[0][0] == "Вход"):
                attend.insert(END, "{0} произошёл {1} в {2} здание\n".format(cm2_2[0][2], cm2_2[0][0], cm2_2[0][1]))
            else:
                attend.insert(END, "{0} произошёл {1} из {2} здания\n".format(cm2_2[0][2], cm2_2[0][0], cm2_2[0][1]))
        text.delete('1.0', END)
        text.insert(END, res1)
    else:
        text.delete('1.0', END)
        text.insert(END, "Такого пропуска нет!")


def entry(e, text, bs):
    sd = list(db.execute(f"SELECT * FROM cards WHERE card_id == ?", (e.get())).fetchall())
    if (len(sd) != 0):
        if (sd[0][3] == "Действителен"):
            cm1 = list(db.execute(f"SELECT ev_id FROM attendance_log WHERE c_id == ?", (e.get())).fetchall())
            if (len(list(cm1)) != 0):
                cm3 = list(db.execute(f"SELECT event_type, ev_place FROM events WHERE event_id == ?", (cm1[len(cm1) - 1])).fetchall())
                print(cm3)
                if (cm3[len(cm3)-1][0] == "Вход" and cm3[len(cm3)-1][1] != bs.get()):
                    text.delete('1.0', END)
                    text.insert(END, "Вы сейчас в {} здании!".format(cm3[len(cm3)-1][1]))
                else:
                    if (cm3[len(cm3) - 1][0] == "Вход"):
                        db.execute(f"INSERT INTO events(event_date,ev_place,event_type) VALUES (?,?,?)",
                                   (time_ch(), bs.get(), "Выход")).fetchall()
                        db.commit()
                        cm2 = list(db.execute(f"SELECT event_id FROM events"))
                        db.execute(f"INSERT INTO attendance_log(ev_id, c_id) VALUES (?, ?)", (cm2[len(cm2) - 1][0], e.get()))
                        db.commit()
                        text.delete('1.0', END)
                        text.insert(END, "Вы вышли из универа!")
                    elif (cm3[len(cm3) - 1][0] == "Выход"):
                        db.execute(f"INSERT INTO events(event_date,ev_place,event_type) VALUES (?,?,?)",
                                   (time_ch(), bs.get(), "Вход")).fetchall()
                        db.commit()
                        cm2 = list(db.execute(f"SELECT event_id FROM events"))
                        db.execute(f"INSERT INTO attendance_log(ev_id, c_id) VALUES (?, ?)", (cm2[len(cm2) - 1][0], e.get()))
                        db.commit()
                        text.delete('1.0', END)
                        text.insert(END, "Вы зашли в универ!")

            else:
                db.execute(f"INSERT INTO events(event_date,ev_place,event_type) VALUES (?,?,?)",
                           (time_ch(), bs.get(), "Вход")).fetchall()
                db.commit()
                cm2 = list(db.execute(f"SELECT event_id FROM events"))
                db.execute(f"INSERT INTO attendance_log(ev_id, c_id) VALUES (?, ?)", (cm2[len(cm2) - 1][0], e.get()))
                db.commit()
                text.delete('1.0', END)
                text.insert(END, "Вы зашли в универ!")
        else:
            text.delete('1.0', END)
            text.insert(END, "Пропуск не действителен!")
    else:
        text.delete('1.0', END)
        text.insert(END, "Такого пропуска нет!")




def delete_key_window():
    delete_window = Toplevel(window)
    delete_window.geometry('400x275+200+100')
    delete_window.title('Пропускная система')
    delete_text = Label(delete_window, text="Деактивация пропусков")
    code_entry_text = Label(delete_window, text="Уникальный код пропуска -> ")
    delete_code_entry = Entry(delete_window)
    delete_button = Button(delete_window, text="Деактивация")
    delete_text.place(x = 139, y = 40)
    delete_button.place(x = 172, y = 150)
    code_entry_text.place(x = 50, y = 95)
    delete_code_entry.place(x = 225, y = 98)
    delete_button.config(command=lambda k=delete_code_entry:keys_delete(k))

def add_employee_window():
    add_emp_window = Toplevel(window)
    add_emp_window.geometry('400x275+200+100')
    add_emp_window.title('Пропускная система')
    add_emp_text = Label(add_emp_window, text="Добавление сотрудников/студентов")
    name_entry_text = Label(add_emp_window, text="Имя владельца пропуска -> ")
    surname_entry_text = Label(add_emp_window, text="Фамилия владельца пропуска  -> ")
    position_entry_text = Label(add_emp_window, text="Должность владельца -> ")
    position_entry_text.place(x=50, y=115)
    add_button = Button(add_emp_window, text="Добавить")
    add_button.place(x=175,y=158)
    id_text = Label(add_emp_window, text="Уникальный ID владельца -> ")
    id_entry = Entry(add_emp_window)
    name_entry = Entry(add_emp_window, width=25)
    surname_entry = Entry(add_emp_window, width=21)
    position_entry = ttk.Combobox(add_emp_window, width=27,
                                       values=["Студент", "Преподаватель", "Администратор", "Работник вуза", "Гость"])
    position_entry.place(x=196,y=117)
    surname_entry.place(x=249, y=75)
    name_entry_text.place(x=50, y=93)
    id_entry.config(state=DISABLED)
    id_entry.place(x=225, y=207)
    name_entry.place(x=225, y=96)
    add_emp_text.place(x=105, y=40)
    id_text.place(x=50, y=205)
    surname_entry_text.place(x=50, y=73)
    add_button.config(
        command=lambda name=name_entry, s_name=surname_entry, pos=position_entry, i=id_entry: employee_add(name, s_name, pos,i))

def delete_employee(id):
    ds = list(db.execute("SELECT * FROM cards WHERE emp_id == ?", (id.get())))
    if (len(ds) == 0):
        db.execute("DELETE FROM employees WHERE employee_id == ?", (id.get()))

def delete_employee_window():
    print(list(db.execute("SELECT * FROM employees")))
    del_emp_window = Toplevel(window)
    del_emp_window.geometry('400x275+200+100')
    del_emp_window.title('Пропускная система')
    del_emp = Label(del_emp_window, text="Удаление информации о сотрудниках/студентов")
    id_entry_text = Label(del_emp_window, text="ID владельца -> ")
    del_id_entry = Entry(del_emp_window)
    del_emp.place(x=65, y=40)
    id_entry_text.place(x=95, y=95)
    del_id_entry.place(x=205, y=96)
    delete_button = Button(del_emp_window, text="Удаление")
    delete_button.place(x=170, y=154)
    delete_button.config(command=lambda id=del_id_entry: delete_employee(id))

def add_key_window():
    addi_window = Toplevel(window)
    addi_window.geometry('400x275+200+100')
    addi_window.title('Пропускная система')
    addi_text = Label(addi_window, text="Добавление пропусков")
    code_entry_text = Label(addi_window, text="Уникальный код пропуска -> ")
    time_entry_text = Label(addi_window, text="Срок действия пропуска (в месяцах) -> ")
    id_entry_text = Label(addi_window, text="ID владельца -> ")
    card_id_entry = Entry(addi_window)
    card_id_entry.config(state=DISABLED)
    time_entry = Entry(addi_window, width=7)
    id_entry = Entry(addi_window, width=10)
    add_button = Button(addi_window, text="Добавить")
    add_button.config(command=lambda E=id_entry, T=time_entry, C=card_id_entry: keys_add(E,T,C))
    card_id_entry.place(x = 225, y = 175)
    time_entry.place(x = 274, y = 77)
    id_entry.place(x = 145, y = 97)
    add_button.place(x = 170, y = 137)
    addi_text.place(x = 135, y = 40)
    code_entry_text.place(x = 50, y = 175)
    time_entry_text.place(x=50, y = 75)
    id_entry_text.place(x=50, y=95)

def show():
    show_window = Toplevel(window)
    show_window.geometry('400x275+200+100')
    show_window.title('Пропускная система')
    show_text = Label(show_window, text="Показ информации о пропусках")
    show_text.place(x = 115, y = 20)
    all_button = Button(show_window, text="Вывод всего", command=list_show)
    sh_button = Button(show_window, text="По ID", command=admin)
    all_button.place(x = 168, y = 80)
    sh_button.place(x = 185, y = 150)

def sh(info):
    info.delete('1.0', END)
    d1 = list(db.execute(f"SELECT * FROM employees"))
    if (len(d1) != 0):
        d2 = list(db.execute(f"SELECT * FROM cards"))
        for i in range(len(d1)):
            d0 = list(db.execute(f"SELECT * FROM cards WHERE emp_id == ?", str(d1[i][0])))
            print(d1, d0)
            if (len(d0) == 0):
                info.insert(END, "ID человека - {0}, {1} {2}, должность - {3}, пропуска нет\n".format(d1[i][0], d1[i][2], d1[i][1], d1[i][3]))
            else:
                info.insert(END, "ID человека - {0}, {1} {2}, должность - {3}, ID пропуска - {4}, дата активации - {5}, срок действия - {6}, [{7}]\n".format(d1[i][0], d1[i][2], d1[i][1], d1[i][3], str(d0[0][0]), d0[0][1], d0[0][2], d0[0][3]))

def list_show():
    show_window = Toplevel(window)
    show_window.geometry('400x275+200+100')
    show_window.title('Пропускная система')
    show_text = Label(show_window, text="Все сотрудники/студенты")
    show_text.place(x = 137, y = 20)
    info = Text(show_window, width = 43, height = 9)
    info.place(x = 25, y = 45)
    butt = Button(show_window, text="Вывод")
    butt.config(command=lambda info=info: sh(info))
    butt.place(x = 180, y = 220)


def admin():
    admin_window = Toplevel(window)
    admin_window.geometry('400x275+200+100')
    admin_window.title('Пропускная система')
    admin_text = Label(admin_window, text="Администратор")
    first_text_p = Label(admin_window, text="Ключ пропуска")
    admin_entry = Entry(admin_window, width=5)
    admin_keys_text = Text(admin_window, width=27, height=4.5)
    admin_attend_text = Text(admin_window, width=47, height=5.8)
    admin_keys_button = Button(admin_window, text="Ok")
    admin_entry.place(x=98, y=100)
    admin_text.place(x=155, y=25)
    first_text_p.place(x=5, y=97)
    admin_keys_button.place(x=135, y=97)
    admin_attend_text.place(x=10, y=160)
    admin_keys_text.place(x=170, y=60)
    admin_keys_button.config(
        command=lambda text=admin_keys_text, ent=admin_entry, attend=admin_attend_text: admin_keys_show(text, ent,
                                                                                                        attend))

def choose_access():
    if (choice_access_right.get() == "Посетитель"):
        user_window = Toplevel(window)
        user_window.geometry('400x275+200+100')
        user_window.title('Пропускная система')
        user_text = Label(user_window,text="Посетитель")
        user_info_bar = Text(user_window, width=21, height = 1)
        building_status = ttk.Combobox(user_window, width=12,
                                       values=list(sql.execute("""SELECT building_num FROM buildings""")))
        users_entry = Entry(user_window, width = 10)
        user_entry_text = Label(user_window, text="ID пропуска -> ")
        num_building_text = Label(user_window, text="Номер здания -> ")
        user_entry_text.place(x = 105, y=85)
        user_button = Button(user_window, text = "Ok")
        user_button.place(x = 185, y = 152)
        users_entry.place(x = 200, y = 86)
        num_building_text.place(x = 105, y=110)
        user_text.place(x = 165, y = 40)
        building_status.place(x = 208, y = 110)
        user_info_bar.place(x = 115, y = 199)
        user_button.config(command=lambda ent=users_entry, tx = user_info_bar, bs = building_status: entry(ent, tx, bs))

    elif (choice_access_right.get() == "Администратор"):
        admin_choose = Toplevel(window)
        admin_choose.geometry('400x275+200+100')
        admin_choose.title('Пропускная система')
        admin_choose_text = Label(admin_choose, text = "Администратор")
        admin_choose_text.place(x = 159, y = 40)
        admin_add_button = Button(admin_choose, text="Добавление", width=22, command=add_employee_window)
        admin_delete_button = Button(admin_choose, text="Удаление", width=22, command=delete_employee_window)
        admin_show_button = Button(admin_choose, text="Вывод", width=22, command=show)
        admin_add_button.place(x = 120, y = 90)
        admin_delete_button.place(x = 120, y = 130)
        admin_show_button.place(x = 120, y = 170)

    elif (choice_access_right.get() == "Обслуживающая компания"):
        comp_window = Toplevel(window)
        comp_window.geometry('400x275+200+100')
        comp_window.title('Пропускная система')
        comp_text = Label(comp_window, text = "Обслуживающая компания")
        comp_add_button = Button(comp_window, text = "Добавление", width = 22, command=add_key_window)
        comp_delete_button = Button(comp_window, text = "Деактивация", width = 22, command=delete_key_window)
        comp_text.place(x = 122, y = 40)
        comp_add_button.place(x = 120, y = 90)
        comp_delete_button.place(x = 120, y = 140)


if __name__ == '__main__':
    db = sqlite3.connect('server.db')
    sql = db.cursor()

    sql.execute("""CREATE TABLE IF NOT EXISTS employees (
            employee_id INTEGER PRIMARY KEY,
            employee_name TEXT NOT NULL,
            employee_surname TEXT NOT NULL,
            employee_position TEXT NOT NULL  
        )""")

    sql.execute("""CREATE TABLE IF NOT EXISTS buildings (
            building_num INTEGER PRIMARY KEY,
            building_address TEXT NOT NULL)
        """)

    sql.execute("""CREATE TABLE IF NOT EXISTS attendance_log (
        attend_id INTEGER PRIMARY KEY,
        ev_id INTEGER NOT NULL,
        c_id INTEGER NOT NULL,
        FOREIGN KEY (ev_id) REFERENCES events(event_id)
        FOREIGN KEY (c_id) REFERENCES cards(card_id)
    )""")

    sql.execute("""CREATE TABLE IF NOT EXISTS cards (
        card_id INTEGER PRIMARY KEY,
        release_date TEXT NOT NULL,
        validity INTEGER NOT NULL,
        activity TEXT NOT NULL,
        emp_id INTEGER NOT NULL,
        FOREIGN KEY (emp_id) REFERENCES employees(employee_id))
    """)



    sql.execute("""CREATE TABLE IF NOT EXISTS events (
        event_id INTEGER PRIMARY KEY,
        event_date TEXT NOT NULL,
        ev_place TEXT NOT NULL,
        event_type TEXT NOT NULL,
        FOREIGN KEY (ev_place) REFERENCES buildings(building_num))
    """)

    sql.execute("""INSERT INTO buildings(building_num,building_address) SELECT ?, ? WHERE NOT EXISTS (SELECT 1 FROM buildings WHERE building_num = ? AND building_address = ?)""",(2, "ул. Четаева, 18", 2, "ул. Четаева, 18"))
    sql.execute("""INSERT INTO buildings(building_num,building_address) SELECT ?, ? WHERE NOT EXISTS (SELECT 1 FROM buildings WHERE building_num = ? AND building_address = ?)""",(1, "ул. Карла Маркса, 10", 1, "ул. Карла Маркса, 10"))
    sql.execute("""INSERT INTO buildings(building_num,building_address) SELECT ?, ? WHERE NOT EXISTS (SELECT 1 FROM buildings WHERE building_num = ? AND building_address = ?)""", (3, "ул. Льва Толстого, 15", 3, "ул. Льва Толстого, 15"))
    sql.execute("""INSERT INTO buildings(building_num,building_address) SELECT ?, ? WHERE NOT EXISTS (SELECT 1 FROM buildings WHERE building_num = ? AND building_address = ?)""", (4, "ул. Горького, 28/17", 4, "ул. Горького, 28/17"))
    sql.execute("""INSERT INTO buildings(building_num,building_address) SELECT ?, ? WHERE NOT EXISTS (SELECT 1 FROM buildings WHERE building_num = ? AND building_address = ?)""", (5, "ул. Карла Маркса, 31/7", 5, "ул. Карла Маркса, 31/7"))
    sql.execute("""INSERT INTO buildings(building_num,building_address) SELECT ?, ? WHERE NOT EXISTS (SELECT 1 FROM buildings WHERE building_num = ? AND building_address = ?)""", (6, "ул. Дементьева, 2а", 6, "ул. Дементьева, 2а"))
    sql.execute("""INSERT INTO buildings(building_num,building_address) SELECT ?, ? WHERE NOT EXISTS (SELECT 1 FROM buildings WHERE building_num = ? AND building_address = ?)""", (7, "ул. Большая Красная, 55", 7, "ул. Большая Красная, 55"))
    sql.execute("""INSERT INTO buildings(building_num,building_address) SELECT ?, ? WHERE NOT EXISTS (SELECT 1 FROM buildings WHERE building_num = ? AND building_address = ?)""", (8, "ул. Четаева, 18а", 8, "ул. Четаева, 18а"))

    print(list(db.execute(f"SELECT * FROM employees")))

    window = Tk()
    window.geometry('400x275+200+100')
    window.title('Пропускная система')
    main_accept_but = Button(text="Ok", command = choose_access)
    main_text = Label(text="Главное меню")
    choice_access_right = ttk.Combobox(window, width = 23 ,values = ["Посетитель", "Администратор", "Обслуживающая компания"])
    choice_access_right.place(x = 120, y = 100)
    main_accept_but.place(x = 190, y = 175)
    main_text.place(x = 155, y = 40)
    window.mainloop()