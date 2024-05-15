import pandas as pd
import os
import sys
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import numpy as np
import mysql.connector

#Hiii, my name is Athanasios Tasis and I am an undergraduate student at University of Patras, this is a python project about handling big data, creating a user-friednly GUI
#and visualizing them so we have a better understanding.

data1 = pd.read_csv("C:\\Users\\tasis\\Desktop\\sxoli\\code\\python\\hotel_booking.csv") #path to the csv file

months = ["0", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"] # all months of a year. "0" is inserted at first position
# of the array so that each month matches the actually number of month. January = 1, February = 2 etc.

def sql_data_transfer(data):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="admin",
            database="python_program"
        )
        cursor = conn.cursor()

        cursor.execute(data)

        conn.commit()
        conn.close()
        print("Data inserted successfully.")

    except mysql.connector.Error as error:
        print("Error:", error)


stays = []
percentage_stays = []

def restart_program():  # a function to restart the whole proccess. we are going to use it later for memory-saving purposses
    python = sys.executable
    os.execl(python, python, *sys.argv)

def data_allocation(): #this function seperates the data of the resort hotel from the data of city hotel upon user selection
    global data
    global total_count
    global hotel_selection
    if(hotel_selection == 0): 
        data = data1[data1['hotel'] == 'Resort Hotel']
        total_count = len(data) #length of all of resort hotel data(bookings of resort hotel + cancelled ones)
    else:
        data = data1[data1['hotel'] == 'City Hotel']
        total_count = len(data)


def cancellation_rate():
    data_allocation() #every time a hotel selection will be made so we can calculate statistics seperatly
    not_cancelled = (data['is_canceled'] == 0).sum() #the sum of not cancelled bookings
    cancelled = (data['is_canceled'] == 1).sum() #sum of cancelled bookings
    percentage_not_cancelled = (not_cancelled / total_count) * 100   #percentage of not cancelled bookings
    percentage_canceled = (cancelled / total_count) * 100   #percentage of cancelled bookings
    message = "Percentage of not canceled bookings is: {:.2f}%\n\nPercentage of canceled bookings is: {:.2f}%".format(percentage_not_cancelled, percentage_canceled)
    messagebox.showinfo("Info", message) # pop up with the results

#average stays for hotel
def average_stays():
    data_allocation()
    average_stays = (data['stays_in_weekend_nights'].sum() + data['stays_in_week_nights'].sum() ) / total_count #calculates the average stays of each booking
    message = "Average days per booking is {:.1f}".format(average_stays)
    messagebox.showinfo("Info", message)

#distribution of bookings per month in hotel
def month_distribution():
    data_allocation()
    stays.append(0) # stays is an array that stores the bookings of each month, it will help us later
    stays.append((data['arrival_date_month'] == 'January').sum() )
    stays.append((data['arrival_date_month'] == 'February').sum())
    stays.append((data['arrival_date_month'] == 'March').sum())
    stays.append((data['arrival_date_month'] == 'April').sum())
    stays.append((data['arrival_date_month'] == 'May').sum())
    stays.append((data['arrival_date_month'] == 'June').sum())
    stays.append((data['arrival_date_month'] == 'July').sum())
    stays.append((data['arrival_date_month'] == 'August').sum())
    stays.append((data['arrival_date_month'] == 'September').sum())
    stays.append((data['arrival_date_month'] == 'October').sum())
    stays.append((data['arrival_date_month'] == 'November').sum())
    stays.append((data['arrival_date_month'] == 'December').sum())



#percentage distribution of bookings per month in hotel
def percentage_distribution():
    month_distribution() # we store in stays[] variable the booking of each month
    for i in range(13):
        percentage_stays.append((stays[i] / total_count) * 100) #we calculate the bookings of each month compared to the totel stays of the year


#monthly bookings for each month at hotel
def monthly_stays(): #a function of printing the results of the 2 above functions
    percentage_distribution()
    message = ""
    for i in range(13):
        message += "Bookings for month {} are: {} and the percentage of bookings against the year is: {:.2f}%\n\n".format(i, stays[i], percentage_stays[i])
    messagebox.showinfo("Info", message)

    x = months
    y = stays


    plt.bar(x, y) # we plot the results at a "bar" type diagram
    plt.title("Distribution of monthly bookings")
    plt.legend(["No. of bookings"])
    plt.show()




