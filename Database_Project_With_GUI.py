# Readme: 
# 1. Use the attached sql script file to set up the transitsystem database
# 2. Change the connection's condition using the username, password, host, port of your local/remote database accordingly
# 3. Run the code and login to the system using some predefined usernames and passwords like (admin1, password1), (admin2, password2)
# 4. After logging in to the program, choose any of the option to querry/modify the database (the inputted information must satisfy the 
# referential or data constraints of the entities in the database; an error will appear if a constraint is violated by the user's inputs)

from mysql.connector import connection
from mysql.connector.errors import Error
import tkinter as tk
from tkinter import messagebox
from tabulate import tabulate


class Authentication_GUI:
    '''A GUI for the authentication window.'''

    def __init__(self, master, conn, cursor):
        '''Initiate the menu GUI.'''

        self.master = master
        self.master.title('Authentication')
        self.conn = conn
        self.cursor = cursor

        # Introduction
        self.label = tk.Label(self.master, 
                              font = ('Helvetica', 11, 'bold'),
                              text='Pomona\'s Transit Management System')
        self.label.grid(row=0, column=0, columnspan=5)

        # Create entry box for user to enter the username
        self.usernameLabel = tk.Label(self.master, text='Username:')
        self.usernameLabel.grid(row=1, column=0)
        self.usernameEntryBox = tk.Entry(self.master, width=30, borderwidth=5)
        self.usernameEntryBox.grid(row=1, column=1)

        # Create entry box for user to enter the password
        self.passwordLabel = tk.Label(self.master, text='Password:')
        self.passwordLabel.grid(row=2, column=0)
        self.passwordEntryBox = tk.Entry(self.master, width=30, borderwidth=5)
        self.passwordEntryBox.grid(row=2, column=1)

        # Create 'Login' button to login to the application
        self.loginButton = tk.Button(self.master, text='Login', command=self.accessDB)
        self.loginButton.grid(row=3, column=0)

        # Create 'Quit' button to quit the application
        self.quitButton = tk.Button(self.master, text='Quit', fg='red', command=self.master.destroy)
        self.quitButton.grid(row=3, column=2)

    def accessDB(self):
        ''' Access the main menu if the login info is correct '''
        authenticate = self._validate_input(self.conn, self.cursor, 
                                            self.usernameEntryBox.get(), 
                                            self.passwordEntryBox.get())

        if authenticate != -1: # Login info is correct
            self.master.destroy() # close the authentication window
            self.master = tk.Tk() 
            self.db = Main_Menu_GUI(self.master, self.conn, self.cursor) # open the main menu
            self.master.mainloop()
        else:
            self._wrongLoginInfo()

    def _validate_input(self, conn, cursor, username, password) -> int:
        ''' Validate the username and password inputted by the user '''
        authenticate(cursor, conn) 
        cursor.execute(f"SELECT username from users WHERE Username='{username}' AND Password='{password}';")
        if not cursor.fetchone():
            return -1 # Username/Password is wrong
        else:
            return 1 # Username/Password is correct

    def _wrongLoginInfo(self) -> None:
        '''Display error if the login info is wrong.'''
        messagebox.showwarning(title='Login Failed', message='Invalid login info!\nPlease try again.')
        self._clear()

    def _clear(self) -> None:
        ''' Clear the textbox '''
        self.usernameEntryBox.delete(0, tk.END)
        self.passwordEntryBox.delete(0, tk.END)       


class Main_Menu_GUI:
    '''A GUI for the Connect Four Game.'''

    def __init__(self, master, conn, cursor):
        '''Initiate the game GUI.'''

        self.master = master
        self.master.title('Database System')  
        self.conn = conn
        self.cursor = cursor

        # Create the buttons for the user to choose an option
        options = tk.Label(self.master, text="Please choose an option below:")
        option1 = tk.Button(self.master, text="Display a Schedule of trips", command=lambda: displayScheduleGUI(self.cursor))
        option2 = tk.Button(self.master, text="Delete a Trip Offering", command=lambda: deleteTripOfferingGUI(self.cursor, self.conn))
        option3 = tk.Button(self.master, text="Add a Trip Offering", command=lambda: addTripOfferingGUI(self.cursor, self.conn))
        option4 = tk.Button(self.master, text="Change the Driver of a Trip Offering", command=lambda: changeDriverGUI(self.cursor, self.conn))
        option5 = tk.Button(self.master, text="Change the Bus of a Trip Offering", command=lambda: changeBusGUI(self.cursor, self.conn))
        option6 = tk.Button(self.master, text="Display a Trip's Stops", command=lambda: displayTripStopsGUI(self.cursor))
        option7 = tk.Button(self.master, text="Insert Actual Trip Info", command=lambda: insertTripDataGUI(self.cursor, self.conn))
        option8 = tk.Button(self.master, text="Add a Driver", command=lambda: addDriverGUI(self.cursor, self.conn))
        option9 = tk.Button(self.master, text="Add a Bus", command=lambda: addBusGUI(self.cursor, self.conn))
        option10 = tk.Button(self.master, text="Delete a Bus", command=lambda: deleteBusGUI(self.cursor, self.conn))
        option11 = tk.Button(self.master, text="Exit the program", fg='red', command=self.master.destroy)

        # Layout of the buttons
        options.grid(row = 0, column = 0)
        option1.grid(row = 1, column = 0)
        option2.grid(row = 2, column = 0)
        option3.grid(row = 3, column = 0)
        option4.grid(row = 4, column = 0)
        option5.grid(row = 5, column = 0)
        option6.grid(row = 6, column = 0)
        option7.grid(row = 7, column = 0)
        option8.grid(row = 8, column = 0)
        option9.grid(row = 9, column = 0)
        option10.grid(row = 10, column = 0)
        option11.grid(row = 11, column = 0)


