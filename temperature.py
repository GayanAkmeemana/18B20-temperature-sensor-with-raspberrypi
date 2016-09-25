import time
import MySQLdb
import os

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

db = MySQLdb.connect("localhost","root","gayan123","temperature")
cur = db.cursor()

temp_sensor = '/sys/bus/w1/devices/28-000005665ef9/w1_slave'

def read_temperature(sensor):
        tempfile = open(sensor)
        thetext = tempfile.read()
        tempfile.close()
        tempdata = thetext.split("\n")[1].split(" ")[9]
        temperature = float(tempdata[2:])
        temperature = temperature / 1000
        return temperature

while 1:
        temperature = read_temperature(temp_sensor)
        localtime = time.asctime( time.localtime(time.time()))
        insertquery = """INSERT INTO tempData(temp,date) VALUES(%s,%s)""",(temperature,localtime)
        cur.execute(*insertquery)
        db.commit()
        print temperature
        print "Data Added"
        time.sleep(4)
