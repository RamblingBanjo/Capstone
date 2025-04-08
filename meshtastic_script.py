import time
import meshtastic
import subprocess
import board
import melopero_samm8q as mp
from adafruit_ms8607 import MS8607


textMessage = "text message not yet defined"
destNode = '!fcc1b36f'

i2c = board.I2C()

sensor = MS8607(i2c)

gps = mp.SAM_M8Q()
gps.set_measurement_frequency(5000)
    
cmdTimeout = 20

def runCmd(cmd):
    try:
        result = subprocess.run(
            "meshtastic " + cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout = cmdTimeout
        )
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
            
    except subprocess.TimeoutExpired:
        print("Timeout occured after {cmdTimeout} seconds. Reconnecting to radio and continuing on.")
        subprocess.run("pkill -x meshtastic", shell=True)
        
        time.sleep(2)
        
        runCmd("--port")
        
        time.sleep(2)
        

    
def main():
    
    runCmd("--port")
    
    print("waiting for radio to initialize")
    time.sleep(5)
                
    i = 0
    
    while i<200:
        
        i += 1
        
        try:
            gps.get_pvt()
            j=0
            nav_data = gps.pvt_data
            
            while j==0:
                print("waiting for GPS connection")
                time.sleep(5)
                gps.get_pvt()
                nav_data = gps.pvt_data
                if nav_data:
                    j = 1
            
            
            print(nav_data)
            
            if nav_data:
                
                latraw = nav_data["latitude"]
                print("latraw: " + str(latraw))
                lat_sign = 0 if latraw > 0 else 1
                print("lat_sign: " +  str(lat_sign))
                lat_value = int(abs(latraw) * 100000)
                print("lat_value: " + str(lat_value))
                lat_str = f"{lat_sign}{lat_value:08d}"
                print("lat_str" + lat_str)
                
                lonraw = nav_data["longitude"]
                print("lonraw" + str(lonraw))
                lon_sign = 0 if lonraw > 0 else 1
                print("lon_sign" + str(lon_sign))
                lon_value = int(abs(lonraw) * 100000)
                print("lon_value" + str(lon_value))
                lon_str = f"{lon_sign}{lon_value:08d}"
                print("lon_str" + lon_str)
                
                altraw = nav_data["MSL_height"]
                alt_str = f"{altraw:08d}"
                print(alt_str)
                
            textMessage = (f"{sensor.temperature:.2f}"+f"{sensor.relative_humidity:.2f}"+f"{sensor.pressure:.1f}"+lat_str + lon_str + alt_str + time.strftime("%H%M%S")).replace(".", "")
            
            runCmd("--sendtext '" + textMessage + "' --dest " + destNode)

            time.sleep(5)

        except KeyboardInterrupt:
            print("breaking due to keyboard interrupt")
            break
    
if __name__ == "__main__":
    main()
            