class TabulateLabel(tk.Label):
    ''' Display extracted data in tab form '''

    def __init__(self, parent, data, **kwargs):
        super().__init__(parent, 
                         font=('Consolas', 10), 
                         justify=tk.LEFT, anchor='nw', **kwargs)

        text = tabulate(data, headers='firstrow', tablefmt='github', showindex=False)
        self.configure(text=text)


def displayScheduleGUI(cursor):
    ''' GUI: display the schedule of trips '''

    window1st = tk.Tk()

    # Introduction
    window1st.title('Display a schedule of trips')
    label = tk.Label(window1st, 
                     font = ('Helvetica', 11, 'bold'),
                     text='Display a schedule of trips')
    label.grid(row=0, column=0, columnspan=5)

    # Create entry box for user to enter the start location name
    startLocLabel = tk.Label(window1st, text='Enter the Start Location Name:')
    startLocLabel.grid(row=1, column=0)
    startLocEntryBox = tk.Entry(window1st, width=30, borderwidth=5)
    startLocEntryBox.grid(row=1, column=1)

    # Create entry box for user to enter the destination name
    destLocLabel = tk.Label(window1st, text='Enter the Destination Name:')
    destLocLabel.grid(row=2, column=0)
    destLocEntryBox = tk.Entry(window1st, width=30, borderwidth=5)
    destLocEntryBox.grid(row=2, column=1)

    # Create entry box for user to enter the date
    dateLabel = tk.Label(window1st, text='Enter the Date using the format "yyyy-MM-dd":')
    dateLabel.grid(row=3, column=0)
    dateEntryBox = tk.Entry(window1st, width=30, borderwidth=5)
    dateEntryBox.grid(row=3, column=1)

    # Create 'Display' button to display the stops of a given trip
    displayButton = tk.Button(window1st, text='Display',
                              command=lambda: displaySchedule(cursor, startLocEntryBox, 
                                                              destLocEntryBox, dateEntryBox))
    displayButton.grid(row=4, column=0)

    # Create 'Quit' button to exit
    exitButton = tk.Button(window1st, text='Exit', fg='red', 
                           command=window1st.destroy)        
    exitButton.grid(row=4, column=2)


def displaySchedule(cursor, 
                    startLocEntryBox, 
                    destLocEntryBox, 
                    dateEntryBox):
    ''' display the schedule of trips '''

    try:
        startLoc = startLocEntryBox.get()
        destLoc = destLocEntryBox.get()
        date= dateEntryBox.get()
        cursor.execute("SELECT T1.StartLocationName AS Start_Location, T1.DestinationName AS Destination, " +
                            "T0.Date, T0.ScheduledStartTime AS Scheduled_Start_Time, " +
                            "T0.ScheduledArrivalTime AS Scheduled_Arrival_Time, " +
                            "T0.DriverName, T0.BusID " +
                        "FROM TripOffering T0, Trip T1 " + 
                        "WHERE T1.StartLocationName LIKE '" + startLoc + "' AND " + 
                            "T1.DestinationName LIKE '" + destLoc + "' AND " + 
                            "T0.Date = '" + date + "' AND " + 
                            "T1.TripNumber = T0.TripNumber " + 
                        "Order by ScheduledStartTime ")
        row = cursor.fetchone()
        result = []
        if row:
            title = []
            for column in cursor.description:
                title.append(column[0])
            result.append(title)

            while row is not None:
                result.append(row)
                row = cursor.fetchone()

            windowResult = tk.Tk()
            windowResult.title('Result')
            TabulateLabel(windowResult, data=result, bg='white').grid(sticky='ew')
        else:
            messagebox.showwarning(title='Error',
                                   message="No data found for this trip.")
    except Error:
        messagebox.showwarning(title='Error',
                               message="No data found for this trip.")
    finally:  
        # Clear the textbox      
        startLocEntryBox.delete(0, tk.END)
        destLocEntryBox.delete(0, tk.END)
        dateEntryBox.delete(0, tk.END)
     

