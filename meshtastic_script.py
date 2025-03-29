import time
import meshtastic
import subprocess

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
    runCmd("--sendtext 'range test' --dest '!fcc1b36f'")
                
    i = 0
    
    while i<5:
        
        i += 1
        
        try:
            print("loop is running baby")
                
            time.sleep(1)

        except KeyboardInterrupt:
            print("breaking due to keyboard interrupt")
            break
    
if __name__ == "__main__":
    main()
            
