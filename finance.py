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
    
    def get_summary(self):
        self.connection = sqlite3.connect(self.__db_name__)
        self.cursor = self.connection.cursor()
        self.cursor.execute("""
            SELECT
                            SUM(CASE WHEN amount > 0 THEN amount ELSE 0 END) AS income,
                            SUM(CASE WHEN amount < 0 THEN amount ELSE 0 END) AS cost,
                            SUM(amount) AS total
            FROM transactions
                            """)
        
        income , cost , total = self.cursor.fetchone()
        self.connection.close()

        return income or 0, abs(cost or 0) , total or 0
    def get_sum(self):
        self.connection = sqlite3.connect(self.__db_name__)
        self.cursor = self.connection.cursor()
        self.cursor.execute("""SELECT SUM(amount) AS total FROM transactions""")
        total = self.cursor.fetchone()
        self.connection.close()
        return total

# =============================Database

db = None
db = Database("finance.db")

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
frame_three.rowconfigure(0 , weight=1)

lbl_total_value=Label(frame_one , text ="مجموع کل " , font = vazir_font, justify="center")
lbl_total_value.grid(row = 1 ,column=0)
lbl_income_value=Label(frame_one, text = "درامد" , font = vazir_font, justify="center")
lbl_income_value.grid(row = 1,column=1)
lbl_cost_value = Label(frame_one, text =" هزینه " , font = vazir_font , justify="center")
lbl_cost_value.grid(row = 1 ,column=2 )

def update_summary():
    income , cost , total = db.get_summary()

    lbl_income_value.config(text=f"{income:,}")
    lbl_cost_value.config(text=f"{cost:,}")
    lbl_total_value.config(text=f"{total:,}")

lal_sum=Label(frame_one , text ="مجموع کل " , font = vazir_font, justify="center")
lal_sum.grid(row = 0 ,column=0)
lal_income=Label(frame_one, text = "درامد" , font = vazir_font, justify="center")
lal_income.grid(row = 0,column=1)
lal_cost = Label(frame_one, text =" هزینه "  , font = vazir_font , justify="center")
lal_cost.grid(row = 0,column=2 )

lal_amount =Label(frame_two , text = "مبلغ" , font = vazir_font, justify="center" )
lal_amount.grid(row=0 , column=0 )
ent_amount = Entry(frame_two, font = vazir_font, justify="center")
ent_amount.grid(row=0 , column= 1 , sticky="ew")

lal_description =Label(frame_two , text = "توضیحات" , font = vazir_font, justify="center" )
lal_description.grid(row=1 , column =0)
ent_description= Entry(frame_two, font = vazir_font, justify="center")
ent_description.grid(row=1 , column= 1 , sticky="sn")

# # ==============================کلید واریز و برداشت 
# def deposit():
#     if not amount: 
#         amount =int(ent_amount.get())


# ======================================

# با کلیک روی هر دکمه صفحه جدید مخصوص خودش باز بشه 
# ==================(فیلتر هم همینجا اضافه میکنیم)نمایش تراکنش ها 
def transactions():
    win = Toplevel()
    win.title("transactions list")
    win.geometry("700x500")
    win.columnconfigure(0 , weight= 1)
    win.rowconfigure(0 , weight= 1)
    win.rowconfigure(1 , weight= 9)
    lal_transactions = Label(win , text = "transactions",font = vazir_font, justify="center" )
    lal_transactions.grid(row=0 , column=0)
    list_box = Listbox(win,font = vazir_font )
    list_box.grid(row=1 , column=0 , sticky="snew" )
    list_box.delete(0, END)
    result= db.get_all_transactions()
    for i in result:
            transaction = (
                f"ID:{i[0]} | "
                f"amount:{i[1]} | "
                f"type:{i[2]} | "
                f"date:{i[3]} | "
                f"description:{i[4]} "
            )
            index = list_box.size()
            list_box.insert(END, transaction)

            if i[2] == "withdraw":
                list_box.itemconfig(index , bg = "#ff6b6b")  #red
            else :
                list_box.itemconfig(index, bg="#b7f7c1")  # light green


bot_transactions = Button(frame_three , text = "نمایش تراکنش ها",font = vazir_font, justify="center" , command=transactions)
bot_transactions.grid(row=0 , column=0)

#==================== جستجو 