def deleteTripOfferingGUI(cursor, conn): 
    ''' GUI: delete a trip offering '''

    window2nd = tk.Tk()

    # Introduction
    window2nd.title('Delete a Trip Offering')
    label = tk.Label(window2nd, font = ('Helvetica', 11, 'bold'),
                     text='Delete a Trip Offering')
    label.grid(row=0, column=0, columnspan=5)

    # Create entry box for user to enter the trip number
    tripNoLabel = tk.Label(window2nd, text='Enter the trip Number:')
    tripNoLabel.grid(row=1, column=0)
    tripNoEntryBox = tk.Entry(window2nd, width=30, borderwidth=5)
    tripNoEntryBox.grid(row=1, column=1)

    # Create entry box for user to enter the date
    dateLabel = tk.Label(window2nd, text='Enter the Date using the format "yyyy-MM-dd":')
    dateLabel.grid(row=2, column=0)
    dateEntryBox = tk.Entry(window2nd, width=30, borderwidth=5)
    dateEntryBox.grid(row=2, column=1)

    # Create entry box for user to enter the scheduled start time
    scheduledStartTimeLabel = tk.Label(window2nd, text='Enter the scheduled Start Time:')
    scheduledStartTimeLabel.grid(row=3, column=0)
    scheduledStartTimeEntryBox = tk.Entry(window2nd, width=30, borderwidth=5)
    scheduledStartTimeEntryBox.grid(row=3, column=1)

    # Create 'Delete' button to delete the trip offering from the database
    deleteButton = tk.Button(window2nd, text='Delete',
                            command=lambda: deleteTripOffering(cursor, conn, 
                                                               tripNoEntryBox, dateEntryBox, 
                                                               scheduledStartTimeEntryBox))
    deleteButton.grid(row=4, column=0)

    # Create 'Quit' button to exit
    exitButton = tk.Button(window2nd, text='Exit', fg='red', command=window2nd.destroy)        
    exitButton.grid(row=4, column=2)


def deleteTripOffering(cursor, conn, 
                       tripNoEntryBox, 
                       dateEntryBox, 
                       scheduledStartTimeEntryBox):
    ''' delete a trip offering '''

    try:
        tripNo = tripNoEntryBox.get()
        date = dateEntryBox.get()
        scheduledStartTime = scheduledStartTimeEntryBox.get()
        cursor.execute("DELETE FROM TripOffering " + 
                        "WHERE TripNumber = '" + tripNo + "' AND " + 
                        "Date = '" + date + "' AND " + 
                        "ScheduledStartTime = '" + scheduledStartTime + "'")
        conn.commit()

        # If the deletion is successful, output a success message
        if cursor.rowcount:
            messagebox.showinfo(title='Success',
                                message="The inputted Trip Offering was successfully deleted.")
        else:
            messagebox.showwarning(title='Error',
                                   message="Error! The inputted Trip Offering does not exist.")
    except Error:
        messagebox.showwarning(title='Error',
                               message="Error! The inputted Trip Offering does not exist.")
    finally:        
        # Clear the textbox
        tripNoEntryBox.delete(0, tk.END)
        dateEntryBox.delete(0, tk.END)
        scheduledStartTimeEntryBox.delete(0, tk.END)

     
def addTripOfferingGUI(cursor, conn):
    ''' GUI: add trip offerings '''

    window3rd = tk.Tk()

    # Introduction
    window3rd.title('Add a Trip Offering')
    label = tk.Label(window3rd, font = ('Helvetica', 11, 'bold'),
                        text='Add a Trip Offering')
    label.grid(row=0, column=0, columnspan=5)

    # Create entry box for user to enter the trip number
    tripNoLabel = tk.Label(window3rd, text='Enter the trip number:')
    tripNoLabel.grid(row=1, column=0)
    tripNoEntryBox = tk.Entry(window3rd, width=30, borderwidth=5)
    tripNoEntryBox.grid(row=1, column=1)

    # Create entry box for user to enter the date
    dateLabel = tk.Label(window3rd, text='Enter the Date using the format "yyyy-MM-dd":')
    dateLabel.grid(row=2, column=0)
    dateEntryBox = tk.Entry(window3rd, width=30, borderwidth=5)
    dateEntryBox.grid(row=2, column=1)   

    # Create entry box for user to enter the scheduledStartTime
    scheduledStartTimeLabel = tk.Label(window3rd, text='Enter the scheduled start time:')
    scheduledStartTimeLabel.grid(row=3, column=0)
    scheduledStartTimeEntryBox = tk.Entry(window3rd, width=30, borderwidth=5)
    scheduledStartTimeEntryBox.grid(row=3, column=1) 

    # Create entry box for user to enter the scheduledArrivalTime
    scheduledArrivalTimeLabel = tk.Label(window3rd, text='Enter the scheduled arrival time:')
    scheduledArrivalTimeLabel.grid(row=4, column=0)
    scheduledArrivalTimeEntryBox = tk.Entry(window3rd, width=30, borderwidth=5)
    scheduledArrivalTimeEntryBox.grid(row=4, column=1) 

    # Create entry box for user to enter the Driver's name
    driverLabel = tk.Label(window3rd, text='Enter the Driver Name:')
    driverLabel.grid(row=5, column=0)
    driverEntryBox = tk.Entry(window3rd, width=30, borderwidth=5)
    driverEntryBox.grid(row=5, column=1) 

    # Create entry box for user to enter the bus ID
    busIDLabel = tk.Label(window3rd, text='Enter the Bus ID:')
    busIDLabel.grid(row=6, column=0)
    busIDEntryBox = tk.Entry(window3rd, width=30, borderwidth=5)
    busIDEntryBox.grid(row=6, column=1) 

    # Create 'Add' button to add the trip to the database
    addButton = tk.Button(window3rd, text='Add',
                            command=lambda: addTripOffering(cursor, conn, tripNoEntryBox, dateEntryBox, 
                                            scheduledStartTimeEntryBox, scheduledArrivalTimeEntryBox, 
                                            driverEntryBox, busIDEntryBox))
    addButton.grid(row=7, column=0)

    # Create 'Quit' button to exit
    exitButton = tk.Button(window3rd, text='Exit', fg='red', command=window3rd.destroy)        
    exitButton.grid(row=7, column=2)


