# Программа анализа .csv файлов

import tkinter as tk
from tkinter.scrolledtext import ScrolledText as st
from tkinter import messagebox as mb
from tkinter import filedialog as fd
import os
import pandas as pd

# Создание главного окна
window = tk.Tk()
window.geometry("550x550")
window.title("Программа анализа .csv файлов")

# Создание меток вывода
label_00 = tk.Label(text = "Файл:")
label_00.grid(row=0, column=0, padx=10, pady=10, sticky="e")

label_01 = tk.Label(text = "")
label_01.grid(row=0, column=1, sticky="w")

label_10 = tk.Label(text = "Строк:")
label_10.grid(row=1, column=0, padx=10, pady=10, sticky="e")

label_11 = tk.Label(text = "")
label_11.grid(row=1, column=1, sticky="w")

label_20 = tk.Label(text = "Столбцов:")
label_20.grid(row=2, column=0, padx=10, pady=10, sticky="e")

label_21 = tk.Label(text = "")
label_21.grid(row=2, column=1, sticky="w")

# Создание текстового вывода с прокруткой
output_text = st(height = 22, width = 50)
output_text.grid(row=3, column=1, padx=10, pady=10, sticky="w")

# Диалог открытия файла
def do_dialog():
    my_dir = os.getcwd()
    name= fd.askopenfilename(initialdir=my_dir)
    return name

# Обработка .csv файлф при помощи pandas
def pandas_read_csv(file_name):
    df = pd.read_csv(file_name, header=None, sep=';')
    cnt_rows = df.shape[0]
    cnt_columns = df.shape[1]
    label_11['text'] = cnt_rows
    label_21['text'] = cnt_columns
    return df

# Выборка столбца в список
def get_column(df, column_ix):
    cnt_rows = df.shape[0]
    lst = []
    for i in range(cnt_rows):
        lst.append(df.iat[i, column_ix])
    return lst

# Поиск имени (Наличие имени = True)    
def meet_name(field):
    checkfor = ['Вера', 'Анатолий', 'Мария', 'Артём', 'Алексей', 
        'Валерия', 'Наталья', 'Оксана', 'Галина', 'Марина',
        'Вероника', 'Виталий', 'Борис', 'Диана', 'Ева']
    for s in checkfor:
        if s in str(field): # Есть совпадение
            return True
    # Нет совпадений
    return False 
    
# Подсчет по всем элементам в списке 
# (Если в этом списке многие элементы содержат имя, то True)    
def list_meet_name(fields_list):
    counter_total = 0
    counter_meet = 0
    for list_item in fields_list:
        counter_total += 1
        if meet_name(list_item):
            counter_meet += 1
    # Конец подсчета
    ratio = counter_meet / counter_total
    if ratio > 0.2:
        return True, ratio
    # Не набралось нужного количества совпадений
    return False, ratio  
    
# Проход всех столбцов    
def check_all_columns(df):
    columns_cnt = df.shape[1]
    for i in range(columns_cnt): # От 0 до columns_cnt-1
        lst = get_column(df, i)
        result = list_meet_name(lst)
        if result[0]:
            output_text.insert(tk.END, "В столбце " + str(i+1) + " предположительно содержится имя." + os.linesep)
            output_text.insert(tk.END, "Процент совпадений " + "{:.2f}".format(result[1]*100) + "%." + os.linesep)
        else:
            output_text.insert(tk.END, "Предположений для столбца " + str(i+1) + " не найдено." + os.linesep)          
    
# Обработчик нажатия кнопки
def process_button():
    file_name = do_dialog()
    label_01['text'] = file_name
    df = pandas_read_csv(file_name)
    check_all_columns(df)
    mb.showinfo(title=None, message="Готово!")

# Создание кнопки
button=tk.Button(window, text="Прочитать файл", command=process_button)
button.grid(row=4, column=1)

# Запуск цикла mainloop
window.mainloop()    
