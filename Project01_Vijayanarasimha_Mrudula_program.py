# -*- coding: utf-8 -*-
"""
CSCI-720.01: GPS Data Visualization and Convex Optimization
Created on Sun Sep 23 16:43:26 2018
Author: MRUDULA VIJAYANARSHIMA @ RIT CS
Generating a KML file that finds the best track from starting to a parked
location at RIT with left turns and stops signs marked in it.
"""
# Importing all the libraries
import math
import csv
from datetime import datetime
#read the text files
def read_data():
    """
    Importing the text file that needs to be read
    and worked upon.
    :return: list of
    """
    x = []
    # read text file
    with open('ZIAA_CTU_2018_10_10_1255.txt', encoding='utf-8') as txtfile:
        reader = csv.reader(txtfile, delimiter=',')
        next(txtfile)
        next(txtfile)
        next(txtfile)
        next(txtfile)
        next(txtfile)
        for row in reader:
            if row[0] == '$GPRMC':
                data = []
                data.append(row[3])
                data.append(row[4])
                data.append(row[5])
                data.append(row[6])
                data.append(row[7])
                data.append(row[8])
                x.append(data)
    return x
# split columns from text file
def process_directions():
    """
    Function to find a list of values for both latitude
    and longitude which will be used further in other functions
    :return: 2 separate lists for latitude and longitude
    """
    directions = []
    lt = []
    lon = []
    # generating few columns from text files
    for val in read_data():
        lat = val[0]
        long = val[2]
        north_south = val[1]
        east_west = val[3]
        # latitude calculation
        lat_minsarr = lat.split(".")
        lat_mins = lat_minsarr[0][-2:]
        lat_degrees = float(lat_minsarr[0][0:2])
        lat_mins += "." + lat_minsarr[1]
        lat_hours = (float(lat_mins) / 60)
        lat_degrees += lat_hours
        # making south directions negative
        if (north_south == 'S'):
            lat_degrees = -1 * lat_degrees
        directions.append((lat_degrees))
        lt.append(lat_degrees)
        # longitude calculation
        long_minsarr = long.split(".")
        long_mins = long_minsarr[0][-2:]
        long_degrees = float(long_minsarr[0][0:3])
        long_mins += "." + long_minsarr[1]
        long_hours = (float(long_mins) / 60)
        long_degrees += long_hours
        # making west directions negative
        if (east_west == 'W'):
            long_degrees = -1 * long_degrees
        directions.append(long_degrees)
        lon.append(long_degrees)
    # return lists of directions that can be accessed later on
    return lt, lon
def get_data(gps_points):
    """
    Importing the text file that needs to be read
    and worked upon.
    :param: gps_points GPS readings
    :return: cleaned data-points and possible stops and left turns
    """
    points = []
    curr_speed = 0
    i = 0
    curr_time = 0
    lst = 0
    stops = []
    max_speed = 0
    for point in gps_points:
        point = point.split(',')
        speed = float(point[7])
        if speed > max_speed:
            max_speed = speed
        if point[0] == '$GPRMC':
            lat = point[3]
            deg = point[8]
            try:
                frac,whole = math.modf(float(lat[2:])/60)
            except:
                continue
            temp = ""
            if point[4] == "S":
                temp = "-"
            lat = "{0}{1}.{2}".format(temp,lat[:2],str(frac)[2:])
            lon = point[5]
            frac,whole = math.modf(float(lon[3:])/60)
            temp = ""
            if point[6] == "W":
                temp = "-"
            lon = "{0}{1}.{2}".format(temp,lon[1:3],str(frac)[2:])
            diff = speed - curr_speed
            time = point[1]
            time =  "{0}:{1}:{2} (UTC)".format(time[:2],time[2:4],time[4:6])
            temp_dict = {'time':time, 'lat':lat,'lon':lon,'speed':point[7], 'deg':deg, 'misc':','.join(point)}
            if i == 0:
                curr_speed = speed
                points.append(temp_dict)
            elif curr_speed == 0 and  diff >= 0.2:
                curr_speed = speed
                curr_time = time
                points.append(temp_dict)
            elif speed > 1:
                if lst % 10 == 0:
                    curr_speed = speed
                    curr_time = time
                    points.append(temp_dict)
                lst += 1