def addTripOffering(cursor, conn, 
                    tripNoEntryBox, 
                    dateEntryBox, 
                    scheduledStartTimeEntryBox, 
                    scheduledArrivalTimeEntryBox, 
                    driverEntryBox, 
                    busIDEntryBox):
    ''' add trip offerings '''

    try:
        tripNo = tripNoEntryBox.get()
        date = dateEntryBox.get()
        scheduledStartTime = scheduledStartTimeEntryBox.get()
        scheduledArrivalTime = scheduledArrivalTimeEntryBox.get()
        driver = driverEntryBox.get()
        busID = busIDEntryBox.get()
        cursor.execute("INSERT INTO TripOffering VALUES ('" + tripNo + "', '" + date + "', '" + scheduledStartTime
             + "', '" + scheduledArrivalTime + "', '" + driver + "', '" + busID + "')")
        conn.commit()
        
        messagebox.showinfo(title='Success', message='The new Trip Offering was successfully added.')
    except Error:
        messagebox.showwarning(title='Error', message='Error! Please check the inputted data.')
    finally:
        # Clear the textbox
        tripNoEntryBox.delete(0, tk.END) 
        dateEntryBox.delete(0, tk.END) 
        scheduledStartTimeEntryBox.delete(0, tk.END) 
        scheduledArrivalTimeEntryBox.delete(0, tk.END) 
        driverEntryBox.delete(0, tk.END)       
        busIDEntryBox.delete(0, tk.END) 


def changeDriverGUI(cursor, conn):
    ''' GUI: change the driver of a given trip offering '''
    window4th = tk.Tk()

    # Introduction
    window4th.title('Change driver')
    label = tk.Label(window4th, font = ('Helvetica', 11, 'bold'),
                        text='Change the Driver of a Trip Offering')
    label.grid(row=0, column=0, columnspan=5)

    # Create entry box for user to enter the bus ID
    newDriverLabel = tk.Label(window4th, text='Enter the new Driver\'s Name:')
    newDriverLabel.grid(row=1, column=0)
    newDriverEntryBox = tk.Entry(window4th, width=30, borderwidth=5)
    newDriverEntryBox.grid(row=1, column=1)

    # Create entry box for user to enter the trip number
    tripNoLabel = tk.Label(window4th, text='Enter the Trip number:')
    tripNoLabel.grid(row=2, column=0)
    tripNoEntryBox = tk.Entry(window4th, width=30, borderwidth=5)
    tripNoEntryBox.grid(row=2, column=1)    

    # Create entry box for user to enter the date
    dateLabel = tk.Label(window4th, text="Enter the Date using the format 'yyyy-MM-dd':")
    dateLabel.grid(row=3, column=0)
    dateEntryBox = tk.Entry(window4th, width=30, borderwidth=5)
    dateEntryBox.grid(row=3, column=1)    

    # Create entry box for user to enter the scheduled start time
    scheduledStartTimeLabel = tk.Label(window4th, text="Enter the Scheduled Start Time:")
    scheduledStartTimeLabel.grid(row=4, column=0)
    scheduledStartTimeEntryBox = tk.Entry(window4th, width=30, borderwidth=5)
    scheduledStartTimeEntryBox.grid(row=4, column=1)    

    # Create 'Change' button to change the driver of a trip offering in the database
    changeButton = tk.Button(window4th, text='Change',
                            command=lambda: changeDriver(cursor, conn, 
                                                         newDriverEntryBox, tripNoEntryBox, 
                                                         dateEntryBox, scheduledStartTimeEntryBox))
    changeButton.grid(row=5, column=0)

    # Create 'Quit' button to exit
    exitButton = tk.Button(window4th, text='Exit', fg='red', command=window4th.destroy)        
    exitButton.grid(row=5, column=2)


def changeDriver(cursor, conn, 
                 newDriverEntryBox, 
                 tripNoEntryBox, 
                 dateEntryBox, 
                 scheduledStartTimeEntryBox):
    ''' change the driver of a given trip offering '''
    try:
        newDriver = newDriverEntryBox.get()
        tripNo = tripNoEntryBox.get()
        date = dateEntryBox.get()
        scheduledStartTime = scheduledStartTimeEntryBox.get()
        cursor.execute("UPDATE TripOffering " +
                                "SET DriverName = '" + newDriver + "' " +
                                "WHERE TripNumber = '" + tripNo + "' AND " +
                                "Date = '" + date + "' AND " +
                                "ScheduledStartTime = '" + scheduledStartTime + "'")
        conn.commit()
        if cursor.rowcount:
            messagebox.showinfo(title='Success',
                                message="The inputted Trip Offering was successfully updated with the new Driver.")
        else:
            messagebox.showwarning(title='Error',
                                   message='Error! Please check the inputted data.')
    except Error:
        messagebox.showwarning(title='Error',
                               message='Error! Please check the inputted data.')
    finally:       
        # Clear the textbox 
        newDriverEntryBox.delete(0, tk.END)
        tripNoEntryBox.delete(0, tk.END)
        dateEntryBox.delete(0, tk.END)
        scheduledStartTimeEntryBox.delete(0, tk.END)


