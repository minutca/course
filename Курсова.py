import tkinter #бібліотека для графічного вікна
from tkinter import ttk #бібліотека для таблиці
window = tkinter.Tk() #створення вікна
window.geometry("1920x1080") #завдаємо розміри
window.title("Складська система ") #змінюємо заголовок вікна 
window.configure(bg="#BED3E4")

import sqlite3 # вбудованна база даних
#створення самої бази даних 
conn = sqlite3.connect("warehouse.db")
cursor = conn.cursor() #підключення бази даних
#створення таблиці stock
cursor.execute(""" 
CREATE TABLE IF NOT EXISTS stock(
id INTEGER PRIMARY KEY AUTOINCREMENT,
product TEXT,
location TEXT,
quantity REAL
)
""")

conn.commit()

#створення функцій
def add_product():
    #отримення даних з полів воду
    product=entry_product.get()
    location=entry_location.get()
    qty=entry_qty.get()

    #перевірка чи всі поля заповнені
    if product =="" or location == "" or qty == "":
        status["text"]="Заповніть всі поля "
        return
    try:
        qty=float(qty)
    except:
        status["text"]= "Кількість має бути числом"
        return
    
#додавання товару до бази даних
    cursor.execute(
    "INSERT INTO stock(product,location,quantity)VALUES(?,?,?)",
    (product,location,qty)
)
    #збереження змін
    conn.commit()
    # повідомлення 
    status["text"]="Товар додано"
#оновлення таблиці
    show_stock()

# функція показу товарів
def show_stock():
    for row in table.get_children():
        table.delete(row)

    cursor.execute("SELECT * FROM stock")

    for row in cursor.fetchall():
        table.insert("", "end", values=(row[0], row[1], row[2], row[3]))
#функція видалення товарів 
def delete_product():
     
#отримання вибраного рядка 
     selected = table.focus()

# перевірка чи вибраний товар 
     if not selected:
         status["text"]="Обреріть товар"
         return
     
     # отримання значення рядка 
     values = table.item(selected,"values")

     product_id = values[0]

     #видалення товару 
     cursor.execute(
        "DELETE FROM stock WHERE id=?",
        (product_id,)
)
     #збереження змін
     conn.commit()
     #повідомлення 
     status["text"]="Товар видалено"
     show_stock()


#функція для переміщення товару
def move_product():
    #отримання вибраного рядка 
    selected=table.focus()

    #пееревірка вибору
    if not selected:
        status["text"]="Оберіть товар"
        return
    
    #отримання нового складу 
    new_location = entry_move.get()

    #перевірка нового складу
    if new_location=="":
        status["text"]="Введіть новий склад"
        return
    try:
        move_qty = float(entry_move_qty.get())
    except:
        status["text"]="Введітть правильну кількість"
        return
    #отримання даних товару
    values = table.item(selected,"values")
    product_id = values[0]
    product = values[1]
    location =values[2]
    qty=float(values[3])
    #перевірка кількості
    if move_qty<=0:
        status["text"]="Кількість має бути більше 0"
        return
    if move_qty>qty:
        status["text"]= "Недостатньо товару"
        return
    #зменшує кількість на старому складі
    cursor.execute(
        "UPDATE stock SET quantity = quantity - ? WHERE id=?",
        (move_qty, product_id)
)
#перевіряємо чи вже є такий товар на новому складі
    cursor.execute(
        "SELECT quantity FROM stock WHERE product=? AND location=?",
        (product, new_location)
)

    result = cursor.fetchone()

    if result:
        cursor.execute(
            "UPDATE stock SET quantity = quantity + ? WHERE product=? AND location=?",
            (move_qty, product, new_location)
)
    else:
        cursor.execute(
            "INSERT INTO stock(product, location, quantity) VALUES(?,?,?)",
            (product, new_location, move_qty)
)
    conn.commit()
    status["text"] = "Товар переміщено"
    show_stock()



frame = tkinter.Label(
    window,
    text="Додавання товару до бази даних",
    font="Calibri 16",
     bg="#BED3E4",
    fg="black", # колір тексту
)
frame.pack(# створення відступа до текста
    pady=10
)
from_frame = tkinter.Frame( #створення контейнера (рамки)
    window,
    bg="white",
    bd=4, # иовщина рамки
    relief = "ridge" # стиль рамки
)
from_frame.pack( #розміщення контейнера (рамки) 
    pady=20
)

