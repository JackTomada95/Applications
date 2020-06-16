import PySimpleGUI as sg
import psycopg2
import datetime
# import the forms to insert the data
from customerform import *
from vehicleform import *
from garageform import * 
# import the anaystics applications
# COUNT
from CountCustomerLocation import *
from CountGarageLocation import *
from CountGarageType import *
from CountVehicleModelBrand import *
# SUM
from SumCustomerLocation import *
from SumGarageLocation import *
from SumGarageType import *
from SumVehicleModelBrand import *
# AVERAGE
from AverageCustomerLocation import *
from AverageGarageLocation import *
from AverageGarageType import *
from AverageVehicleModelBrand import *

# theme
sg.theme("TealMono")

class repairForm():

    def __init__(self):
        # data we need for the table idr, idg, idv, idc, repaird, revenue
        global data
        global dSelected # the date
        data = []
        colHeadings = ["Repair ID", "Vehicle ID", "C. Name", "C. Surname", "Garage ID", "G. City", "G. Type", "Repair Date", "Revenue"]
        d0 = ["","","","","","","","",""]
        data.append(d0)
    
        self.menu_repair =  [
                                ["Insert", ["Garage", "Vehicle", "Customer"]],
                                ["Analysis", ["SUM", ["SUM Customer Location", "SUM Garage Location", "SUM Garage Type", "SUM Vehicle Model and Brand"], 
                                 "COUNT", ["COUNT Customer Location", "COUNT Garage Location", "COUNT Garage Type", "COUNT Vehicle Model and Brand"],
                                 "AVERAGE", ["AVERAGE Customer Location", "AVERAGE Garage Location", "AVERAGE Garage Type", "AVERAGE Vehicle Model and Brand"]]],
                                ["Refresh Tables", ["Refresh all tables"]],
                                ["Exit", ["Exit"]]
                            ]
        
        self.frame1 =   [
                            [sg.Text("Customer: ", size=(12,1)), sg.Combo(values=[], size=(30,10), enable_events=True, tooltip="Customers", key="selCUSTOMER", readonly=True)],
                            [sg.Text("IDc: ", size=(12,1)), sg.InputText(size=(30,1), key='idc')],
                            [sg.Text("Name: ", size=(12,1)), sg.InputText(size=(30,1), key='name')],
                            [sg.Text("Surname: ", size=(12,1)), sg.InputText(size=(30,1), key='surname')],
                            [sg.Text("City: ", size=(12,1)), sg.InputText(size=(30,1), key='cityCUSTOMER')],
                            [sg.Text("Region: ", size=(12,1)), sg.InputText(size=(30,1), key='regionCUSTOMER')]
                        ]

        self.frame2 =   [
                            [sg.Text("Vehicle: ", size=(35,1)), sg.Text("Garage: ")],
                            [sg.Combo(values=[], size = (20,10), enable_events=True, tooltip="VEHICLE", key="selVEHICLE", readonly=True), sg.Text("", size=(14,1)),
                             sg.Combo(values=[], size = (26,10), enable_events=True, tooltip="GARAGE", key="selGARAGE", readonly=True)],
                            [sg.Text("IDv: ", size=(10, 1)), sg.InputText(size=(12,1), key="idv"), sg.Text("", size=(12,1)),
                             sg.Text("IDg: ", size=(10,1)), sg.InputText(size=(12,1), key="idg")],
                            [sg.Text("Model: ", size=(10, 1)), sg.InputText(size=(12,1), key="model"), sg.Text("", size=(12,1)),
                             sg.Text("City: ", size=(10,1)), sg.InputText(size=(12,1), key="cityGARAGE")],
                            [sg.Text("Brand: ", size=(10, 1)), sg.InputText(size=(12,1), key="brand"), sg.Text("", size=(12,1)),
                             sg.Text("Region: ", size=(10,1)), sg.InputText(size=(12,1), key="regionGARAGE")],
                            [sg.Text("Choose the date: ")],
                            [sg.CalendarButton("Choose Date", target="input", key="date", format=None),
                             sg.Button("OK", key="OK")], [sg.Input("", size=(20,1), key="input"), sg.Text("", size=(17,1)),
                             sg.Text("Revenue: ", size=(10,1)), sg.InputText(size=(12,1), key="revenue")]
                        ]
        
        self.frame_table =  [
                                [sg.Text("")],
                                [sg.Table(values=data[0:][:], headings=colHeadings, key="TABLE", num_rows=10, enable_events=True, justification="center", 
                                 auto_size_columns=True)],
                                [sg.Text("")],
                                [sg.Text("", size=(25, 1)), sg.Button("ADD", key="ADD", size=(8,1)),
                                 sg.Button("UPDATE", key="UPDATE", size=(8,1)),
                                 sg.Button("DELETE", key="DELETE", size=(8,1))]
                            ]

        self.layout =   [
                            [sg.Menu(self.menu_repair)],
                            [sg.Frame("Customer", self.frame1), sg.Frame("Vehicle, Garage and Facts", self.frame2)],
                            [sg.Text("", size = (8,1)), sg.Frame("Repair Form", self.frame_table, size=(10,1))]
                        ]
        
        self.window = sg.Window("Repair Form").Layout(self.layout).Finalize()

        self.populateGarage()
        self.populateCustomer()
        self.populateVehicle()

        while True:
            event, values = self.window.Read()

            if event == "Garage":
                GarageForm()
            elif event == "Customer":
                CustomerForm()
            elif event == "Vehicle":
                VehicleForm()
            elif event == "Refresh all tables":
                self.populateGarage()
                self.populateCustomer()
                self.populateVehicle()
            elif event == "selCUSTOMER":
                self.selectCustomer(values)
            elif event == "selGARAGE":
                self.selectGarage(values)
            elif event == "selVEHICLE":
                self.selectVehicle(values)
            elif event == "OK":
                dSelected = values["input"][0:10]
            elif event == "ADD":
                self.addRepairFact(values)
            elif event == "TABLE":
                self.rowSelected(values)
            elif event == "UPDATE":
                self.updateRepairFact(values)
            elif event == "DELETE":
                self.deleteRepairFact(values)
            elif event == "SUM Customer Location":
                SumCustomerLocation()
            elif event == "SUM Garage Location":
                SumGarageLocation()
            elif event == "SUM Garage Type":
                SumGarageType()
            elif event == "SUM Vehicle Model and Brand":
                SumVehicleModelBrand()
            elif event == "COUNT Customer Location":
                CountCustomerLocation()
            elif event == "COUNT Garage Location":
                CountGarageLocation()
            elif event == "COUNT Garage Type":
                CountGarageType()
            elif event == "COUNT Vehicle Model and Brand":
                CountVehicleModelBrand()
            elif event == "AVERAGE Customer Location":
                AverageCustomerLocation()
            elif event == "AVERAGE Garage Location":
                AverageGarageLocation()
            elif event == "AVERAGE Garage Type":
                AverageGarageType()
            elif event == "AVERAGE Vehicle Model and Brand":
                AverageVehicleModelBrand()
            elif event in ("Exit", None):
                break
        
        self.window.Close()

