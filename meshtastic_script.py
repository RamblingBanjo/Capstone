import time
import meshtastic
import subprocess
import board
from adafruit_ms8607 import MS8607


textMessage = "text message not yet defined"
destNode = '!fcc1b36f'

i2c = board.I2C()

sensor = MS8607(i2c)

def runCmd(cmd):
    process = subprocess.Popen(
        "meshtastic " + cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    
    for line in process.stdout:
        print(line, end="")
        
    process.wait()
    
def main():
    
    runCmd("--port")
    runCmd("--sendtext " + textMessage + " --dest " + destNode)
                
    i = 0
    
    while i<20:
        
        i += 1
        
        try:
            print(f"Temperature: {sensor.temperature:.2f} C")
            print(f"Humidity: {sensor.relative_humidity:.2f} %")
            print(f"Pressure: {sensor.pressure:.2f} hPa")
                
            time.sleep(1)

        except KeyboardInterrupt:
            print("breaking due to keyboard interrupt")
            break
    
if __name__ == "__main__":
    main()
            