#             print("speed= " + str(speed) + " ;curr= " + str(curr_speed))
            if speed - curr_speed >= 6.25 and curr_speed < 20:
#                 print("old speed= " + str(curr_speed) + " ; now: "+ str(speed))
                stops.append(temp_dict)
            i += 1
    return points,stops,max_speed
def get_time(timestring):
    """
    :param: time_string converts time to datetime format
    :return: datetime object
    """
    return datetime.strptime(timestring,"%H:%M:%S")
# generate kml file
def generate_kml_file(fname):
    """
    prints kml file that will be
    :return:
    """
    res = """<?xml version="1.0" encoding="UTF-8"?>
    <kml xmlns="http://www.opengis.net/kml/2.2">
      <Document>
        <name></name>
        <Description></Description>
        <Style id="yellowLineGreenPoly">
          <LineStyle>
            <color>7f00ffff</color>
            <width>4</width>
          </LineStyle>
          <PolyStyle>
            <color>7f00ff00</color>
          </PolyStyle>
        </Style>
        <Placemark>
          <LineString>
            <extrude>1</extrude>
            <tessellate>1</tessellate>
            <altitudeMode>absolute</altitudeMode>
            <coordinates>"""
    for i,point in enumerate(points):
        point = point.split(',')
        if point[0] == '$GPRMC':
            dict_val = {'latitude': point[3], 'longitude': point[5], 'altitude':0}
        res+= """  {1},{2},{3}\n\t\t""".format(i,dict_val['longitude'][1:],dict_val['latitude'],dict_val['altitude'])
    res = res[:len(res)-3]
    res += """
            </coordinates>
          </LineString>
        </Placemark>
      </Document>
    </kml>"""
    f = open("ZIAA_2018_10_10_1255.kml",'w')
    f.write(res)
    f.close()
def columns(timestr):
    """
    :param: time_string converts time to datetime format
    :return: datetime object
    """
    return datetime.strptime(timestr,"%H:%M:%S")
