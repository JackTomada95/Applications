import PySimpleGUI as sg
import psycopg2

class CustomerForm():

    def __init__(self):

        self.frame_layout = [
                                [sg.Text("Select customer: ", justification = "left", size = (20,1)),
                                 sg.Combo([], size=(30,1), enable_events=True, key='selCustomer', readonly=True)],
                                [sg.Text("Name: ", size = (20,1)), sg.InputText(size = (30, 1), key = "name")],
                                [sg.Text("Surname: ", size = (20,1)), sg.InputText(size = (30, 1), key = "surname")],
                                [sg.Text("Birth Date: ", size = (20,1)), sg.InputText(size = (30, 1), key = "birth_date", tooltip="yyyy-mm-dd")],
                                [sg.Text("Gender: ", size = (20,1)),
                                 sg.Radio("Female", "R", size = (10, 1), key = "female"),
                                 sg.Radio("Male", "R", size = (10, 1), key = "male")],
                                [sg.Text("City: ", size = (20,1)), sg.InputText(size = (30, 1), key = "city")],
                                [sg.Text("Region: ", size = (20,1)),
                                 sg.Combo(["Veneto", "Trentino-Sud Tirol", "Friuli-Venezia Giulia", "Other"], size = (30,1), readonly=True, key = "region")]
                            ]
        
        self.layout =   [
                            [sg.Frame('', self.frame_layout, title_color='blue')],
                            [sg.Text('')],
                            [sg.Text(''), sg.Button('Add', size=(8,1), key='add'),
                            sg.Button('Update', size=(8,1), key='update'),
                            sg.Button('Delete', size=(8,1), key='delete'),
                            sg.Button('Close', size=(8,1), key='close'),
                            sg.Button('Populate', size=(8,1), key='populate')],
                            [sg.Text('')]
                        ]

        self.window = sg.Window('Customer Form').Layout(self.layout).Finalize()

        while True:
            event, values = self.window.Read()

            if event == 'add':
                self.addCustomer(values)
            elif event == 'selCustomer':
                self.selectCustomer(values)
            elif event == 'populate':
                self.populateCustomer()
            elif event == 'update':
                self.updateCustomer(values)
            elif event == "delete":
                self.deleteCustomer()
            elif event in (None, "close"):
                break
        
        self.window.Close()


# ---------------------------------------------------------------------------------------------------
    def addCustomer(self, values):
        conn = None

        try:
            
            conn = psycopg2.connect(host="localhost",database="GarageDB",user="postgres", password="375Pass",port='5432')

            
            cur = conn.cursor()

            
            cname = str(values['name'])
            surname = str(values['surname'])
            birth_date = str(values['birth_date'])
            city = str(values['city'].title())
            region = str(values['region'])
            
            if values["female"] is True:
                gender = "Female"
            else:
                gender = "Male"


            
            customerInsert = "INSERT INTO \"Garages\".\"Customer\" (cname, surname, birth_date, gender, city, region) VALUES(%s,%s,%s,%s,%s,%s)"
            customerRec = (cname, surname, birth_date, gender, city, region)
            cur.execute(customerInsert, customerRec)
            conn.commit()

            
            x = "Customer {} has been inserted".format(str(values["surname"]))
            sg.Popup(x)

            
            self.clearFields() 
            

        except (Exception, psycopg2.DatabaseError) as error:
            sg.Popup("addGarage", str(error))

        finally:
            if conn is not None:
                cur.close()
                conn.close()

#-----------------------------------------------------------------------------------

    def populateCustomer(self):

        data = []
        conn = None

        try:
            
            conn = psycopg2.connect(host="localhost",database="GarageDB",user="postgres", password="375Pass",port='5432')

            
            cur = conn.cursor()

            selectCustomer = "SELECT * FROM \"Garages\".\"Customer\" ORDER BY idc"
            cur.execute(selectCustomer)
            self.rows = cur.fetchall()

            data[:] = []
            for row in self.rows:
                data.append(row[0:3])

            self.window.FindElement("selCustomer").Update(values=data)   

            self.clearFields()        
          
        except (Exception, psycopg2.DatabaseError) as error:
            sg.Popup("Populate", str(error))

        finally:
            if conn is not None:
                cur.close()
                conn.close()
# ---------------------------------------------------------------------------------

    def selectCustomer(self, values):
        global idSelected

        idSelected = values['selCustomer'][0]

        for row in self.rows:
            if (idSelected == row[0]):
                self.window.FindElement("name").Update(str(row[1])) 
                self.window.FindElement("surname").Update(str(row[2]))
                self.window.FindElement("birth_date").Update(str(row[4]))
                if str(row[3]) == "Female":
                    self.window.FindElement("female").Update(value="True")
                elif str(row[3]) == "Male":
                    self.window.FindElement("male").Update(value="True")
                self.window.FindElement("city").Update(str(row[5]))
                self.window.FindElement("region").Update(str(row[6]))
                break

# -----------------------------------------------------------------------------------

    def updateCustomer(self, values):
        conn = None

        try:
            
            conn = psycopg2.connect(host="localhost",database="GarageDB",user="postgres", password="375Pass",port='5432')

            
            cur = conn.cursor()

            selectCustomer = "SELECT * FROM \"Garages\".\"Customer\" WHERE idc = %s"
            cur.execute(selectCustomer, (idSelected,))
            self.row = cur.fetchone() 

            cname = str(values['name'])
            surname = str(values['surname'])
            city = str(values["city"]).title()
            birth_date = str(values["birth_date"])
            region = str(values['region'])
            
            if values["female"]:
                gender = "Female"
            else:
                gender = "Male"
            
            customerUpdate = "UPDATE \"Garages\".\"Customer\" SET cname = %s, surname = %s, gender = %s, birth_date = %s, city = %s, region = %s WHERE idc = %s"
            cur.execute(customerUpdate, (cname, surname, gender, birth_date, city, region, idSelected)) 
            conn.commit()

            x = "The customer {} has been updated".format(str(values["surname"]))
            sg.Popup(x)
            self.clearFields()

        except (Exception, psycopg2.DatabaseError) as error:
            sg.Popup("Update", str(error))

        finally:
            if conn is not None:
                cur.close()
                conn.close()


# ---------------------------------------------------------------------------------

    def deleteCustomer(self):
        try:
        
            conn = psycopg2.connect(host="localhost",database="GarageDB",user="postgres", password="375Pass",port='5432')

            
            cur = conn.cursor()

            customerDelete = "DELETE FROM \"Garages\".\"Customer\" WHERE idc = %s"
            cur.execute(customerDelete, (idSelected,))
            conn.commit()

            sg.Popup("Record has been deleted")
            self.clearFields()

        except (Exception, psycopg2.DatabaseError) as error:
            sg.Popup("Delete", str(error))

        finally:
            if conn is not None:
                cur.close()
                conn.close()

# ---------------------------------------------------------------------------------------------------
    def clearFields(self):
        self.window.FindElement("name").Update("")
        self.window.FindElement("surname").Update("")
        self.window.FindElement("city").Update("")
        self.window.FindElement("region").Update("")
        self.window.FindElement("birth_date").Update("")
        self.window.FindElement("female").Update(value='True')

# ----------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    CustomerForm()