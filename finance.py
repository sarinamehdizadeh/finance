from tkinter import*
import tkinter as TK
import sqlite3
from tkinter.font import Font
from tkinter import messagebox
from datetime import datetime
import os

class Database:
    def __init__(self , db):
        self.__db_name__ = db
        self.connection = sqlite3.connect(db)
        self.cursor = self.connection.cursor()
        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS [transactions](
                            id INTEGER PRIMARY KEY AUTOINCREMENT, 
                            [amount] REAL NOT NULL, 
                            [type] TEXT, 
                            [date] TEXT, 
                            [description] TEXT);
                            """
                            )
        
        self.connection.commit()
        self.connection.close()

    def add_transaction(self ,  amount , typeT , description):
        self.connection = sqlite3.connect(self.__db_name__)
        self.cursor = self.connection.cursor()
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute("INSERT INTO transactions(amount , type,date, description) VALUES(?,?,?,?)", ( amount , typeT ,date, description))
        self.connection.commit()
        self.connection.close()

    def get_all_transactions(self):
        self.connection = sqlite3.connect(self.__db_name__)
        self.cursor = self.connection.cursor()
        self.cursor.execute("SELECT * FROM transactions")
        result = self.cursor.fetchall()
        self.connection.close()
        return result

# =============================Database

db = None


# =========================================tk

window = Tk()
window.title("personal finance manager")
window.geometry("700x800")
padx = 5
pady = 5
vazir_font = Font(family='Vazir' , size=13)


window.columnconfigure(0 , weight=1)
window.rowconfigure(0 ,weight=1)
window.rowconfigure(1 ,weight=5)
window.rowconfigure(2 ,weight=2)

frame_one = LabelFrame(window , text = "اطلاعات کلی")
frame_one.grid(sticky="snew"  , padx=padx , pady=pady)
frame_two = LabelFrame(window , text="افزودن تراکنش جدید")
frame_two.grid(sticky="snew" , padx=padx , pady=pady)
frame_three = LabelFrame(window , text="دکمه ها")
frame_three.grid(sticky="snew" , padx=padx , pady=pady)

frame_one.columnconfigure(0 ,weight= 1)
frame_one.columnconfigure(2 ,weight= 1)
frame_one.columnconfigure(1 ,weight= 1)
frame_one.rowconfigure(0 ,weight= 1)
frame_one.rowconfigure(1 ,weight= 1)


frame_two.columnconfigure(0 , weight=1)
frame_two.columnconfigure(1 , weight=1)
frame_two.columnconfigure(2 , weight=2)
frame_two.rowconfigure(0 , weight=1)
frame_two.rowconfigure(1 , weight=1)

frame_three.columnconfigure(0 ,weight=1)
frame_three.columnconfigure(1 ,weight=1)
frame_three.columnconfigure(2 ,weight=1)
frame_three.columnconfigure(3 ,weight=1)
frame_three.rowconfigure(0 , weight=1)


lal_sum=Label(frame_one , text ="مجموع کل " , font = vazir_font, justify="center")
lal_sum.grid(row = 0 ,column=0)
lal_income=Label(frame_one, text = "درامد" , font = vazir_font, justify="center")
lal_income.grid(row = 0,column=1)
lal_cost = Label(frame_one, text =" هزینه " , font = vazir_font , justify="center")
lal_cost.grid(row = 0 ,column=2 )

lal_sum=Label(frame_one , text ="" , font = vazir_font, justify="center")
lal_sum.grid(row = 1 ,column=0)
lal_income=Label(frame_one, text = "" , font = vazir_font, justify="center")
lal_income.grid(row = 1,column=1)
lal_cost = Label(frame_one, text ="" , font = vazir_font , justify="center")
lal_cost.grid(row = 1,column=2 )




lal_amount =Label(frame_two , text = "مبلغ" , font = vazir_font, justify="center" )
lal_amount.grid(row=0 , column=0 )
ent_amount = Entry(frame_two, font = vazir_font, justify="center")
ent_amount.grid(row=0 , column= 1 , sticky="ew")

lal_description =Label(frame_two , text = "توضیحات" , font = vazir_font, justify="center" )
lal_description.grid(row=1 , column =0)
ent_amout = Entry(frame_two, font = vazir_font, justify="center")
ent_amout.grid(row=1 , column= 1 , sticky="sn")

bot_deposit = Button(frame_two , text = " واریز " , bg= "green" ,font = vazir_font, justify="center")
bot_deposit.grid(row=0 , column=2 , sticky= "ns")

bot_withdraw = Button(frame_two , text = "برداشت" , bg= "red", font = vazir_font, justify="center")
bot_withdraw.grid(row=1, column=2 , sticky= "ns")



# با کلیک روی هر دکمه صفحه جدید مخصوص خودش باز بشه 
# ==================نمایش تراکنش ها 

bot_transactions = Button(frame_three , text = "نمایش تراکنش ها",font = vazir_font, justify="center")
bot_transactions.grid(row=0 , column=0)

#==================== جستجو 

bot_search = Button(frame_three , text = "جستجو",font = vazir_font, justify="center")
bot_search.grid(row=0 , column=1)

# ===================(مثلا 10 تراکنش اخر)فیلتر بر اساس تاریخ یا مبلغ یا تعداد تراکنش

bot_filter = Button(frame_three , text = "فیلتر",font = vazir_font, justify="center")
bot_filter.grid(row=0 , column=2)

window.mainloop()