tkinter.Label(
    from_frame,
    text="Товар",
    font="Calibri 10",
    bg="white"
).grid(
    row=0,
    column=0,
    pady=10,
    padx=10
)
# поле введення для назви товару
entry_product=tkinter.Entry(
    from_frame, #назва контейнера
    bg="#d3d3d3"
)
# розміщення поля введення
entry_product.grid(
    row=0,
    column=1,
    pady=10,
    padx=10
)

tkinter.Label(
    from_frame,
    text ="Склад",
    font ="Calibri 10",
    bg ="white"
).grid(
    row=1, #рядок в таблиці
    column=0, #колонка
    pady= 10, #відступ по у
    padx= 10 #відступ по х
)
storage=tkinter.Entry( #створення поля для введення
    from_frame,
    bg ="#d3d3d3"
)
storage.grid(
    row= 1,
    column= 1,
    pady=10,
    padx=10
)
#додана зміної для функції
entry_location = storage

tkinter.Label(
    from_frame,
    text= "Кількість",
     font="Calibri 10",
     bg="white"
).grid(

     row=2,#рядок в таблиці
    column=0, #колонка
    pady= 10, #відступ по у
    padx= 10 #відступ по х
)
quantity = tkinter.Entry(
    from_frame,
    bg="#d3d3d3"
)
quantity.grid(
    row=2,
    column=1,
    pady=10,
    padx=10
)
#додана зміної для функції
entry_qty = quantity

add = tkinter.Button(
    from_frame, #контейнер
    text="Додати товар", #текст кнопки
    font="Calibri 12",
    command=add_product
)
add.grid(
    row=3, # нижче інших елементів
    column=0,
    columnspan=2,
    pady=10
)
#створення таблиці
table = ttk.Treeview(
    window,
    columns=(
        "id",
        "product", 
        "location", 
        "qty"
),
    show="headings", #приховує перший порожній стовпець
    height=13
)
table.heading(
    "id",
    text="ID"
)
table.heading(
    "product",
      text="Товар"
)
table.heading(
    "location",
      text="Локація"
)

table.heading(
    "qty",
    text="Кількість"
)

# налаштування колонок 
table.column(
    "id",
    width=50,
    anchor="center"
)
table.column(
    "product", 
    width=350, 
    anchor="center"
)

table.column(
    "location", 
    width=250, 
    anchor="center"
)

table.column(
    "qty", 
    width=150, 
    anchor="center"
)

table.pack(pady=20)

#створення рамки для колонки
btn_frame = tkinter.LabelFrame(
    window,
    text="Операції з товарами",
    font=("Calibri", 12,"bold"),
    bg="#ffffff",
    padx=20,
    pady=10
)

btn_frame.pack(pady=10)

#колонка оновлення
ttk.Button(
    btn_frame, 
    text="Оновити список", 
    command=show_stock
).grid(
    row=0, 
    column=0, 
    padx=10
)


#колонка видалення
ttk.Button(
    btn_frame, 
    text="Видалити товар", 
    command=delete_product
).grid(
    row=0, 
    column=1, 
    padx=10
)

#переміщення 
tkinter.Label(
    btn_frame,
    text="Новий склад",
    bg="#ffffff"
).grid(
    row=1,
    column=0,
    pady=5
)

#поле нового складу
entry_move = tkinter.Entry(btn_frame)
entry_move.grid(
    row=1, 
    column=1
)

tkinter.Label(
    btn_frame, 
    text="Кількість", 
    bg="#f2f4f7"
).grid(
    row=2, 
    column=0, 
    pady=5
)

#поле кількості
entry_move_qty = tkinter.Entry(btn_frame)

entry_move_qty.grid(
    row=2, 
    column=1
)
#кнопка переміщення
ttk.Button(
    btn_frame, 
    text="Перемістити", 
    command=move_product
).grid(
    row=1, 
    column=2, 
    rowspan=2, 
    padx=15
)

# Виведення повідомлення наекран
status = tkinter.Label(#створення текстового напису
    window,
    text="",
    font=("Calibri", 10, "bold"),
    bg="#ffffff",
    fg="#000000"
)

status.pack(pady=10)

# оновлення таблиці
show_stock()

window.mainloop() #зациклив графічне вікно 