# --------------------------------------------------------------------------------------
   
    def populateCustomer(self):
        dataC = []
        conn = None

        try:
            
            conn = psycopg2.connect(host="localhost",database="GarageDB",user="postgres", password="375Pass",port='5432')

            cur = conn.cursor()

            selectCustomer = "SELECT * FROM \"Garages\".\"Customer\" ORDER BY idc"
            cur.execute(selectCustomer)
            self.rowsC = cur.fetchall()

            dataC.clear()
            for row in self.rowsC:
                dataC.append(row[0:3])

            self.window.FindElement("selCUSTOMER").Update(values=dataC)

        except (Exception, psycopg2.DatabaseError) as error:
            sg.Popup("Populate Customer", str(error))

        finally:
            if conn is not None:
                cur.close()
                conn.close()

# --------------------------------------------------------------------------------------
    
    def populateVehicle(self):
        dataV = []
        conn = None

        try:
            
            conn = psycopg2.connect(host="localhost",database="GarageDB",user="postgres", password="375Pass",port='5432')

            cur = conn.cursor()

            selectVehicle = "SELECT * FROM \"Garages\".\"Vehicle\" ORDER BY idv"
            cur.execute(selectVehicle)
            self.rowsV = cur.fetchall()

            dataV.clear()
            for row in self.rowsV:
                dataV.append(row[0:3])

            self.window.FindElement("selVEHICLE").Update(values=dataV)

        except (Exception, psycopg2.DatabaseError) as error:
            sg.Popup("Populate Vehicle", str(error))

        finally:
            if conn is not None:
                cur.close()
                conn.close()
