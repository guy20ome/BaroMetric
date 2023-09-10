import pandas as pd
import numpy as np
import requests
import json
import time
import sys

f = open('PressureWebService.log','w')
f.write('PressureWebService: start \n')
f.flush()

minP=1000
maxP=1030
pStep=(maxP-minP)//8

def laMetricUpdate(theCaller, theCity, theCountry):

    try:
        print('--')
        if theCaller is None : theCaller=''
        if theCity is None or theCountry is None:
            theCity='NOUMEA'
            theCountry='NC'
        print('GET pressure start at: %s' % time.ctime())
        print('The city : '+theCity)
        print('The country : '+theCountry)

        f.write('GET pressure start at: %s \n' % time.ctime())
        f.write('The city : '+theCity+'\n')
        f.write('The country : '+theCountry+'\n')

        
        #Get previous values
        try:
            df = pd.read_csv('tabPressures'+theCaller+'.csv')
        except:
            data=np.array([np.arange(6)])
            index=[1]
            columns=['p1','p2','p3','p4','p5','p6']
            df = pd.DataFrame(data, index=index, columns=columns)

        # Get the pressure
        rGet = requests.get("https://api.openweathermap.org/data/2.5/weather?q="+theCity+','+theCountry+"&appid=4e14201488215f9b772d5afd12144094")

        # Convert it to a Python dictionary
        data = json.loads(rGet.text)
        pressure = data['main']['pressure']
        tempK = data['main']['temp']
        tempC = round(tempK - 273.15)
        
        print("Pressure: %s" % (pressure))
        print("Temperature: %s" % (tempC))
        #print("1")
        f.write("Pressure: %s \n" % (pressure))
        #print("1")
        f.write("Temperature: %s \n" % (tempC))
        #print("1")
        
        #Saved pressure values
        p0=df.iloc[0]['p1']
        p1=df.iloc[0]['p2']
        p2=df.iloc[0]['p3']
        p3=df.iloc[0]['p4']
        p4=df.iloc[0]['p5']
        p5=df.iloc[0]['p6']
        p6=pressure
        #print("1")
        print('Saved Pressure values in '+theCity+': %s' % str(p1)+','+str(p2)+','+str(p3)+','+str(p4)+','+str(p5)+','+str(p6))
        #print("1")
        f.write('Saved Pressure values in '+theCity+': '+str(p1)+','+str(p2)+','+str(p3)+','+str(p4)+','+str(p5)+','+str(p6)+'\n')
        #print("1")

        # add icon
        iDisplay = 'i40126'
        iUp = 'i37999'
        iDown = 'i38001'
        if p6>p5:
            iDisplay=iUp 
        if p6<p5:
            iDisplay=iDown
        #print("1")

        #Steps pressure values
        if p0<minP:p0=minP
        p0=(p0-minP)//pStep
        if p0<=0:p0=1
        print('p0:%s'%p0)
            
        if p1<minP:p1=minP
        p1=(p1-minP)//pStep
        if p1<=0:p1=1
        
        if p2<minP:p2=minP
        p2=(p2-minP)//pStep
        if p2<=0:p2=1
        
        if p3<minP:p3=minP
        p3=(p3-minP)//pStep
        if p3<=0:p3=1
        
        if p4<minP:p4=minP
        p4=(p4-minP)//pStep
        if p4<=0:p4=1
        
        if p5<minP:p5=minP
        p5=(p5-minP)//pStep
        if p5<=0:p5=1
        
        if p6<minP:p6=minP
        p6=(pressure-minP)//pStep
        if p6<=0:p6=1

        pressures=str(p0)+','+str(p1)+','+str(p2)+','+str(p3)+','+str(p4)+','+str(p5)+','+str(p6)

        #print("1")
        print('Graph values: %s' % pressures)
        f.write('Graph values: %s\n' % pressures)
        #print("1")

        #set data
        myData = {"frames":
                      [
                          {"index":0,"text":"Temperature "+str(tempC)+" and Pressure in "+theCity,"icon":"i40126"},
#                          {"index":1,"chartData":[int(p0),int(p1),int(p2),int(p3),int(p4),int(p5),int(p6)]},
                          {"index":1,"chartData":[8,int(p1),int(p2),int(p3),int(p4),int(p5),int(p6)]},
                          {"index":2,"text":str(pressure),"icon":iDisplay}
                      ]
                 }

        # save pressure
        df.iloc[0]['p1']=df.iloc[0]['p2']
        df.iloc[0]['p2']=df.iloc[0]['p3']
        df.iloc[0]['p3']=df.iloc[0]['p4']
        df.iloc[0]['p4']=df.iloc[0]['p5']
        df.iloc[0]['p5']=df.iloc[0]['p6']
        df.iloc[0]['p6']=pressure
        df.to_csv('tabPressures'+theCaller+'.csv', index=False)

        #return data
        print('GET pressure end at: %s' % time.ctime())
        print('--')
        f.write('GET pressure end at: %s \n\n' % time.ctime())
        f.flush()
        return(myData)
    except:
        print('Unknown error')
        return('')

from flask import Flask, request, escape, jsonify
from flask_restful import Resource, Api
from json import dumps

app = Flask(__name__)
api = Api(app)

class Weather(Resource):
    def get(self):
        myData = laMetricUpdate(request.remote_addr, request.args.get('theCity'),request.args.get('theCountry'))
        return jsonify(myData)

api.add_resource(Weather, '/weather')

if __name__ == '__main__':
     app.run(host='192.168.1.51', port='9999')
     
