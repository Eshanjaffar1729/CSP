from matplotlib import pyplot as plt
import  mysql.connector 
import math
import LoadingData

def average(x):
    ans = 0
    for elems in x:
        ans += elems
    return ans/len(x)

db = mysql.connector.connect(host="localhost",user="root",passwd="",database="stock1")
mc = db.cursor()




#defining Some useful variables and lists
X = []
Y = []
l = [] 
MA =[]
n = 365
for i in range(1,n+1):
    X.append(i)

mc.execute("select val from price")
val = mc.fetchall()

for i in range(0,n):
    Y.append(int(val[i][0]))



for i in range(0,n):
    ra = []
    if i<5:
        MA.append(Y[i])
    else:
        for j in range(i-4,i+1):
            ra.append(Y[j])
        MA.append(average(ra))
    ra=[]


mc.execute("alter table price add column pred NUMERIC(7,2)")
for i in range(1,n+1):
    prediction = MA[i-1]
    mc.execute("update price set pred={} where Dnum={}".format(prediction,i))
db.commit()

def plot_data():
    fig, ax = plt.subplots()
    ax.plot(X,Y)
    ax.plot(X,MA,color="green")
    fig.show()

def pred(dnum):
    mc.execute("select * from price where dnum={}".format(dnum))
    dataOut = mc.fetchall()
    for elems in dataOut:
        print(elems)

def remove(dnum):
    mc.execute("delete from price where dnum={}".format(dnum))
    db.commit()



msg = '''
Enter 1 to predict the share price of a given day
Enter 2 to remove the data of given day
Enter 3 to plot the share price and exit
'''

cont = True

while cont:
    print(msg)
    ans = int(input())
    if ans==1:
        date_number = int(input("Enter the Day number to predict share price: "))
        pred(date_number)
    elif ans==2:
        date_number = int(input("Enter the Day number to delete the data coresponding: "))
        remove(date_number)
        print("Data conressponding to {} removed sucessfully".format(date_number))
    elif ans==3:
        plot_data()
        cont = False
    else:
        print("Invalid Input!")

    print("")
    