# --------------------------------------------------------------------------------------
    
    def populateGarage(self):
        dataG = []
        conn = None

        try:
            
            conn = psycopg2.connect(host="localhost",database="GarageDB",user="postgres", password="375Pass",port='5432')

            cur = conn.cursor()

            selectGarage = "SELECT * FROM \"Garages\".\"Garage\" ORDER BY idg"
            cur.execute(selectGarage)
            self.rowsG = cur.fetchall()

            dataG.clear()
            for row in self.rowsG:
                dataG.append(row[0:3])

            self.window.FindElement("selGARAGE").Update(values=dataG)

        except (Exception, psycopg2.DatabaseError) as error:
            sg.Popup("Populate Garage", str(error))

        finally:
            if conn is not None:
                cur.close()
                conn.close()

# ---------------------------------------------------------------------------------------

    def selectCustomer(self, values):
        global idcSelected
        idcSelected = values["selCUSTOMER"][0]

        for row in self.rowsC:
            if idcSelected == row[0]:
                self.window.FindElement("idc").Update(int(row[0]))
                self.window.FindElement("name").Update(str(row[1]))
                self.window.FindElement("surname").Update(str(row[2]))
                self.window.FindElement("cityCUSTOMER").Update(str(row[5]))
                self.window.FindElement("regionCUSTOMER").Update(str(row[6]))

        # self.tablePopulate
# ---------------------------------------------------------------------------------------

    def selectVehicle(self, values):
        global idvSelected
        idvSelected = values["selVEHICLE"][0]

        for row in self.rowsV:
            if idvSelected == row[0]:
                self.window.FindElement("idv").Update(int(row[0]))
                self.window.FindElement("model").Update(str(row[1]))
                self.window.FindElement("brand").Update(str(row[2]))

        self.tablePopulate() # the table gets populated once you select a vehicle

# ---------------------------------------------------------------------------------------

    def selectGarage(self, values):
        global idgSelected
        idgSelected = values["selGARAGE"][0]

        for row in self.rowsG:
            if idgSelected == row[0]:
                self.window.FindElement("idg").Update(int(row[0]))
                self.window.FindElement("cityGARAGE").Update(str(row[2]))
                self.window.FindElement("regionGARAGE").Update(str(row[3]))

# ---------------------------------------------------------------------------------------  add repair fact

    def addRepairFact(self, values):
        conn = None

        try:

            conn = psycopg2.connect(host="localhost",database="GarageDB",user="postgres", password="375Pass",port='5432')

            cur = conn.cursor()
            

            idg = idgSelected
            idv = idvSelected
            idc = idcSelected
            repaird = dSelected # defined in the while loop
            revenue = int(values["revenue"])

            factInsert = "INSERT INTO \"Garages\".\"RepairFacts\" (idg, idv, idc, repaird, revenue) VALUES (%s, %s, %s, %s, %s)"
            factRec = (idg, idv, idc, repaird, revenue)
            cur.execute(factInsert, factRec)
            conn.commit()
            
            sg.Popup("Data has been inserted correctly")
            self.tablePopulate()

        except (Exception, psycopg2.DatabaseError) as error:
            sg.Popup("Add RepairFact", str(error))

        finally:
            if conn is not None:
                cur.close()
                conn.close() 


