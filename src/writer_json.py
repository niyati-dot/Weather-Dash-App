import requests
import json
import datetime as dt
import taosrest

# get the data from the API
def get_weather(location, conn):

    # Created key
    payload = {'Key': '26881949144648c69d1174946241707', 'q': location, 'aqi': 'yes'}
    r = requests.get("http://api.weatherapi.com/v1/current.json", params=payload)

    # Geting the json from the request's result
    r_string = r.json()

    # Taking only current part of the JSON
    current = r_string['current']
    #print(current) to checking
    # Fixing time format from YYYY-MM-DD hh:mm:ss to -> YYYY-MM-DDThh:mm:ssZ
    # create datetime object from string
    origin_time = dt.datetime.strptime(current['last_updated'],'%Y-%m-%d %H:%M') 
    
    #turn datetime into formated string for tdengine
    current['last_updated'] = origin_time.strftime('%Y-%m-%dT%H:%M:%SZ')

    #print(current)  
    # write the weather data to tdengine
    write_weather(location,current,conn)    
    return current

#open tdengine connection
def open_con():
 
    # Open a connection to tdengine cloud. Using the url and token specified in the instance
    try:
        conn = taosrest.connect(url="https://gw.us-west-2.aws.cloud.tdengine.com",
                    token="3f86424c957fa1cf04cb41eec876ec83d21879bd"
                    )
 
    except taosrest.Error as e:
        print(e)

    return conn

# Writes the weather data to tdengine
def write_weather(location, weather_js, conn):
    
    # Remove the whitespaces from the locations (tdengine tables don't have whitespaces -> "sanfrancisco" instead of "san francisco")
    no_whitepsace_location = location.replace(" ", "")
 
    # print(no_whitepsace_location)

    # write measurement to tdengine
    conn.query(f"insert into weather.{no_whitepsace_location} values ('{weather_js['last_updated']}', {weather_js['temp_c']}, {weather_js['temp_f']}, {weather_js['wind_mph']}, {weather_js['wind_kph']})")     
    
# closes the tdengine connection
def close_con(conn):
    conn.close()



if __name__ == "__main__":
    
    # open connection
    conn = open_con()
    
    # write data for berlin
    get_weather("barlin",conn)

    # write data for san francisco
    get_weather("san frasciso",conn)

    # close connection and end the program
    close_con(conn)
