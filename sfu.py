import subprocess
import os
import shutil
#pip install cryptography
from cryptography.fernet import Fernet
import json


banner = """
╔═╗┌─┐┌─┐┬ ┬┬─┐┌─┐  ╔═╗┬┬  ┌─┐  ╦ ╦┌─┐┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
╚═╗├┤ │  │ │├┬┘├┤   ╠╣ ││  ├┤   ║ ║├─┘│  │ │├─┤ ││├┤ ├┬┘
╚═╝└─┘└─┘└─┘┴└─└─┘  ╚  ┴┴─┘└─┘  ╚═╝┴  ┴─┘└─┘┴ ┴─┴┘└─┘┴└─
"""

file_upload_location = os.getcwd() + "/upload_location/"
reference_file = json.loads(open(os.getcwd() + "/reference_file.json","r").read())
encryption_key = "gFC5uG5ikHoaRJuhAWvDKbN-lETu_eqH7cO1tUZKw8E="

def file_uploader():
  a = input("\n Please enter file name with full path : ")
  file_name_with_location = str(a)
  if os.path.exists(file_name_with_location):
    b = input("\n Please enter email id of the user : ")
    user_email = str(b)
    if len(user_email) > 0:

      print("\n....Saving File....")
      shutil.copy(file_name_with_location, file_upload_location)

      print("\n....Encrypting File....")
      fernet = Fernet(encryption_key)
      fObj = open(file_name_with_location,"r")
      # reading uploaded file
      with open(file_upload_location + fObj.name, 'rb') as file:
        original = file.read()
      # encrypting the file
      encrypted = fernet.encrypt(original)
      # writing the encrypted data
      with open(file_upload_location + fObj.name, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)
      print("\n....Encryption Completed....")
      # update refence file
      reference_file[fObj.name] = {
        "user_email": user_email
      }
      update_reference(reference_file)
      print("\n....Updated Reference File....")
      print("\n....File Upload Completed....")
    else:
      print("\nEmail id required")
  else:
    print("\nInvalid File")

def update_reference(r_data):
  d_str = json.dumps(r_data, indent = 4)
  with open(os.getcwd() + "/reference_file.json","w") as f:
    f.write(d_str)

def send_opt(r_file,f_name):
  r_file[f_name]["otp"] = "1234"
  update_reference(r_file)
  return r_file

def file_download():
  a = input("\n Please enter file name to download (without path) : ")
  file_name = str(a)
  if file_name in reference_file:
    reference_file_updated = send_opt(reference_file,file_name)
    b = input("\n Enter the otp sent to your email for verification : ")
    e_otp = str(b)
    if e_otp == reference_file_updated[file_name]["otp"]:
      print("\n....Decrypting File....")
      fernet = Fernet(encryption_key)
      # opening the encrypted file
      with open(file_upload_location + file_name, 'rb') as enc_file:
        encrypted = enc_file.read()
      # decrypting the file
      decrypted = fernet.decrypt(encrypted)
      with open(file_name, 'wb') as dec_file:
        dec_file.write(decrypted)
      print("\n....File Downloaded....")
    else:
      print("\nInvalid Otp")
  else:
    print("\nInvalid File")

def SFPMain():

    subprocess.call('clear')
    print(banner)

    a = input("\n 1. Upload File\n 2. Download File \n Your input is: ")
    userinput = int(a)
    if (userinput == 1):
        print("\n....Upload Process Begin....")
        file_uploader()

    elif (userinput == 2):
        print("\n....Download Process Begin....")
        file_download()
    else:
        raise Exception("Please provide correct input")

if __name__ == '__main__' :
    # Calling main function
    SFPMain()