#distribution of bookings based on the season in hotel
def seasonal_stays(): # this function calculates the bookings for each season with the help of the previous functions by adding the results of 3 months based on the season.
    #we know windter is month 12, 1, and 2 so we can add them up and create new statistics
    percentage_distribution()
    message = ("Stays in winter total up to: {} and the percentage of bookings against other seasons is {:.2f}%\n\n"
           "Stays in spring total up to: {} and the percentage of bookings against other seasons is {:.2f}%\n\n"
           "Stays in summer total up to: {} and the percentage of bookings against other seasons is {:.2f}%\n\n"
           "Stays in autumn total up to: {} and the percentage of bookings against other seasons is {:.2f}%\n\n").format(
               stays[12] + stays[1] + stays[2], percentage_stays[12] + percentage_stays[1] + percentage_stays[2],
               stays[3] + stays[4] + stays[5], percentage_stays[3] + percentage_stays[4] + percentage_stays[5],
               stays[6] + stays[7] + stays[8], percentage_stays[6] + percentage_stays[7] + percentage_stays[8],
               stays[9] + stays[10] + stays[11], percentage_stays[9] + percentage_stays[10] + percentage_stays[11])

    
    
    messagebox.showinfo("Info", message)
    
    
    
    y = ([stays[12] + stays[1] + stays[2], stays[3] + stays[4] + stays[5], stays[6] + stays[7] + stays[8], stays[9] + stays[10] + stays[11]])
    my_labels = ["WINTER", "SPRING", "SUMMER", "AUTUMN"]
    my_explode = [0.1, 0.1, 0.1, 0.1]
    plt.pie(y, labels = my_labels, explode=my_explode,shadow=True) # plot them as a pie diagram which will help us undestand the graph better
    plt.legend()
    plt.show()






#distribution of bookings per room type in hotel
def room_stays():
    data_allocation()
    start_ascii = ord('A')
    end_ascii = ord('P')
    percentage = []

    current_ascii = start_ascii

    message = ""
    while current_ascii <= end_ascii:
        letter = chr(current_ascii)
        num_bookings = (data['assigned_room_type'] == letter).sum()
        percentage_0 = (num_bookings / total_count) * 100
        percentage.append(percentage_0)
        message += "Number of bookings for type {} room: {} and the percentage is: {:.2f}%\n\n".format(letter, num_bookings, percentage_0)
        current_ascii += 1

    messagebox.showinfo("Info", message)
    y = percentage
    my_labels = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P"]
    plt.pie(y, labels = my_labels ,shadow=True, autopct='%1.1f%%') # plot them as a pie diagram which will help us undestand the graph better
    plt.legend()
    plt.show()



#distribution based on independant travellers, families and couples in hotel

def traveller_distribution():
    data_allocation()
    individual = ((data['adults'] == 1) & (data['children'] == 0) & (data['babies'] == 0)).sum() #here we seperate each kind of traveller by looking at the data of the csv file
# individuals of course will be only 1 without any children. families should always have at least 1 children and 1 adult(but children cannot book so adult isnt calculated)
#couples should be only 2 adults, and the remaining guests are other type of travellers. preatty simple and straigt-forward calculations here
    family = (((data['children'] > 0) | (data['babies'] > 0))).sum()

    couples =  (((data['adults'] == 2) & (data['children'] == 0) & (data['babies'] == 0) )).sum()

    other = total_count - individual - family - couples

    message = ("For the resort hotel, there are {} individual travelers, {} families, {} couples, and {} other kind of travellers.\n\n"
           "Individual travellers acquire {:.2f}%, families acquire {:.2f}%, couples acquire {:.2f}%, and other kind of travellers acquire {:.2f}%.").format(
               individual, family, couples, other,
               (individual / total_count) * 100, (family / total_count) * 100,
               (couples / total_count) * 100, (other / total_count) * 100)

    messagebox.showinfo("Info", message)

    y = [individual, family, couples, other]
    my_labels = ["Individuals", "Families", "Couples", "Other"]
    my_explode = [0.1, 0.1, 0.1, 0.1]
    plt.pie(y, labels = my_labels, explode=my_explode,shadow=True) #again a pie diagram with an explode of 0.1 so each slice is seperated from the others
    plt.legend()
    plt.show()


