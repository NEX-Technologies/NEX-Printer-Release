import subprocess
import sys
import time

def main():
    system_config_path = "/boot/config.txt"

    printer_model = read_config(system_config_path, "printer_model")
    serial_port_name = read_config(system_config_path, "serial_port_name")
    upload_baud_rate =  57600
    hex_path = f"/home/pi/G3D-Printer/build/resources/hex/{printer_model}.hex"

    # Override for testing.
    hex_path = "/home/romnegrillo/Desktop/Workspace/sketch_sep05a.ino.hex"

    num_tries = 0
    max_tries = 5

    # Try uploading 5 times to be sure.
    while num_tries < max_tries:
        print("Uploading hex...")
        result = subprocess.run([f"avrdude -v -p atmega328p -c arduino -P {serial_port_name} -b {upload_baud_rate} -D -U flash:w:{hex_path}:i"], shell=True)
        print(f"Return code {result.returncode}")

        num_tries += 1

        # Stop the loop if the upload is successful,
        # when return code is 0.
        if result.returncode == 0:
            print("Upload success.")
            break

        time.sleep(1)

def read_config(path, key):
    try:
        with open(path, "r", newline="") as f:
            for line in f:
                if line.startswith(key):
                    target = line.strip()
                    key, val = target.split("=")
                    key = key.strip()
                    val = val.strip()

                    print(key, val)
        return val

    except Exception as exp:
        print(str(exp))

    return ""

if __name__ == "__main__":
    main()