def changeBusGUI(cursor, conn):
    ''' GUI: change the bus of a given trip offering '''

    window5th = tk.Tk()

    # Introduction
    window5th.title('Change bus')
    label = tk.Label(window5th, font = ('Helvetica', 11, 'bold'),
                        text='Change the bus of a trip offering')
    label.grid(row=0, column=0, columnspan=5)

    # Create entry box for user to enter the bus ID
    newBusIDLabel = tk.Label(window5th, text='Enter the new bus ID:')
    newBusIDLabel.grid(row=1, column=0)
    newBusIDEntryBox = tk.Entry(window5th, width=30, borderwidth=5)
    newBusIDEntryBox.grid(row=1, column=1)

    # Create entry box for user to enter the trip number
    tripNoLabel = tk.Label(window5th, text='Enter the Trip number:')
    tripNoLabel.grid(row=2, column=0)
    tripNoEntryBox = tk.Entry(window5th, width=30, borderwidth=5)
    tripNoEntryBox.grid(row=2, column=1)    

    # Create entry box for user to enter the date
    dateLabel = tk.Label(window5th, text="Enter the Date using the format 'yyyy-MM-dd':")
    dateLabel.grid(row=3, column=0)
    dateEntryBox = tk.Entry(window5th, width=30, borderwidth=5)
    dateEntryBox.grid(row=3, column=1)    

    # Create entry box for user to enter the scheduled start time
    scheduledStartTimeLabel = tk.Label(window5th, text='Enter the Scheduled Start Time:')
    scheduledStartTimeLabel.grid(row=4, column=0)
    scheduledStartTimeEntryBox = tk.Entry(window5th, width=30, borderwidth=5)
    scheduledStartTimeEntryBox.grid(row=4, column=1)    

    # Create 'Change' button to change the bus of a trip offering in the database
    changeButton = tk.Button(window5th, text='Change',
                             command=lambda: changeBus(cursor, conn, 
                                                      newBusIDEntryBox, tripNoEntryBox, 
                                                      dateEntryBox, scheduledStartTimeEntryBox))
    changeButton.grid(row=5, column=0)

    # Create 'Quit' button to exit
    exitButton = tk.Button(window5th, text='Exit', fg='red', command=window5th.destroy)        
    exitButton.grid(row=5, column=2)


def changeBus(cursor, conn, 
              newBusIDEntryBox, 
              tripNoEntryBox, 
              dateEntryBox, 
              scheduledStartTimeEntryBox):
    ''' change the bus of a given trip offering '''

    try:
        newBusID = newBusIDEntryBox.get()
        tripNo = tripNoEntryBox.get()
        date = dateEntryBox.get()
        scheduledStartTime = scheduledStartTimeEntryBox.get()
        cursor.execute("UPDATE TripOffering " +
                                "SET BusID = '" + newBusID + "' " +
                                "WHERE TripNumber = '" + tripNo + "' AND " +
                                "Date = '" + date + "' AND " +
                                "ScheduledStartTime = '" + scheduledStartTime + "'")
        conn.commit()
        if cursor.rowcount:
            messagebox.showinfo(title='Success',
                                message="The inputted Trip Offering was successfully updated with the new Bus ID.")
        else:
            messagebox.showwarning(title='Error',
                                   message='Error! Please check the inputted data.')
    except Error:
        messagebox.showwarning(title='Error',
                               message='Error! Please check the inputted data.')
    finally:        
        # Clear the textbox
        newBusIDEntryBox.delete(0, tk.END)
        tripNoEntryBox.delete(0, tk.END)
        dateEntryBox.delete(0, tk.END)
        scheduledStartTimeEntryBox.delete(0, tk.END)
    

def displayTripStopsGUI(cursor):
    ''' GUI: display the stops of a given trips '''

    window6th = tk.Tk()

    # Introduction
    window6th.title('Display the stops of a given trip')
    label = tk.Label(window6th, font = ('Helvetica', 11, 'bold'),
                        text='Display the stops of a given trip')
    label.grid(row=0, column=0, columnspan=5)

    # Create entry box for user to enter the trip number
    tripNoLabel = tk.Label(window6th, text='Enter the tripNo\'s Name:')
    tripNoLabel.grid(row=1, column=0)
    tripNoEntryBox = tk.Entry(window6th, width=30, borderwidth=5)
    tripNoEntryBox.grid(row=1, column=1)

    # Create 'Display' button to display the stops of a given trip
    displayButton = tk.Button(window6th, text='Display',
                              command=lambda: displayTripStops(cursor, tripNoEntryBox))
    displayButton.grid(row=2, column=0)

    # Create 'Quit' button to exit
    exitButton = tk.Button(window6th, text='Exit', fg='red', command=window6th.destroy)        
    exitButton.grid(row=2, column=2)