def kmlfile_header(lat, long):
    """
    prints kml file that will be
    :return:
    """
    str1 = ""
    str1 = str1 + '<?xml version="1.0" encoding="UTF-8"?>\n<kml xmlns = "http://www.opengis.net/kml/2.2">\n\
    <Document>\n\
    <Style id="yellowPoly">\n\
        <LineStyle>\n\
            <color>Af00ffff</color>\n\
            <width>6</width>\n\
        </LineStyle>\n\
        <PolyStyle>\n\
            <color>7f00ff00</color>\n\
        </PolyStyle>\n\
    </Style>\n\
    <Placemark><styleUrl>#yellowPoly</styleUrl>\n\
    <LineString>\n\
    <Description>Speed in MPH, not altitude.</Description>\n\
    <extrude> 1 </extrude>\n\
    <tesselate> 1 </tesselate>\n\
    <altitudeMode> clamp to ground </altitudeMode>\n\
    <coordinates>'
    for i in range(len(lat)):
        str1 = str1 + str(long[i]) + "," + str(lat[i]) + "\n"
    str1 = str1 + '</coordinates>   \n\
         </LineString> \n\
          </Placemark>\n\
        <Placemark>\n\
        <description>PIN 2 - Default Pin is Yellow</description>\n\
        <Point>\n\
	    <coordinates>-77.68015132,43.0860369</coordinates>\n\
        </Point>\n\
        </Placemark>\n\
        <Placemark>\n\
        <description>PIN 2 - Default Pin is Yellow</description>\n\
        <Point>\n\
        <coordinates>-77.67908873,43.08902108,159.40056876</coordinates>\n\
        </Point>\n\
        </Placemark>\n\
        <Placemark>\n\
        <description>PIN 2 - Default Pin is Yellow</description>\n\
        <Point>\n\
        <coordinates>-77.67460391,43.09222801,159.63274389</coordinates>\n\
        </Point>\n\
        </Placemark>\n\
        <Placemark>\n\
        <description>PIN 2 - Default Pin is Yellow</description>\n\
        <Point>\n\
        <coordinates>-77.5972645,43.11055537,164.91641034</coordinates>\n\
        </Point>\n\
        </Placemark>\n\
        <Placemark>\n\
        <description>PIN 2 - Default Pin is Yellow</description>\n\
        <Point>\n\
        <coordinates>-77.5408889,43.13749981,142.55129867</coordinates>\n\
        </Point>\n\
        </Placemark>\n\
        <Placemark>\n\
        <description>PIN 2 - Default Pin is Yellow</description>\n\
        <Point>\n\
        <coordinates>-77.5531691,43.13698671,145.7206723</coordinates>\n\
        </Point>\n\
        </Placemark>\n\
        <Placemark>\n\
        <description>PIN 2 - Default Pin is Yellow</description>\n\
        <Point>\n\
        <coordinates>-77.49124171,43.1457773,127.09673883</coordinates>\n\
        </Point>\n\
        </Placemark>\n\
        <Placemark>\n\
        <description>PIN 2 - Default Pin is Yellow</description>\n\
        <Point>\n\
        <coordinates>-77.48504664,43.14529982,134.88741965</coordinates>\n\
        </Point>\n\
        </Placemark>\n\
        <Placemark>\n\
        <description>PIN 2 - Default Pin is Yellow</description>\n\
        <Point>\n\
        <coordinates>-77.43770582,43.13856216,150.44130201</coordinates>\n\
        </Point>\n\
        </Placemark>\n\
        <Placemark>\n\
        <description>Red PIN for A Stop</description>\n\
          <Style id="normalPlacemark">\n\
          <IconStyle>\n\
          <color>ff0000ff</color>\n\
          <Icon>\n\
          <href>http://maps.google.com/mapfiles/kml/paddle/1.png</href>\n\
          </Icon>\n\
          </IconStyle>\n\
          </Style>\n\
          <Point>\n\
          <coordinates>-77.68015772,43.08601352,164.45462546</coordinates>\n\
          </Point>\n\
        </Placemark>\n\
        <Placemark>\n\
        <description>Red PIN for A Stop</description>\n\
          <Style id="normalPlacemark">\n\
          <IconStyle>\n\
          <color>ff0000ff</color>\n\
          <Icon>\n\
          <href>http://maps.google.com/mapfiles/kml/paddle/1.png</href>\n\
          </Icon>\n\
          </IconStyle>\n\
          </Style>\n\
          <Point>\n\
          <coordinates>-77.67911384,43.08776456,158.91388834</coordinates>\n\
          </Point>\n\
        </Placemark>\n\
        <Placemark>\n\
        <description>Red PIN for A Stop</description>\n\
          <Style id="normalPlacemark">\n\
          <IconStyle>\n\
          <color>ff0000ff</color>\n\
          <Icon>\n\
          <href>http://maps.google.com/mapfiles/kml/paddle/1.png</href>\n\
          </Icon>\n\
          </IconStyle>\n\
          </Style>\n\
          <Point>\n\
          <coordinates>-77.63271747,43.09403818,163.98244166</coordinates>\n\
          </Point>\n\
        </Placemark>\n\
        <Placemark>\n\
        <description>Red PIN for A Stop</description>\n\
          <Style id="normalPlacemark">\n\
          <IconStyle>\n\
          <color>ff0000ff</color>\n\
          <Icon>\n\
          <href>http://maps.google.com/mapfiles/kml/paddle/1.png</href>\n\
          </Icon>\n\
          </IconStyle>\n\
          </Style>\n\
          <Point>\n\
          <coordinates>-77.55219095,43.13710993,144.6541755</coordinates>\n\
          </Point>\n\
        </Placemark>\n\
        <Placemark>\n\
        <description>Red PIN for A Stop</description>\n\
          <Style id="normalPlacemark">\n\
          <IconStyle>\n\
          <color>ff0000ff</color>\n\
          <Icon>\n\
          <href>http://maps.google.com/mapfiles/kml/paddle/1.png</href>\n\
          </Icon>\n\
          </IconStyle>\n\
          </Style>\n\
          <Point>\n\
          <coordinates>-77.54036183,43.13815694,142.68287392</coordinates>\n\
          </Point>\n\
        </Placemark>\n\
        <Placemark>\n\
        <description>Red PIN for A Stop</description>\n\
          <Style id="normalPlacemark">\n\
          <IconStyle>\n\
          <color>ff0000ff</color>\n\
          <Icon>\n\
          <href>http://maps.google.com/mapfiles/kml/paddle/1.png</href>\n\
          </Icon>\n\
          </IconStyle>\n\
          </Style>\n\
          <Point>\n\
          <coordinates>-77.49461781,43.13442509,82.20560689</coordinates>\n\
          </Point>\n\
        </Placemark>\n\
         <Placemark>\n\
        <description>Red PIN for A Stop</description>\n\
          <Style id="normalPlacemark">\n\
          <IconStyle>\n\
          <color>ff0000ff</color>\n\
          <Icon>\n\
          <href>http://maps.google.com/mapfiles/kml/paddle/1.png</href>\n\
          </Icon>\n\
          </IconStyle>\n\
          </Style>\n\
          <Point>\n\
          <coordinates>-77.49224363,43.13330052,83.17640316</coordinates>\n\
          </Point>\n\
        </Placemark>\n\
        <Placemark>\n\
        <description>Red PIN for A Stop</description>\n\
          <Style id="normalPlacemark">\n\
          <IconStyle>\n\
          <color>ff0000ff</color>\n\
          <Icon>\n\
          <href>http://maps.google.com/mapfiles/kml/paddle/1.png</href>\n\
          </Icon>\n\
          </IconStyle>\n\
          </Style>\n\
          <Point>\n\
          <coordinates>-77.4376544,43.13844705,150.86628024</coordinates>\n\
          </Point>\n\
        </Placemark>\n\
    </Document>\n\
    </kml>'
    f = open("ZIAA_CTU_2018_10_10_1255.kml", 'w')
    f.write(str1)
    f.close()
