import  mysql.connector 
import openpyxl


db = mysql.connector.connect(host="localhost",user="root",passwd="",database="Stock1")
mc = db.cursor()


path = "Data.xlsx"
wb_obj = openpyxl.load_workbook(path)
sheet_obj = wb_obj.active

#defining Some useful variables and lists
X = []
Y = []
n = 365
for i in range(1,n+1):
    X.append(i)

for i in range(1,n+1):
    cell_obj = sheet_obj.cell(row = i, column = 2)
    Y.append(cell_obj.value)

mc.execute("CREATE TABLE price(Dnum int,val numeric(7,2))")

for i in range(0,n):
	d = X[i]
	o = Y[i]
	mc.execute("INSERT INTO price(Dnum,val) VALUES({},{})".format(d,o))

db.commit()