def displayTripStops(cursor, tripNoEntryBox):
    ''' display the stops of a given trips '''

    try:
        tripNo = tripNoEntryBox.get()
        cursor.execute("SELECT * FROM TripStopInfo "+
                                "WHERE TripNumber = '" + tripNo + "' " +
                                "Order By SequenceNumber ")
        row = cursor.fetchone()
        result = []
        if row:
            title = []
            for column in cursor.description:
                title.append(column[0])
            result.append(title)

            while row is not None:
                result.append(row)
                row = cursor.fetchone()

            windowResult = tk.Tk()            
            windowResult.title('Result')
            TabulateLabel(windowResult, data=result, bg='white').grid(sticky='ew')
        else:
            messagebox.showwarning(title='Error',
                                    message="The inputted Trip Number = " + tripNo + " does not exist")
    except Error:
        messagebox.showwarning(title='Error',
                               message="The inputted Trip Number = " + tripNo + " does not exist")
    finally:       
        # Clear the textbox 
        tripNoEntryBox.delete(0, tk.END)


def insertTripDataGUI(cursor, conn):
    ''' GUI: insert the actual data of a given trip '''

    window7th = tk.Tk()

    # Introduction
    window7th.title('Insert an actual trip/stop info')
    label = tk.Label(window7th, font = ('Helvetica', 11, 'bold'),
                        text='Insert an actual trip info')
    label.grid(row=0, column=0, columnspan=5)

    # Create entry box for user to enter the trip number
    tripNoLabel = tk.Label(window7th, text='Enter the trip number:')
    tripNoLabel.grid(row=1, column=0)
    tripNoEntryBox = tk.Entry(window7th, width=30, borderwidth=5)
    tripNoEntryBox.grid(row=1, column=1)

    # Create entry box for user to enter the date
    dateLabel = tk.Label(window7th, text='Enter the Date using the format "yyyy-MM-dd":')
    dateLabel.grid(row=2, column=0)
    dateEntryBox = tk.Entry(window7th, width=30, borderwidth=5)
    dateEntryBox.grid(row=2, column=1)   

    # Create entry box for user to enter the scheduled Start Time
    scheduledStartTimeLabel = tk.Label(window7th, text='Enter the scheduled start time:')
    scheduledStartTimeLabel.grid(row=3, column=0)
    scheduledStartTimeEntryBox = tk.Entry(window7th, width=30, borderwidth=5)
    scheduledStartTimeEntryBox.grid(row=3, column=1) 

    # Create entry box for user to enter the stop number
    stopLabel = tk.Label(window7th, text='Enter the stop number:')
    stopLabel.grid(row=4, column=0)
    stopEntryBox = tk.Entry(window7th, width=30, borderwidth=5)
    stopEntryBox.grid(row=4, column=1) 

    # Create entry box for user to enter the scheduled Arrival Time
    scheduledArrivalTimeLabel = tk.Label(window7th, text='Enter the scheduled arrival time:')
    scheduledArrivalTimeLabel.grid(row=5, column=0)
    scheduledArrivalTimeEntryBox = tk.Entry(window7th, width=30, borderwidth=5)
    scheduledArrivalTimeEntryBox.grid(row=5, column=1) 

    # Create entry box for user to enter the actual Start Time
    actualStartTimeLabel = tk.Label(window7th, text='Enter the actual start time:')
    actualStartTimeLabel.grid(row=6, column=0)
    actualStartTimeEntryBox = tk.Entry(window7th, width=30, borderwidth=5)
    actualStartTimeEntryBox.grid(row=6, column=1) 

    # Create entry box for user to enter the actual Arrival Time
    actualArrivalTimeLabel = tk.Label(window7th, text='Enter the actual arrival time:')
    actualArrivalTimeLabel.grid(row=7, column=0)
    actualArrivalTimeEntryBox = tk.Entry(window7th, width=30, borderwidth=5)
    actualArrivalTimeEntryBox.grid(row=7, column=1) 

    # Create entry box for user to enter the passengers on board
    passengersInLabel = tk.Label(window7th, text='Enter the number of passengers in:')
    passengersInLabel.grid(row=8, column=0)
    passengersInEntryBox = tk.Entry(window7th, width=30, borderwidth=5)
    passengersInEntryBox.grid(row=8, column=1) 

    # Create entry box for user to enter the passengers exits
    passengersOutLabel = tk.Label(window7th, text='Enter the number of passengers out:')
    passengersOutLabel.grid(row=9, column=0)
    passengersOutEntryBox = tk.Entry(window7th, width=30, borderwidth=5)
    passengersOutEntryBox.grid(row=9, column=1)  

    # Create 'Add' button to add the trip to the database
    addButton = tk.Button(window7th, text='Add',
                            command=lambda: insertTripData(cursor, conn, 
                                                           tripNoEntryBox, 
                                                           dateEntryBox, 
                                                           scheduledStartTimeEntryBox, 
                                                           stopEntryBox, 
                                                           scheduledArrivalTimeEntryBox, 
                                                           actualStartTimeEntryBox, 
                                                           actualArrivalTimeEntryBox, 
                                                           passengersInEntryBox, 
                                                           passengersOutEntryBox))
    addButton.grid(row=10, column=0)

    # Create 'Quit' button to exit
    exitButton = tk.Button(window7th, text='Exit', fg='red', command=window7th.destroy)        
    exitButton.grid(row=10, column=2)

