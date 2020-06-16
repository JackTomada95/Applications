import PySimpleGUI as sg
import psycopg2
import datetime


class SumCustomerLocation():

    def __init__(self):
        
        global data
        data = []
        colHeadings = ["Customer ID", "City", "Region", "Sum"]
        d0 = ["","","", ""]
        data.append(d0)
    
        
        self.frame_table =  [
                                [sg.Text('Click on "GO" to run the analysis: '), sg.Text(size=(20,1)), sg.Button("GO", size=(8,1), key="GO")],
                                [sg.Text("")],
                                [sg.Text(size=(4,1)), sg.Table(values=data[0:][:], headings=colHeadings, key="TABLE", num_rows=15, enable_events=True, justification="center",# what is data[0:][:]???
                                 auto_size_columns=False)],
                                [sg.Text("")]
                            ]

        self.layout =   [
                            [sg.Frame("Customer, Location dimension", self.frame_table, size=(10,1))],
                            [sg.Text("", size=(48,1)), sg.Button("CLOSE", size=(8,1), key="CLOSE")]
                        ]
        
        self.window = sg.Window("GROUP BY ROLLUP: Customer dimension, Location hierarchy").Layout(self.layout).Finalize()

        while True:
            event, values = self.window.Read()

            if event == "GO":
                self.tablePopulate()
            elif event in ("CLOSE", None):
                break
        
        self.window.Close()

    
    def tablePopulate(self):
        data.clear()
        self.window.Element("TABLE").Update(values=data)

        try:

            conn = psycopg2.connect(host="localhost",database="GarageDB",user="postgres", password="375Pass",port='5432')

            cur = conn.cursor()

            selectFactTableRows = "SELECT cu.idc, cu.city, cu.region, SUM(rp.revenue) FROM \"Garages\".\"Customer\" cu JOIN \"Garages\".\"RepairFacts\" rp ON cu.idc = rp.idc GROUP BY ROLLUP (cu.region,cu.city,cu.idc);"
            cur.execute(selectFactTableRows)
            self.rollupRows = cur.fetchall() 

            for row in self.rollupRows:            

                d = [row[0], row[1], row[2], row[3]] 
                data.append(d)
                self.window.Element("TABLE").update(values=data) 

        
        except (Exception, psycopg2.DatabaseError) as error:
            sg.Popup("ROLLUP CUSTOMER BY LOCATION (SUM)", str(error))

        finally:
            if conn is not None:
                cur.close()
                conn.close()   

if __name__ == "__main__":
    SumCustomerLocation()