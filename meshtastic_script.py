import time
import meshtastic
import subprocess
import board
from adafruit_ms8607 import MS8607

textMessage = "text message not yet defined"
destNode = '!fcc1b36f'

i2c = board.I2C()

sensor = MS8607(i2c)

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
            textMessage = (f"{sensor.temperature:.2f}"+f"{sensor.relative_humidity:.2f}"+f"{sensor.pressure:.1f}"+time.strftime("%H%M%S")).replace(".", "")
            
            runCmd("--sendtext '" + textMessage + "' --dest " + destNode)

            time.sleep(5)

        except KeyboardInterrupt:
            print("breaking due to keyboard interrupt")
            break
    
if __name__ == "__main__":
    main()
            