# ---------------------------------------------------------------------------------------  populate the table

    def tablePopulate(self):
        data.clear()
        self.window.Element("TABLE").Update(values=data)

        try:

            conn = psycopg2.connect(host="localhost",database="GarageDB",user="postgres", password="375Pass",port='5432')

            cur = conn.cursor()

            selectFactTableRows = "SELECT * FROM \"Garages\".\"RepairFacts\" WHERE idv = %s ORDER BY idr"
            cur.execute(selectFactTableRows, (idvSelected, ))
            self.rRows = cur.fetchall() 

            for row in self.rRows: # now you need to extract rows from the customer and garage table (you can get vehicle's ID directly from the fact table)

                # get customer's name and surname from customer's table            

                selectCustomer = "SELECT * FROM \"Garages\".\"Customer\" WHERE idc = %s"
                cur.execute(selectCustomer, (row[3],))
                rowCustomer = cur.fetchone()

                # get Garage's location and type

                selectGarage = "SELECT * FROM \"Garages\".\"Garage\" WHERE idg = %s"
                cur.execute(selectGarage, (row[1],))
                rowGarage = cur.fetchone()

                # append the needed data and populate the table
                d = [row[0], row[2], rowCustomer[1], rowCustomer[2], rowGarage[0], rowGarage[2], rowGarage[1], row[4], row[5]] 
                data.append(d)
                self.window.Element("TABLE").update(values=data) 

        
        except (Exception, psycopg2.DatabaseError) as error:
            sg.Popup("Populate Table", str(error))

        finally:
            if conn is not None:
                cur.close()
                conn.close()   

# -------------------------------------------------------------------------------

    def rowSelected(self, values):
        global rowInd
        global rowValues

        rowInd = values["TABLE"][0]
        rowValues = data[rowInd]

        sg.Popup(rowValues)


# ------------------------------------------------------------------

    def updateRepairFact(self, values):
        rowValues[7] = dSelected
        rowValues[8] = int(values["revenue"])

        conn = None

        try:
            conn = psycopg2.connect(host="localhost",database="GarageDB",user="postgres", password="375Pass",port='5432')
            cur = conn.cursor()

            # now you must update the repair form, but only date and revenue

            RepairFactUpdate = "UPDATE \"Garages\".\"RepairFacts\" SET repaird = %s, revenue = %s  WHERE idr = %s"
            cur.execute(RepairFactUpdate, (rowValues[7], rowValues[8], rowValues[0]))
            conn.commit()

            data[rowInd] = rowValues
            self.window.Element("TABLE").Update(values=data)

        except (Exception, psycopg2.DatabaseError) as error:
            sg.Popup("Update Enrollment", str(error))

        finally:
            if conn is not None:
                cur.close()
                conn.close() 

# ----------------------------------------------------------------------

    def deleteRepairFact(self, values):
        conn = None

        try:
            conn = psycopg2.connect(host="localhost",database="GarageDB",user="postgres", password="375Pass",port='5432')
            cur = conn.cursor()

            RepairFactDelete = "DELETE FROM \"Garages\".\"RepairFacts\" WHERE idr = %s"
            cur.execute(RepairFactDelete, (rowValues[0],))
            conn.commit()

            del data[rowInd]
            self.window.Element("TABLE").Update(values = data)

        except (Exception, psycopg2.DatabaseError) as error:
            sg.Popup("Delete Enrollment", str(error))

        finally:
            if conn is not None:
                cur.close()
                conn.close() 


if __name__ == "__main__":
    repairForm()