def insertTripData(cursor, conn, 
                   tripNoEntryBox, 
                   dateEntryBox, 
                   scheduledStartTimeEntryBox, 
                   stopEntryBox, 
                   scheduledArrivalTimeEntryBox, 
                   actualStartTimeEntryBox, 
                   actualArrivalTimeEntryBox, 
                   passengersInEntryBox, 
                   passengersOutEntryBox):
    ''' insert the actual data of a given trip '''

    try:
        tripNo = tripNoEntryBox.get()
        date = dateEntryBox.get()
        scheduledStartTime = scheduledStartTimeEntryBox.get()
        stop = stopEntryBox.get()
        scheduledArrivalTime = scheduledArrivalTimeEntryBox.get()
        actualStartTime = actualStartTimeEntryBox.get()
        actualArrivalTime = actualArrivalTimeEntryBox.get()
        passengersIn = passengersInEntryBox.get()
        passengersOut = passengersOutEntryBox.get()
        cursor.execute("INSERT INTO ActualTripStopInfo VALUES ('" + tripNo + "', '" + date + "', '" + scheduledStartTime + "', '" + stop + "', '" + scheduledArrivalTime
                    + "', '" + actualStartTime + "', '" + actualArrivalTime + "', '" + passengersIn + "', '" + passengersOut + "')")
        conn.commit()
        messagebox.showinfo(title='Success', message='The actual data of the given trip offering was successfully recorded.')
    
    except Error:
        messagebox.showwarning(title='Error', message='Error! Please check the inputted data.')
    
    finally:
        # Clear the textbox
        tripNoEntryBox.delete(0, tk.END) 
        dateEntryBox.delete(0, tk.END) 
        scheduledStartTimeEntryBox.delete(0, tk.END) 
        stopEntryBox.delete(0, tk.END) 
        scheduledArrivalTimeEntryBox.delete(0, tk.END) 
        actualStartTimeEntryBox.delete(0, tk.END) 
        actualArrivalTimeEntryBox.delete(0, tk.END) 
        passengersInEntryBox.delete(0, tk.END) 
        passengersOutEntryBox.delete(0, tk.END)     


def addDriverGUI(cursor, conn):
    ''' GUI: add a driver '''

    window8th = tk.Tk()

    # Introduction
    window8th.title('Add a driver')
    label = tk.Label(window8th, font = ('Helvetica', 11, 'bold'),
                     text='Add a driver')
    label.grid(row=0, column=0, columnspan=5)

    # Create entry box for user to enter the driver's name
    driverLabel = tk.Label(window8th, text='Enter the Driver\'s Name:')
    driverLabel.grid(row=1, column=0)
    driverEntryBox = tk.Entry(window8th, width=30, borderwidth=5)
    driverEntryBox.grid(row=1, column=1)

    # Create entry box for user to enter the phone number
    phoneNoLabel = tk.Label(window8th, text='Enter the Driver\'s Phone number:')
    phoneNoLabel.grid(row=2, column=0)
    phoneNoEntryBox = tk.Entry(window8th, width=30, borderwidth=5)
    phoneNoEntryBox.grid(row=2, column=1)    

    # Create 'Add' button to add the driver to the database
    addButton = tk.Button(window8th, text='Add',
                            command=lambda: addDriver(cursor, conn, 
                                                      driverEntryBox, phoneNoEntryBox))
    addButton.grid(row=3, column=0)

    # Create 'Quit' button to exit
    exitButton = tk.Button(window8th, text='Exit', fg='red', command=window8th.destroy)        
    exitButton.grid(row=3, column=2)


def addDriver(cursor, conn, driverEntryBox, phoneNoEntryBox):
    ''' add a driver '''
    try:
        driver = driverEntryBox.get()
        phoneNo = phoneNoEntryBox.get()
        cursor.execute("INSERT INTO Driver VALUES ('" + driver + "', '" + phoneNo + "')")
        conn.commit()
        messagebox.showinfo(title='Success',
                               message="Driver's name = " + driver + " was successfully added!")
    except Error:
        messagebox.showwarning(title='Error',
                               message='Error! Please check the inputted data.')
    finally:     
        # Clear the textbox   
        driverEntryBox.delete(0, tk.END)
        phoneNoEntryBox.delete(0, tk.END)


