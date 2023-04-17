#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 14:30:29 2022

@author: alecchurch
"""

# sounding.py
import urllib
import matplotlib.pyplot as plt
import numpy as np

def read_sounding_multiple(lines,S_line,E_line):
    pressure=[]
    altitude=[]
    temp    =[]
    rh      =[]
    #print(I_line)
    for line in lines[S_line+6:E_line]: # 100
        #print(line)
        entries = entries = line.split()
        if len(entries) == 11: # check that we have 11 columns
            pressure.append(float(entries[0]))
            altitude.append(float(entries[1]))
            temp.append(float(entries[2]))
            rh.append(float(entries[4]))
    return(pressure,altitude,temp,rh)

def read_sounding(url):
    pressure=[]
    altitude=[]
    temp    =[]
    tdew    =[]
    lines   = urllib.request.urlopen(url).readlines()
    for line in lines[10:76]: # 100
        entries = line.decode("utf-8").split()
        if len(entries) == 11: # check that we have 11 columns
            pressure.append(float(entries[0]))
            altitude.append(float(entries[1]))
            temp.append(float(entries[2]))
            tdew.append(float(entries[3]))
    return(pressure,altitude,temp,tdew)

def location(url):
    lines  = urllib.request.urlopen(url).readlines()
    lon=lines[81] # longitude 132
    lat=lines[80] # latitude  131
    lon=float(lon.decode("utf-8").split(":")[1])
    lat=float(lat.decode("utf-8").split(":")[1])
    return(lat,lon) 


if __name__ == '__main__':
    
    
    url1 = 'http://weather.uwyo.edu/cgi-bin/sounding?region=naconf&TYPE=TEXT%3ALIST&YEAR=2022&MONTH=10&FROM=0612&TO=0612&STNM=71924'
    url2 = 'http://weather.uwyo.edu/cgi-bin/sounding?region=naconf&TYPE=TEXT%3ALIST&YEAR=2022&MONTH=10&FROM=0612&TO=0612&STNM=72694'
    url3 = 'http://weather.uwyo.edu/cgi-bin/sounding?region=naconf&TYPE=TEXT%3ALIST&YEAR=2022&MONTH=10&FROM=0612&TO=0612&STNM=78988'

    #lat,lon = location(url)
    p1,h1,t1,td1 = read_sounding(url1)
    p2,h2,t2,td2 = read_sounding(url2)
    p3,h3,t3,td3 = read_sounding(url3)
    
    plt.figure(0)
    plt.plot(t1,h1,'g--')
    plt.plot(t2,h2,'k--')
    plt.plot(t3,h3,'r--')
    plt.title('Temperature at Different Altitudes')
    plt.xlabel("Temperature [°C]")
    plt.ylabel("Altitude [m]")
    plt.legend(['75° N','45° N','12°N'])
    plt.show()
    
    plt.figure(0)
    plt.plot(td1,h1,'g--')
    plt.plot(td2,h2,'k--')
    plt.plot(td3,h3,'r--')
    plt.title('Dewpoint Temperature at Different Altitudes')
    plt.xlabel("Dewpoint Temperature [°C]")
    plt.ylabel("Altitude [m]")
    plt.legend(['75° N','45° N','12°N'])
    plt.show()
    
    import metpy.calc as mpcalc
    from metpy.plots import SkewT
    from metpy.units import units
    
    '''
    Skew T plot for first dataset (url1)
    '''
    
    lat = '74.70'
    lon = '-94.97'
    fig = plt.figure(figsize=(9, 9))
    skew = SkewT(fig)
    t1  = t1 * units.degC
    td1 = td1* units.degC
    p1  = p1 * units.hPa
    # Calculate parcel profile
    prof1 = mpcalc.parcel_profile(p1, t1[0], td1[0]).to('degC')
    #u = np.linspace(-10, 10, len(p)) * units.knots
    #v = np.linspace(-20, 20, len(p)) * units.knots
    skew.plot(p1, t1, 'r',label = 'Temperature')
    skew.plot(p1, td1, 'g', label = 'Dewpoint T')
    skew.plot(p1, prof1, 'k', label = 'Parcel Profile')  # Plot parcel profile
    #skew.plot_barbs(p[::2], u[::2], v[::2])
    skew.ax.set_xlim(-50, 35)
    skew.ax.set_ylim(1000, 100)
    # Add the relevant special lines
    skew.plot_dry_adiabats(label = 'Dry Adiabats')
    skew.plot_moist_adiabats(label = 'Moist Adiabats')
    skew.plot_mixing_lines(label = 'Mixing Lines')
    skew.shade_cape(p1, t1, prof1, label = 'CAPE')
    skew.shade_cin(p1, t1, prof1, label = 'CIN')
    plt.legend()
    plt.title('lat='+str(lat)+' lon='+str(lon))
    plt.show()   
    
    
    '''
    Skew T plot for second dataset (url2)
    '''
    
    lat = '44.91'
    lon = '-123.00'
    fig = plt.figure(figsize=(9, 9))
    skew = SkewT(fig)
    t2  = t2 * units.degC
    td2 = td2* units.degC
    p2  = p2 * units.hPa
    # Calculate parcel profile
    prof2 = mpcalc.parcel_profile(p2, t2[0], td2[0]).to('degC')
    #u = np.linspace(-10, 10, len(p)) * units.knots
    #v = np.linspace(-20, 20, len(p)) * units.knots
    skew.plot(p2, t2, 'r', label = 'Temperature')
    skew.plot(p2, td2, 'g', label = 'Dewpoint T')
    skew.plot(p2, prof2, 'k', label = 'Parcel Profile')  # Plot parcel profile
    #skew.plot_barbs(p[::2], u[::2], v[::2])
    skew.ax.set_xlim(-50, 35)
    skew.ax.set_ylim(1000, 100)
    # Add the relevant special lines
    skew.plot_dry_adiabats(label = 'Dry Adiabats')
    skew.plot_moist_adiabats(label = 'Moist Adiabats')
    skew.plot_mixing_lines(label = 'Mixing Lines')
    skew.shade_cape(p2, t2, prof2, label = 'CAPE')
    skew.shade_cin(p2, t2, prof2, label = 'CIN')
    plt.legend()
    plt.title('lat='+str(lat)+' lon='+str(lon))
    plt.show()   
    
    
    '''
    Skew T plot for third dataset (url3)
    '''
    
    lat = '12.20'
    lon = '-68.96'
    fig = plt.figure(figsize=(9, 9))
    skew = SkewT(fig)
    t3  = t3 * units.degC
    td3 = td3* units.degC
    p3  = p3 * units.hPa
    # Calculate parcel profile
    prof3 = mpcalc.parcel_profile(p3, t3[0], td3[0]).to('degC')
    #u = np.linspace(-10, 10, len(p)) * units.knots
    #v = np.linspace(-20, 20, len(p)) * units.knots
    skew.plot(p3, t3, 'r', label = 'Temperature')
    skew.plot(p3, td3, 'g', label = 'Dewpoint T')
    skew.plot(p3, prof3, 'k', label = 'Parcel Profile')  # Plot parcel profile
    #skew.plot_barbs(p[::2], u[::2], v[::2])
    skew.ax.set_xlim(-50, 35)
    skew.ax.set_ylim(1000, 100)
    # Add the relevant special lines
    skew.plot_dry_adiabats(label = 'Dry Adiabats')
    skew.plot_moist_adiabats(label = 'Moist Adiabats')
    skew.plot_mixing_lines(label = 'Mixing Lines')
    skew.shade_cape(p3, t3, prof3, label = 'CAPE')
    skew.shade_cin(p3, t3, prof3, label = 'CIN')
    plt.legend()
    plt.title('lat='+str(lat)+' lon='+str(lon))
    plt.show()   
    
    '''
    #2-D Plot Tasks
    # save data to the local disk
    def isfloat(num):
        try:
            float(num)
            return True
        except ValueError:
            return False
        
    outdir='./'
    mon=['01','02','03','04','05','06','07','08','09','10','11','12']
    days=['31','28','31','30','31','30','31','31','30','31','30','31']
    
    rh = []
    temp = []
    height = []
    date = []
    day = 0
    for i in range(12):
        print(mon[i])
        url = 'http://weather.uwyo.edu/cgi-bin/sounding?region=naconf&TYPE=TEXT%3ALIST&YEAR=2022&MONTH='+mon[i]+'&FROM=0100&TO='+days[i]+'12&STNM=72476'
        urllib.request.urlretrieve(url, outdir + 'Sonde_'+mon[i]+'_2.txt')  
        # Save each month to an array
        # lines = urllib.request.urlopen(url).readlines()
        fname = 'Sonde_'+mon[i]+'_2.txt'
        f = open(fname,'r')
        lines = f.readlines()
        f.close()
        tempDate = []
        
        for line in lines:
            entry = line.split()
            if len(entry) == 9 and entry[0] == '<H2>72694':
                tempDate = entry[6],entry[7]
                day += 1
            if len(entry) == 11 and isfloat(entry[0]) == True:
                height.append(float(entry[1]))  # Height data at each row
                rh.append(float(entry[4]))      # RH data at each row
                temp.append(float(entry[2]))    # Temp data at each row
                date.append(tempDate)           # Date at each row
                
    height = np.array(height)
    rh = np.array(rh)
    temp = np.array(temp)
    date = np.array(date)           
    
    x = np.arange(0,365,1)   
    y = np.arange(0,int(max(height)),100)
    grid=np.empty([len(x),len(y)])
    for i in x:
        for j,j1 in enumerate(y):
            grid[i,j] = i+j1
        
    from scipy import interpolate
    H_new = np.arange(100,15000,100)
    f_rh = interpolate.interp1d(np.array(height),np.array(rh),fill_value='extrapolate')
    Rh_new = f_rh(H_new)
    
    f_t = interpolate.interp1d(np.array(height),np.array(temp),fill_value='extrapolate')
    Temp_new = f_t(H_new)
    '''
    
    '''
    Plotting 2-D Arrays for RH and T data
    '''
    import matplotlib.pyplot as plt
    from scipy import interpolate
    import matplotlib.cm as cm

    
    outdir='./'
    mon=['01','02','03','04','05','06','07','08','09','10','11','12']
    days=['31','28','31','30','31','30','31','31','30','31','30','31']
    
    for i in range(12):
        url = 'http://weather.uwyo.edu/cgi-bin/sounding?region=naconf&TYPE=TEXT%3ALIST&YEAR=2022&MONTH='+mon[i]+'&FROM=0100&TO='+days[i]+'12&STNM=71815'
        urllib.request.urlretrieve(url, outdir + 'Sonde_'+mon[i]+'_2.txt')  
        # Save each month to an array
    
    T_2d=np.empty([149,365])
    RH_2d=np.empty([149,365])
    H_new=np.arange(100,15000,100)
    idays=0
    for imon in range(12):
        f=open(outdir + 'sonde_'+mon[imon]+'_2.txt', 'r')
        lines = f.readlines()
        num=0
        start_line=[]
        end_line=[]
        for line in lines:
            entries = line.split()
            num=num+1
            #print(entries)
            if 'at' in entries:
                id=entries.index('at')
                if (entries[id+1][-1]) == 'Z':
                    time=entries[id+1][0:2]
                    day=entries[id+2][0:2]
                    print(' time:',time,day,num)
                    num0=num
                    start_line.append(num)
        N_sonde=len(start_line)
        end_line = np.array(start_line.copy())  + 74
        for i in range(1,N_sonde-1):
            if end_line[i] >  start_line[i+1]:
                end_line[i]=start_line[i+1]
          
        for I in range(N_sonde):
            print('imon:',imon,idays,start_line[I])
            p,h,t,rh   = read_sounding_multiple(lines,start_line[I],end_line[I])
            f_t = interpolate.interp1d(np.array(h),np.array(t),fill_value='extrapolate')
            f_rh = interpolate.interp1d(np.array(h),np.array(rh),fill_value='extrapolate')

            T_2d[:,idays]=f_t(H_new)
            
            rh_new = f_rh(H_new)
            for p in range(149):
                if rh_new[p] > 100:
                    rh_new[p] = 100
                if rh_new[p] < 0:
                    rh_new[p] = 0  
            RH_2d[:,idays]=rh_new
            
            idays=idays+1
            if idays >364: break
        if idays >364: break
        
    print(idays) 
    x=np.arange(0,365,1)
    y=H_new/1000.
    
    fig, ax = plt.subplots()
    img=ax.imshow(T_2d[:, :],extent=(x.min(), x.max(), y.min(), y.max()),
               interpolation='nearest', cmap=cm.gist_rainbow,aspect=15,origin 
    ='lower')
    ax.set_title("Temperature [°C]")
    ax.set_xlabel('Days',size=20)
    ax.set_ylabel('Altitude [km]',size=20)
    cbar=fig.colorbar(img, ax=ax,label='Temperature [°C]',spacing='proportional')
    
    
    fig, ax = plt.subplots()
    img=ax.imshow(RH_2d[:, :],extent=(x.min(), x.max(), y.min(), y.max()),
               interpolation='nearest', cmap=cm.gist_rainbow,aspect=15,origin 
    ='lower')
    ax.set_title("RH [%]")
    ax.set_xlabel('Days',size=20)
    ax.set_ylabel('Altitude [km]',size=20)
    cbar=fig.colorbar(img, ax=ax,label='RH [%]',spacing='proportional')
    