def search():
    win = Toplevel()
    win.title("seach transaction")
    win.geometry("500x500")
    win.columnconfigure(0 , weight= 1)
    win.columnconfigure(1 , weight= 1)
    win.rowconfigure(0 , weight= 1)
    win.rowconfigure(1 , weight= 1)
    win.rowconfigure(2 , weight= 9)

    lal_search_amount = Label(win , text = "search amount",font = vazir_font, justify="center" )
    lal_search_amount.grid(row=0 , column=0)
    ent_search_amount = Entry(win ,font = vazir_font, justify="center")
    ent_search_amount.grid(row=0 , column=1)
    lal_search_date = Label(win , text = "search date ",font = vazir_font, justify="center" )
    lal_search_date.grid(row=1 , column=0)
    ent_search_date = Entry(win ,font = vazir_font, justify="center")
    ent_search_date.grid(row=1 , column=1)

    list_box = Listbox(win ,font = vazir_font)
    list_box.grid(row=2 , column=0  , columnspan= 2, sticky="snew")
    def entry_key_release(key ):    
        list_box.delete(0, END)
        date= ent_search_date.get()
        amount_text = ent_search_amount.get()
        result= db.get_all_transactions()
        for i in result:
                show = True
                if amount_text:
                    try:
                        amount = int(amount_text)
                        if abs(i[1]) != amount:
                            show = False
                    except ValueError:
                        show = False
                if date:
                    if date != i[3].split(" ")[0]:
                        show = False
                if show:
                    transaction = (
                        f"ID:{i[0]} | "
                        f"amount:{i[1]} | "
                        f"type:{i[2]} | "
                        f"date:{i[3]} | "
                        f"description:{i[4]} "
                    )
                    index = list_box.size()
                    list_box.insert(END , transaction)

                    if i[2] == "withdraw":
                        list_box.itemconfig(index , bg = "#ff6b6b")
                    else :
                        list_box.itemconfig(index, bg="#b7f7c1")  
                    # if amount == "":
                    #     if date == i[3].split(" ")[0]:
                    #         list_box.insert(END, transaction)
                    #         if i[2] == "withdraw":
                    #             list_box.itemconfig(index , bg = "#ff6b6b")  #red
                    #         else :
                    #             list_box.itemconfig(index, bg="#b7f7c1")  # light green
                    # else :
                    #     pass
                # elif date =="":
                #     amount = int(amount)
                #     if amount == i [1]:
                #         list_box.insert(END, transaction)
                #         if i[2] == "withdraw":
                #             list_box.itemconfig(index , bg = "#ff6b6b")  #red
                #         else :
                #             list_box.itemconfig(index, bg="#b7f7c1")  # light green
                #     else :
                #         pass
                # else :
                #     amount=int(amount)
                #     if amount == i [1] and date == i[3].split(" ")[0]:
                #         list_box.insert(END, transaction)
                #         if i[2] == "withdraw":
                #             list_box.itemconfig(index , bg = "#ff6b6b")  #red
                #         else :
                #             list_box.itemconfig(index, bg="#b7f7c1")  # light green
                #     else :
                #         pass


    ent_search_amount.bind('<KeyRelease>' , entry_key_release)
    ent_search_date.bind('<KeyRelease>' , entry_key_release)

bot_search = Button(frame_three , text = "جستجو",font = vazir_font, justify="center" , command = search)
bot_search.grid(row=0 , column=1)



def deposit():
    x = ent_amount.get()
    y = ent_description.get()
    if not x :
        messagebox.showerror("error" , "اول مبلغ را وارد کنید")
        return
    try:
        u = float(x)
    except ValueError:
        messagebox.showerror("error" , "مبلغ باید عدد باشد")
        ent_amount.delete(0 , END)
        ent_description.delete(0 , END)
        return
    if u < 0 :
        messagebox.showerror("error" , "مبلغ غیر قابل قبول")
        ent_amount.delete(0 , END)
        ent_description.delete(0 , END)
        return
    elif u == 0 :
        messagebox.showerror("error" , "مبلغ کمتر از حد قابل قبول")
        ent_amount.delete(0 , END)
        ent_description.delete(0 , END)
        return
    else:
        db.add_transaction(u , "deposite"  , y)
        update_summary()
        messagebox.showinfo("done" , "done")
    ent_amount.delete(0 , END)
    ent_description.delete(0 , END)

bot_deposit = Button(frame_two , text = " دریافت" , bg= "green" ,font = vazir_font, justify="center", command= deposit )
bot_deposit.grid(row=0 , column=2 , sticky= "ns")


def withdraw():
    x = ent_amount.get()
    y = ent_description.get()
    total = db.get_sum()
    print(total[0])
    if not x :
        messagebox.showerror("error" , "اول مبلغ را وارد کنید")
        ent_amount.delete(0 , END)
        ent_description.delete(0 , END)
        return
    try:
        u = float(x)
    except ValueError:
        messagebox.showerror("error" , "مبلغ باید عدد باشد")
        ent_amount.delete(0 , END)
        ent_description.delete(0 , END)
        return
    if u < 0 :
        messagebox.showerror("error" , "مبلغ غیر قابل قبول")
        ent_amount.delete(0 , END)
        ent_description.delete(0 , END)
        return
    elif u == 0 :
        messagebox.showerror("error" , "مبلغ کمتر از حد قابل قبول")
        ent_amount.delete(0 , END)
        ent_description.delete(0 , END)
        return
    elif u > int(total[0]):
        y = messagebox.askyesno("error" , "موجودی نداری... میخوای منفی بشه ؟ ")
        if not y :
            return
    u = -u
    db.add_transaction(u , "withdraw"  , y)
    update_summary()
    messagebox.showinfo("done" , "done")
    ent_amount.delete(0 , END)
    ent_description.delete(0 , END)

bot_withdraw = Button(frame_two , text = "پرداخت" , bg= "red", font = vazir_font, justify="center" , command=withdraw)
bot_withdraw.grid(row=1, column=2 , sticky= "ns")



update_summary()
window.mainloop()