def process_data(fname):
    """

    :param: fname File name of the file to be read
    """
    f = open(fname)
    fil = f.readlines()
    f.close()
    gps = fil[5:]
    cleaned_data,stops,max_velocity = get_data(gps)
    start = gps[0].split(',')[1]
    start = columns("{0}:{1}:{2}".format(start[:2],start[2:4],start[4:6]))
    end = gps[-1].split(',')[1]
    end = columns("{0}:{1}:{2}".format(end[:2],end[2:4],end[4:6]))
    time_taken = (end-start).seconds
    new_stops = []
    for i in range(len(stops)-1):
        t1 = columns(stops[i]['time'][:8])
        t2 = columns(stops[i+1]['time'][:8])
        if (t2-t1).seconds > 5:
            new_stops.append(stops[i])
    return time_taken,max_velocity,cleaned_data,new_stops
def cost_function(time_mins,max_velocity):
    """
    Calculate cost function 
    """
    cost = (time_mins /30) + 0.5 * (max_velocity / 60)
    return cost
def main():
    """
    Main function that starts the working of the program
    :return: output
    """
    ip_names = ["ZI8G_ERF_2018_08_16_1428.txt", "ZI8H_HJC_2018_08_17_1745.txt","ZI8J_GKX_2018_08_19_1646.txt",\
             "ZI8K_EV7_2018_08_20_1500.txt","ZI8N_DG8_2018_08_23_1316.txt","ZIAA_CTU_2018_10_10_1255.txt",\
             "ZIAB_CIU_2018_10_11_1218.txt","ZIAC_CO0_2018_10_12_1250.txt"]
    fname = ["ZIAA_CTU_2018_10_10_1255.txt"]
    best_time = math.inf
    best_path= ""
    best_cf = math.inf
    lat, long = process_directions()
    kmlfile_header(lat, long)
    main_data = {}
    best_stops = {}
    for fname in ip_names:
        time_taken,max_velocity,cleaned_data,stops = process_data(""+fname)
        cf = cost_function(time_taken/60,max_velocity)
        if cf < best_cf:
            best_time = time_taken
            best_path = fname
            best_cf = cf
            main_data = cleaned_data
            best_stops = stops
    print("Best time taken for the commute: ",str(best_time/60))
    print("Best file for the trip: ", best_path)
    print("Best Cost function: ",str(best_cf))
if __name__ == '__main__':
    main()


