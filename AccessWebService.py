import pandas as pd
import numpy as np
import requests
import json
import time
import sys

minP=1000
maxP=1030
pStep=(maxP-minP)//8

f = open('AccessWebService.log','w')
f.write('AccessWebService: start \n')

#Get previous values
try:
    df = pd.read_csv('tabPressures.csv')
except:
    data=np.array([np.arange(6)])
    index=[1]
    columns=['p1','p2','p3','p4','p5','p6']
    df = pd.DataFrame(data, index=index, columns=columns)

while True:
    # Get the pressure
    print('Get pressure at: %s' % time.ctime())
    f.write('Get pressure at: %s \n' % time.ctime())
    rGet = requests.get("https://api.openweathermap.org/data/2.5/weather?q=GENEVA,CH&appid=4e14201488215f9b772d5afd12144094")
    
    # Convert it to a Python dictionary
    data = json.loads(rGet.text)
    pressure = data['main']['pressure']
    tempK = data['main']['temp']
    tempC = round(tempK - 273.15)
    print("Pressure: %s" % (pressure))
    f.write('Pressure: %s \n' % (pressure))
    print('Temperature: %s' % tempC)
    f.write('Temperature: %s \n' % tempC)
    
    p0=df.iloc[0]['p1']
    p1=df.iloc[0]['p2']
    p2=df.iloc[0]['p3']
    p3=df.iloc[0]['p4']
    p4=df.iloc[0]['p5']
    p5=df.iloc[0]['p6']
    p6=pressure
    print('Pressure values: %s' % str(p1)+','+str(p2)+','+str(p3)+','+str(p4)+','+str(p5)+','+str(p6))
    
    #Steps pressure values
    if p0<minP:p0=minP
    p0=(p0-minP)//pStep
    if p0<=0:p0=1

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
    
    # add pressure
    #pressures=str(df.iloc[0]['p1'])+','+str(df.iloc[0]['p2'])+','+str(df.iloc[0]['p3'])+','+str(df.iloc[0]['p4'])+','+str(df.iloc[0]['p5'])+','+str(pressure)
    #pressures=str(p1)+','+str(p2)+','+str(p3)+','+str(p4)+','+str(p5)+','+str(pressure)
#    pressures=str(p0)+','+str(p1)+','+str(p2)+','+str(p3)+','+str(p4)+','+str(p5)+','+str(p6)
    pressures='8,'+str(p1)+','+str(p2)+','+str(p3)+','+str(p4)+','+str(p5)+','+str(p6)
    print('Graph values: %s' % pressures)
    f.write('Graph values: %s \n' % pressures)

    iDisplay = 'i37998'
    iUp = 'i37999'
    iDown = 'i38001'
    if p6>p5:
        iDisplay=iUp 
    if p6<p5:
        iDisplay=iDown
     
    headers = {
        'Accept':'application/json',
        'X-Access-Token':'ZjEwMjBmZGNkMmQ1NWE1ZmNlYzY2ZDNhYmQ1NDc4MmZlZWNiZGUzYTA1OWVjMTY1OTFiZjg4YzZjNjZlMzZmOA==',
        'Cache-Control':'no-cache'}
    
    data_start = '{"frames": [{"index":0,"text":"Temperature '+str(tempC)+' and Pressure in Geneva","icon":"i37998"},'
    frame1 = '{"index":1,"chartData":['+pressures+']},'
    frame2 = '{"index":2,"text":"'+str(pressure)+'","icon":"'+iDisplay+'"}'
    data_end = ']}'
    data=data_start+frame1+frame2+data_end
    
    url = "https://developer.lametric.com/api/v1/dev/widget/update/com.lametric.76f9324890f56b4093ec9da83e069967/3"
    
    print('Post pressure at: %s' % time.ctime())
    f.write('Post pressure at: %s \n\n' % time.ctime())
    rPost = requests.post(url, headers=headers, data=data)    
    result=rPost.content
    print(result)
    
    #for index, row in df.iterrows():
    #    if index>0:pressures=pressures+str(row['val'])+','
        
    # save pressure
    df.iloc[0]['p1']=df.iloc[0]['p2']
    df.iloc[0]['p2']=df.iloc[0]['p3']
    df.iloc[0]['p3']=df.iloc[0]['p4']
    df.iloc[0]['p4']=df.iloc[0]['p5']
    df.iloc[0]['p5']=df.iloc[0]['p6']
    df.iloc[0]['p6']=pressure
    df.to_csv('tabPressures.csv', index=False)
    
    f.flush()
    time.sleep(60*60*1)
