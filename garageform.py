import PySimpleGUI as sg
import psycopg2

class GarageForm():
    
    def __init__(self):

        
        self.frame_layout =     [
                                    [sg.Text("Select Garages: ", justification="left", size=(20,1)),
                                     sg.Combo([], size=(30,1), enable_events=True, key='selGarages', readonly=True)],
                                    [sg.Text("Type: ", size = (20,1)), sg.Combo(["big", "small"], size = (30,1), readonly=True, key = "type")],
                                    [sg.Text("City: ", size = (20,1)),
                                     sg.Combo(["Venezia", "Treviso", "Padova","Trento", "Bolzano", "Udine", "Trieste", "Gorizia"], size = (30,1), key = "city", readonly=True)],
                                    [sg.Text("Region: ", size = (20,1)),
                                     sg.Combo(["Veneto", "Trentino-Sud Tirol", "Friuli-Venezia Giulia"], size = (30,1), readonly=True, key = "region")]
                                ]

        self.layout =           [
                                    [sg.Frame("", self.frame_layout, title_color="blue")],
                                    [sg.Text('', size=(1,1)), sg.Button('Add', size=(8,1), key='add'),
                                     sg.Button('Update', size=(8,1), key='update'),
                                     sg.Button('Delete', size=(8,1), key='delete'),
                                     sg.Button('Close', size=(8,1), key='close'),
                                     sg.Button('Populate', size=(8,1), key='populate')],
                                    [sg.Text('')]
                                ]

        self.window = sg.Window('Garage Form').Layout(self.layout).Finalize()

        while True:
            event, values = self.window.Read()

            if event == 'add':
                self.addGarage(values)
            elif event == 'selGarages':
                self.selectGarage(values)
            elif event == 'populate':
                self.populateGarage()
            elif event == 'update':
                self.updateGarage(values)
            elif event == "delete":
                self.deleteGarage()
            elif event in (None, "close"):
                break
        
        self.window.Close()
          
# ------------------------------------------------------------------------------------------------
    def addGarage(self, values):
        conn = None

        try:
            
            conn = psycopg2.connect(host="localhost",database="GarageDB",user="postgres", password="375Pass",port='5432')

            
            cur = conn.cursor()

            
            gtype = str(values['type'])
            city = str(values['city'])
            region = str(values['region'])

            
            garageInsert = "INSERT INTO \"Garages\".\"Garage\" (gtype, city, region) VALUES(%s,%s,%s)"
            garageRec = (gtype, city, region)
            cur.execute(garageInsert, garageRec)
            conn.commit()

            
            x = "A new garage has been inserted"
            sg.Popup(x)

            
            self.clearFields() 
            

        except (Exception, psycopg2.DatabaseError) as error:
            sg.Popup("addGarage", str(error))

        finally:
            if conn is not None:
                cur.close()
                conn.close()

# ---------------------------------------------------------------------------------

    def populateGarage(self):

        data = []
        conn = None

        try:
            
            conn = psycopg2.connect(host="localhost",database="GarageDB",user="postgres", password="375Pass",port='5432')

            
            cur = conn.cursor()

            selectGarage = "SELECT * FROM \"Garages\".\"Garage\" ORDER BY idg"
            cur.execute(selectGarage)
            self.rows = cur.fetchall()

            data[:] = []
            for row in self.rows:
                data.append(row[0:4])

            self.window.FindElement("selGarages").Update(values=data)   

            self.clearFields()        
          
        except (Exception, psycopg2.DatabaseError) as error:
            sg.Popup("Populate", str(error))

        finally:
            if conn is not None:
                cur.close()
                conn.close()
# ---------------------------------------------------------------------------------

    def selectGarage(self, values):
        global idSelected

        idSelected = values['selGarages'][0]

        for row in self.rows:
            if (idSelected == row[0]):
                self.window.FindElement("type").Update(str(row[1]))
                self.window.FindElement("city").Update(str(row[2]))
                self.window.FindElement("region").Update(str(row[3]))
                break

# -----------------------------------------------------------------------------------

    def updateGarage(self, values):
        conn = None

        try:
            
            conn = psycopg2.connect(host="localhost",database="GarageDB",user="postgres", password="375Pass",port='5432')

           
            cur = conn.cursor()

            selectGarage = "SELECT * FROM \"Garages\".\"Garage\" WHERE idg = %s"
            cur.execute(selectGarage, (idSelected,)) 
            self.row = cur.fetchone() 

            gtype = str(values['type'])
            city = str(values['city'])
            region = str(values['region'])
            
            garageUpdate = "UPDATE \"Garages\".\"Garage\" SET gtype = %s, city = %s, region = %s WHERE idg = %s"
            cur.execute(garageUpdate, (gtype, city, region, idSelected)) 
            conn.commit()

            x = "This garage has been updated"
            sg.Popup(x)
            self.clearFields()

        except (Exception, psycopg2.DatabaseError) as error:
            sg.Popup("Update", str(error))

        finally:
            if conn is not None:
                cur.close()
                conn.close()


# ---------------------------------------------------------------------------------

    def deleteGarage(self):
        try:
        
            conn = psycopg2.connect(host="localhost",database="GarageDB",user="postgres", password="375Pass",port='5432')

            
            cur = conn.cursor()

            garageDelete = "DELETE FROM \"Garages\".\"Garage\" WHERE idg = %s"
            cur.execute(garageDelete, (idSelected,))
            conn.commit()

            sg.Popup("Record has been deleted")
            self.clearFields()

        except (Exception, psycopg2.DatabaseError) as error:
            sg.Popup("Delete", str(error))

        finally:
            if conn is not None:
                cur.close()
                conn.close()


# --------------------------------------------------------------------------------
    def clearFields(self):
        self.window.FindElement("type").Update("")
        self.window.FindElement("city").Update("")
        self.window.FindElement("region").Update("")

if __name__ == '__main__':
    GarageForm()
            
