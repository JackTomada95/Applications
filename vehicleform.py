import PySimpleGUI as sg
import psycopg2

class VehicleForm():
    
    def __init__(self):

        self.frame_layout =     [
                                    [sg.Text("Select Vehicle: ", justification = "left", size = (12, 1)),
                                     sg.Combo([], size=(30,1), enable_events=True, key='selVehicles', readonly=True)],
                                    [sg.Text("Model: ", size =(12, 1)), sg.InputText(size = (30,1), key = "model")],
                                    [sg.Text("Brand", size =(12, 1)), sg.InputText(size = (30,1), key = "brand")]
                                ]
        
        self.layout =           [
                                    [sg.Frame("", self.frame_layout, title_color="blue")],
                                    [sg.Text("")],
                                    [sg.Button('Add', size=(8,1), key='add'),
                                     sg.Button('Update', size=(8,1), key='update'),
                                     sg.Button('Delete', size=(8,1), key='delete'),
                                     sg.Button('Close', size=(8,1), key='close'),
                                     sg.Button('Populate', size=(8,1), key='populate')],
                                    [sg.Text('')]                                    
                                ]
        
        self.window = sg.Window("Vehicle Form").Layout(self.layout).Finalize()

        while True:
            event, values = self.window.Read()

            if event == 'add':
                self.addVehicle(values)
            elif event == 'selVehicles':
                self.selectVehicle(values)
            elif event == 'populate':
                self.populateVehicle()
            elif event == 'update':
                self.updateVehicle(values)
            elif event == "delete":
                self.deleteVehicle()
            elif event in (None, "close"):
                break
        
        self.window.Close()

# -----------------------------------------------------------

    def addVehicle(self, values):
        conn = None

        try:
            
            conn = psycopg2.connect(host="localhost",database="GarageDB",user="postgres", password="375Pass",port='5432')

            
            cur = conn.cursor()

            
            model = str(values['model'])
            brand = str(values['brand'])

            
            vehicleInsert = "INSERT INTO \"Garages\".\"Vehicle\" (model, brand) VALUES(%s,%s)"
            vehicleRec = (model, brand)
            cur.execute(vehicleInsert, vehicleRec)
            conn.commit()

            
            x = "Vehicle {} , {} has been inserted".format(str(values["model"]), str(values["brand"]))
            sg.Popup(x)

            
            self.clearFields() 
            

        except (Exception, psycopg2.DatabaseError) as error:
            sg.Popup("addGarage", str(error))

        finally:
            if conn is not None:
                cur.close()
                conn.close()

# -----------------------------------------------------------

    def populateVehicle(self):

        data = []
        conn = None

        try:
            
            conn = psycopg2.connect(host="localhost",database="GarageDB",user="postgres", password="375Pass",port='5432')

            
            cur = conn.cursor()

            selectVehicle = "SELECT * FROM \"Garages\".\"Vehicle\" ORDER BY idv"
            cur.execute(selectVehicle)
            self.rows = cur.fetchall()

            data[:] = []
            for row in self.rows:
                data.append(row[0:3])

            self.window.FindElement("selVehicles").Update(values=data)   

            self.clearFields()        
          
        except (Exception, psycopg2.DatabaseError) as error:
            sg.Popup("Populate", str(error))

        finally:
            if conn is not None:
                cur.close()
                conn.close()
# ---------------------------------------------------------------------------------

    def selectVehicle(self, values):
        global idSelected

        idSelected = values['selVehicles'][0]

        for row in self.rows:
            if (idSelected == row[0]):
                self.window.FindElement("model").Update(str(row[1])) 
                self.window.FindElement("brand").Update(str(row[2]))
                break

# -----------------------------------------------------------------------------------

    def updateVehicle(self, values):
        conn = None

        try:
            
            conn = psycopg2.connect(host="localhost",database="GarageDB",user="postgres", password="375Pass",port='5432')

            
            cur = conn.cursor()

            selectVehicle = "SELECT * FROM \"Garages\".\"Vehicle\" WHERE idv = %s"
            cur.execute(selectVehicle, (idSelected,)) 
            self.row = cur.fetchone() 

            model = str(values['model'])
            brand = str(values['brand'])
            
            vehicleUpdate = "UPDATE \"Garages\".\"Vehicle\" SET model = %s, brand = %s WHERE idv = %s"
            cur.execute(vehicleUpdate, (model, brand, idSelected)) 
            conn.commit()

            x = "This vehicle has been updated"
            sg.Popup(x)
            self.clearFields()

        except (Exception, psycopg2.DatabaseError) as error:
            sg.Popup("Update", str(error))

        finally:
            if conn is not None:
                cur.close()
                conn.close()


# ---------------------------------------------------------------------------------

    def deleteVehicle(self):
        try:
        
            conn = psycopg2.connect(host="localhost",database="GarageDB",user="postgres", password="375Pass",port='5432')

            
            cur = conn.cursor()

            vehicleDelete = "DELETE FROM \"Garages\".\"Vehicle\" WHERE idv = %s"
            cur.execute(vehicleDelete, (idSelected,))
            conn.commit()

            sg.Popup("Record has been deleted")
            self.clearFields()

        except (Exception, psycopg2.DatabaseError) as error:
            sg.Popup("Delete", str(error))

        finally:
            if conn is not None:
                cur.close()
                conn.close()
# -----------------------------------------------------------
    def clearFields(self):
        self.window.FindElement("model").Update("")
        self.window.FindElement("brand").Update("")
# -----------------------------------------------------------
if __name__ == "__main__":
    VehicleForm()