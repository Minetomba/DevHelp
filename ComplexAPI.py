import sys
import subprocess
operating = sys.platform
import os
import base64

ENCODING = 'utf-8'

class Cryptography:
    def encode(message):
		binary_message = ''.join(format(ord(char), '08b') for char in message)
        hex_message = hex(int(binary_message, 2))[2:]
        base64_message = base64.b64encode(bytes.fromhex(hex_message)).decode(ENCODING)
        binary_base64 = ''.join(format(ord(char), '08b') for char in base64_message)
        reversed_message = binary_base64[::-1]
        encrypted_message = f"s+{reversed_message}="
        return encrypted_message

    def decode(encrypted_message):
        if encrypted_message.startswith("s+") and encrypted_message.endswith("="):
            reversed_message = encrypted_message[2:-1][::-1]
            binary_base64 = ''.join(chr(int(reversed_message[i:i+8], 2)) for i in range(0, len(reversed_message), 8))
            decoded_base64 = base64.b64decode(binary_base64)
            binary_message = ''.join(format(byte, '08b') for byte in decoded_base64)
            original_message = ''.join(chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message), 8))
            return original_message
        return None

import os
import zipfile

class BackupSystem:
    def __init__(self, source_dir, zip_file, txt_file, restore_dir):
        """
        Initialize the BackupSystem class with paths.

        Args:
            source_dir (str): Path to the source directory to be zipped.
            zip_file (str): Path to the output ZIP file.
            txt_file (str): Path to the output .txt file containing ZIP contents.
            restore_dir (str): Path to the directory where contents are restored.
        """
        self.source_dir = source_dir
        self.zip_file = zip_file
        self.txt_file = txt_file
        self.restore_dir = restore_dir

    def zip_directory(self):
        """
        Compress the source directory into a ZIP file.
        """
        with zipfile.ZipFile(self.zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(self.source_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, start=self.source_dir)  # Preserve folder structure
                    zipf.write(file_path, arcname)
        print(f"Directory '{self.source_dir}' has been zipped into '{self.zip_file}'.")

    def zip_to_txt(self):
        """
        Reads the contents of a ZIP file and stores them in a .txt file.
        """
        with zipfile.ZipFile(self.zip_file, 'r') as zipf, open(self.txt_file, 'w') as txtf:
            for file_info in zipf.infolist():
                txtf.write(f"File: {file_info.filename}\n")
                with zipf.open(file_info) as file:
                    file_content = file.read().decode(errors='ignore')  # Handle text/binary files safely
                    txtf.write(f"Contents:\n{file_content}\n")
        print(f"ZIP file '{self.zip_file}' contents have been written to '{self.txt_file}'.")

    def recover_zip_and_delete(self):
        """
        Recreate the ZIP file from the .txt file, unzip its contents, and delete the original ZIP.
        """
        # Recreate the ZIP from the .txt
        self.txt_to_zip()

        # Extract ZIP contents into the restore directory
        with zipfile.ZipFile(self.zip_file, 'r') as zipf:
            zipf.extractall(self.restore_dir)

        # Delete the original ZIP file
        os.remove(self.zip_file)
        print(f"ZIP file '{self.zip_file}' deleted. Directory restored to '{self.restore_dir}'.")

    def txt_to_zip(self):
        """
        Creates a ZIP file from the contents of the .txt file.
        """
        with open(self.txt_file, 'r') as txtf, zipfile.ZipFile(self.zip_file, 'w') as zipf:
            lines = txtf.readlines()
            file_name = None
            content = []

            for line in lines:
                if line.startswith("File:"):
                    # Write the previous file into the ZIP if it exists
                    if file_name and content:
                        zipf.writestr(file_name, ''.join(content))
                    
                    # Start a new file
                    file_name = line.split("File:")[1].strip()
                    content = []  # Reset content for the new file
                elif line.startswith("Contents:"):
                    continue  # Skip the 'Contents:' line
                else:
                    content.append(line)  # Collect file contents

            # Write the last file into the ZIP
            if file_name and content:
                zipf.writestr(file_name, ''.join(content))

        print(f"ZIP file '{self.zip_file}' has been recreated from '{self.txt_file}'.")
class Backup:
    def create(directoryname, zipname, txtfile, restorename):
        """
        Steps to transform it in TXT: Get directory path, Initiate backup system, zip directory
        transform to txt, remove zip.
        """
        source_directory = os.path.join(os.getcwd(), directoryname)
        print(f"[static] Got source directory path '{source_directory}' [static]")
        zip_file = zipname
        txt_file = txtfile
        restore_directory = restorename
        backup = BackupSystem(source_directory, zip_file, txt_file, restore_directory)
        print("[static] Initiated Backup [static]")
        backup.zip_directory()
        print("[+] Zipped Directory [+]")
        backup.zip_to_txt()
        print("[+] Zip transformed to .txt [+]")
        os.remove(os.path.join(os.getcwd(), zip_file))
        print("[-] Removed ZIP [-]")
    def restore(directoryname, zipname, txtfile, restorename):
        """
        Steps to restore from txt: Get directory path, initiate backupsystem, recover zip, unzip zip, delete zip
        """
        source_directory = os.path.join(os.getcwd(), directoryname)
        print(f"[static] Got source directory path '{source_directory}' [static]")
        zip_file = zipname
        txt_file = txtfile
        restore_directory = restorename
        backup = BackupSystem(source_directory, zip_file, txt_file, restore_directory)
        print("[static] Initiated Backup [static]")
        backup.recover_zip_and_delete()
        print("[+] Restored Backup [+]")
class OSLinker:
    def system(command, output):
        try:
            executed = str(command)
            if executed == "clear":
                if operating in ("win32", "win64", "win86"):
                    return subprocess.run("cls", shell=True, text=bool(output))
                elif operating in ("linux", "darwin"):
                    return subprocess.run("clear", shell=True, text=bool(output))
                else:
                    print("==== - Invalid OS - ====")
                    raise OSError
            if executed == "ipconfig":
                if operating in ("win32", "win64", "win86"):
                    return subprocess.run("ipconfig", shell=True, text=bool(output))
                elif operating in ("linux", "darwin"):
                    return subprocess.run("ifconfig", shell=True, text=bool(output))
                else:
                    print("==== - Invalid OS - ====")
                    raise OSError
            if executed == "ls":
                if operating in ("win32", "win64", "win86"):
                    return subprocess.run("dir", shell=True, text=bool(output))
                elif operating in ("linux", "darwin"):
                    return subprocess.run("ls", shell=True, text=bool(output))
                else:
                    print("==== - Invalid OS - ====")
                    raise OSError
            if executed == "sl":
                if operating in ("win32", "win64", "win86"):
                    return subprocess.run("dir", shell=True, text=bool(output))
                elif operating in ("linux", "darwin"):
                    return subprocess.run("ls", shell=True, text=bool(output))
                else:
                    raise OSError("Invalid OS")
        except KeyboardInterrupt:
            print("Interrupted while executing a system command")
        except Exception as e:
            print(f"Error occured: {e}")
            return str(e)
class Utility:
    # Fix email verification function
    @staticmethod
    def verify_email(email):
        adresa = email
        if "@" in adresa and adresa.endswith((".com", ".net", ".ms", ".mail", ".ro")):
            print("Valid Address")
        else:
            print("Invalid Address")

    # Function to check if a number is negative
    @staticmethod
    def is_negative(numb):
        return numb < 0

    # Radix Sort function that returns the sorted array
    @staticmethod
    def radix_sort(arr):
        if not arr:  # Handle edge case for empty list
            return arr

        def counting_sort(arr, exp):
            n = len(arr)
            output = [0] * n  # Output array to store sorted numbers
            count = [0] * 10  # Count array to store frequency of digits (0-9)

            # Store the count of occurrences for each digit in the numbers
            for i in range(n):
                index = (arr[i] // exp) % 10
                count[index] += 1

            # Update count[i] so that count[i] contains the actual position of this digit in output[]
            for i in range(1, 10):
                count[i] += count[i - 1]

            # Build the output array by placing the elements in their correct position
            i = n - 1
            while i >= 0:
                index = (arr[i] // exp) % 10
                output[count[index] - 1] = arr[i]
                count[index] -= 1
                i -= 1

            # Copy the sorted elements back into the original array
            for i in range(n):
                arr[i] = output[i]

        max_num = max(arr)
        exp = 1  # Represents the digit place (ones, tens, hundreds, etc.)
        while max_num // exp > 0:
            counting_sort(arr, exp)  # Call the nested counting_sort function
            exp *= 10

        return arr  # Ensure the sorted array is returned

    # Function to find the closest value in a list to a given value
    @staticmethod
    def closest_in(listt, to):
        # Convert tuple to list if necessary
        if isinstance(listt, tuple):
            listt = list(listt)

        # Filter out non-numeric items and convert strings to integers if possible
        numeric_list = []
        for item in listt:
            if isinstance(item, (int, float)):
                numeric_list.append(item)
            elif isinstance(item, str):
                try:
                    numeric_list.append(int(item))
                except ValueError:
                    continue  # Skip items that cannot be converted to integers

        # Sort the list using radix_sort (only works for non-negative integers)
        sorted_list = Utility.radix_sort(numeric_list)

        # Find the closest value to 'to'
        to = int(to)
        closest_value = min(sorted_list, key=lambda x: abs(x - to))

        return closest_value