def addBusGUI(cursor, conn):
    ''' GUI: add a bus '''

    window9th = tk.Tk()

    # Introduction
    window9th.title('Add a bus')
    label = tk.Label(window9th, font = ('Helvetica', 11, 'bold'),
                     text='Add a bus')
    label.grid(row=0, column=0, columnspan=5)

    # Create entry box for user to enter the bus ID
    busIDLabel = tk.Label(window9th, text='Enter the bus\'s ID:')
    busIDLabel.grid(row=1, column=0)
    busIDEntryBox = tk.Entry(window9th, width=30, borderwidth=5)
    busIDEntryBox.grid(row=1, column=1)

    # Create entry box for user to enter the bus's model
    busModelLabel = tk.Label(window9th, text='Enter the bus\'s model:')
    busModelLabel.grid(row=2, column=0)
    busModelEntryBox = tk.Entry(window9th, width=30, borderwidth=5)
    busModelEntryBox.grid(row=2, column=1)    

    # Create entry box for user to enter the bus's year
    busYearLabel = tk.Label(window9th, text='Enter the bus\'s year:')
    busYearLabel.grid(row=3, column=0)
    busYearEntryBox = tk.Entry(window9th, width=30, borderwidth=5)
    busYearEntryBox.grid(row=3, column=1)    

    # Create 'Add' button to add the driver to the database
    addButton = tk.Button(window9th, text='Add',
                          command=lambda: addBus(cursor, conn, 
                                                 busIDEntryBox, busModelEntryBox, 
                                                 busYearEntryBox))
    addButton.grid(row=4, column=0)

    # Create 'Quit' button to exit
    exitButton = tk.Button(window9th, text='Exit', fg='red', command=window9th.destroy)        
    exitButton.grid(row=4, column=2)

def addBus(cursor, conn, busIDEntryBox, busModelEntryBox, busYearEntryBox):
    ''' add a bus '''
    try:
        busID = busIDEntryBox.get()
        busModel = busModelEntryBox.get()
        busYear = busYearEntryBox.get()
        cursor.execute("INSERT INTO Bus VALUES ('" + busID + "', '" + busModel + "', '" + busYear + "')")
        conn.commit()
        messagebox.showinfo(title='Success',
                            message="Bus ID = " + busID + " was successfully added!")
    except Error:
        messagebox.showwarning(title='Error',
                               message='Error! Please check the inputted data.')
    finally:        
        # Clear the textbox
        busIDEntryBox.delete(0, tk.END)
        busModelEntryBox.delete(0, tk.END)
        busYearEntryBox.delete(0, tk.END)


def deleteBusGUI(cursor, conn):
    ''' GUI: delete a bus '''

    window10th = tk.Tk()

    # Introduction
    window10th.title('Delete a bus')
    label = tk.Label(window10th, font = ('Helvetica', 11, 'bold'),
                     text='Delete a bus')
    label.grid(row=0, column=0, columnspan=5)

    # Create entry box for user to enter the bus ID
    busIDLabel = tk.Label(window10th, text='Enter the bus\'s ID:')
    busIDLabel.grid(row=1, column=0)
    busIDEntryBox = tk.Entry(window10th, width=30, borderwidth=5)
    busIDEntryBox.grid(row=1, column=1)

    # Create 'Delete' button to delete driver from the database
    deleteButton = tk.Button(window10th, text='Delete',
                            command=lambda: deleteBus(cursor, conn, busIDEntryBox))
    deleteButton.grid(row=2, column=0)

    # Create 'Quit' button to exit
    exitButton = tk.Button(window10th, text='Exit', fg='red', command=window10th.destroy)        
    exitButton.grid(row=2, column=2)


def deleteBus(cursor, conn, busIDEntryBox):
    ''' delete a bus '''

    try:
        busID = busIDEntryBox.get()
        cursor.execute("DELETE FROM Bus WHERE busID = '" + busID + "'")
        conn.commit()
        if cursor.rowcount:
            messagebox.showinfo(title='Success',
                                message="Bus ID = " + busID + " was successfully deleted!")
        else:
            messagebox.showwarning(title='Error',
                                   message="Error! Bus ID = " + busID + " does not exists.")
    except Error:
        messagebox.showwarning(title='Error',
                               message="Error! Bus ID = " + busID + " does not exists.")
    finally:    
        # Clear the textbox    
        busIDEntryBox.delete(0, tk.END)


def authenticate(cursor, conn):
    ''' record some of the usernames and passwords that can access the system '''
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (Username text, Password text)''')
    cursor.execute("INSERT INTO users VALUES ('admin1', 'password1')")
    cursor.execute("INSERT INTO users VALUES ('admin2', 'password2')")
    cursor.execute("INSERT INTO users VALUES ('admin3', 'password3')")
    cursor.execute("INSERT INTO users VALUES ('admin4', 'password4')")
    cursor.execute("INSERT INTO users VALUES ('', '')") # this one just for quick login to access the program
    conn.commit()


def main():
    '''Main function to run the app.'''
    conn = connection.MySQLConnection(user='root', password='helloworld',
                                      host='localhost', database='transitsystem', port=3306)
    cursor = conn.cursor(buffered=True)
    authenticate(cursor, conn)    

    # Open the authentication window first and login successfully if username/passoword is correct
    root = tk.Tk()
    app = Authentication_GUI(root, conn, cursor)
    root.mainloop()


# Run the main 
if __name__ == "__main__":
    main()