# changes in the market of tourism over time
def changes_over_time():
    data_allocation()
    
    cancellations_2015 = []
    cancellations_2016 = []
    cancellations_2017 = []
    total_count_2015 = (data["arrival_date_year"] == 2015).sum()
    total_count_2016 = (data["arrival_date_year"] == 2016).sum()
    total_count_2017 = (data["arrival_date_year"] == 2017).sum()
    
    for i in range(0, 13):
        month_cancel_count_2015 = (data["is_canceled"] == 1) & (data["arrival_date_month"] == months[i]) & (data["arrival_date_year"] == 2015)
        cancellations_2015.insert(i, ((month_cancel_count_2015.sum() / total_count_2015) *100)) # calculated the percentage of calcelled bookings only for 2015
    
    for i in range(0, 13):
        month_cancel_count_2016 = (data["is_canceled"] == 1) & (data["arrival_date_month"] == months[i]) & (data["arrival_date_year"] == 2016)
        cancellations_2016.insert(i, ((month_cancel_count_2016.sum() / total_count_2016) *100)) #the same for 2016 and so on

    for i in range(0, 13):
        month_cancel_count_2017 = (data["is_canceled"] == 1) & (data["arrival_date_month"] == months[i]) & (data["arrival_date_year"] == 2017)
        cancellations_2017.insert(i, ((month_cancel_count_2017.sum() / total_count_2017) *100))


    plt.stackplot(months, cancellations_2015, cancellations_2016, cancellations_2017, colors =['r', 'c', 'b'])
    plt.xlabel('Months')
    plt.ylabel('Percentage cancellations')
    plt.title('Percentage of cancellations each year')
    plt.tight_layout()
    plt.legend(['2015', '2016', '2017'], loc='upper left', fontsize=10)
    plt.show()

    def bookings_in_year():
        cancellations_2015 = []
        cancellations_2016 = []
        cancellations_2017 = []
        for i in range(0, 13):
            month_cancel_count_2015 = (data["is_canceled"] == 0) & (data["arrival_date_month"] == months[i]) & (data["arrival_date_year"] == 2015)
            cancellations_2015.insert(i, month_cancel_count_2015.sum()) # calculated the percentage of non-calcelled bookings only for 2015
    
        for i in range(0, 13):
            month_cancel_count_2016 = (data["is_canceled"] == 0) & (data["arrival_date_month"] == months[i]) & (data["arrival_date_year"] == 2016)
            cancellations_2016.insert(i, month_cancel_count_2016.sum()) #the same for 2016 and so on

        for i in range(0, 13):
            month_cancel_count_2017 = (data["is_canceled"] == 0) & (data["arrival_date_month"] == months[i]) & (data["arrival_date_year"] == 2017)
            cancellations_2017.insert(i, month_cancel_count_2017.sum())

        plt.stackplot(months, cancellations_2015, cancellations_2016, cancellations_2017, colors =['r', 'c', 'b'])
        plt.xlabel('Months')
        plt.ylabel('Bookings')
        plt.title('Bookings per year')
        plt.tight_layout()
        plt.legend(['2015', '2016', '2017'], loc='upper left', fontsize=10)
        plt.show()


    bookings_in_year()

def show_hotel_selection(callback):
    hotel_selection_window = tk.Toplevel(root)  # i create a new window for the options "resort hote" and "city hotel"
    hotel_selection_window.title("Select Hotel Name") 
    hotel_selection_window.geometry("600x350") # make the window big and visible to the user
    global hotel_selection  #access the global variable hotel_selection that is responsible for seperatig the data of the resort hotel and city hotel from the origianl given data
    def selected(option):  
        global hotel_selection
        if option == 0: #option 0 is resort hotel
            hotel_selection = 0
            hotel_selection_window.destroy() # closes the window
            callback()
            restart_program() # program is restarted so the arrays dont flood and for memory utilizetion purposes
        elif option ==1: #same as above
            hotel_selection = 1
            hotel_selection_window.destroy()
            callback()
            restart_program()

    resort_button = tk.Button(hotel_selection_window, text="Resort Hotel", command=lambda: selected(0), bd=8)
    resort_button.pack()

    city_button = tk.Button(hotel_selection_window, text="City Hotel", command=lambda: selected(1), bd=8)
    city_button.pack()


def on_button_click(option):   #here its a "switch" style creation. when the user presses a button it calls the show_hotel_selection function, with a parameter assigned to each button
    if option == "Average nights per booking":
        show_hotel_selection(average_stays)
    elif option == "Cancellation Rate":
        show_hotel_selection(cancellation_rate)
    elif option == "Distribution of bookings per month":
        show_hotel_selection(monthly_stays)
    elif option == "Distribution of bookings per season":
        show_hotel_selection(seasonal_stays)
    elif option == "Distribution of booking per room type":
        show_hotel_selection(room_stays)
    elif option == "Distribution based on traveller's type":
        show_hotel_selection(traveller_distribution)
    elif option == "See the changes in diffrent statistics over time":
        show_hotel_selection(changes_over_time)
    elif option == "EXIT":
        sys.exit()

    
# Create the main window
root = tk.Tk()
root.title("Thanaros Project in Python - CEID")  #name of my program
root.geometry('600x350')

# Create buttons
buttons = [   #here its an array of all the available options that will be available to the user
    "Average nights per booking",
    "Cancellation Rate",
    "Distribution of bookings per month",
    "Distribution of bookings per season",
    "Distribution of booking per room type",
    "Distribution based on traveller's type",
    "See the changes in diffrent statistics over time"
]

button = tk.Button(root, text="EXIT", command=lambda option="EXIT": on_button_click(option), pady=10, bg='#0af5dd', bd= 5, activebackground='#ff1a1a', activeforeground='#ffff33')
button.pack(anchor="nw")

for button_text in buttons: #I have created a loop that creates each button for each selection available to the user with some redish color and a dark red when you hit the button
    button = tk.Button(root, text=button_text, command=lambda option=button_text: on_button_click(option), pady=5, bg='#ff9999', bd= 5, activebackground='#ff1a1a', activeforeground='#ffff33')
    button.pack()

root.mainloop() #run the main programm. root is our main window 

#notice how i use a lot of functions. that is because i want to make sure not any uneccesary calculations are made and no any memory is used without a reason. by using loops
#the program uses as less memory as possible as only calculated the neccesary stuff. Really happy you read all that!! Athanasios Tasis - 1093503 - tasisinfo2@gmail.com
#up1093503@upnet.gr


sql_data_transfer()