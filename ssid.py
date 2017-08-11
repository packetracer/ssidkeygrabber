#Load necessary modules
import subprocess
import time
from Tkinter import *

#Define filename to write SSIDs/Keys to
FNAME = 'keys.txt'

#Define function that gathers list of profiles from host machine
def nabProfiles():
	#Set cmd to netsh profile query shell, pass it to shell
	cmd = "netsh wlan show profiles"
	output = subprocess.check_output(cmd)
	
	#Split returned output at line breaks
	output = output.split("\r\n")
	
	#init list of profiles, load them into list
	profileList = []
	for i in range(0,len(output)):
		#Check for existence of phrase "Profile" in return line, split off after colon, take right side of split into list
		if ("Profile" in output[i]):
			if not ("Profiles" in output[i]):
				profileName = output[i].split(": ")
				profileList.append(profileName[1])
	#Send back the parsed list of profile names
	return profileList

#Define function that checks wlan profiles based on gathered list of profile names
def nabKeys(profileList):
	#init local function variables
	entry = []
	bulkout = []
	WEP = False
	textout = []
	#iterate list of profiles, return output of each profile
	for i in range(0,len(profileList)):
		cmd = 'netsh wlan show profile name="' + profileList[i] + '" key=clear'
		output = subprocess.check_output(cmd)
		#begin parsing out nonsense, starting at line breaks
		output = output.split("\r\n")
		for j in range(0,len(output)):
			#check for SSID name phrase, if so, parse, load into output list
			if ("SSID name" in output[j]):
				output[j] = output[j].replace("    ","")
				textout.append(output[j])
			#do same for phrase WEP, also, set bool to True to check for WEP key and decode into ASCII
			if ("WEP" in output[j]):
				WEP = True
			if ("Key Content" in output[j]):
				output[j] = output[j].split(": ")[1]
				if WEP:
					WEP = False
					textout.append("WEP KEY: \nHex:" + output[j] + "\nASCII: "+output[j].decode("hex"))
				else:
					textout.append("WPA KEY: " + output[j])
			#if no authentication for profile, no key info will exist
			if ("None" in output[j]):
				textout.append("No key information for this profile.")
	return textout

#Define function to collect profile names, keys, and return data
def gatherInfo():
	profiles = nabProfiles()
	textout = nabKeys(profiles)
	return textout

#send data to TKinter GUI
def displayInfo(w):
	textout = gatherInfo()
	w = Label(root, text= "SSID Key Info:", justify=LEFT, width=30)
	w.pack()
	w = Label(root, text= "============")

	w.pack()
	texto = ""
	f = open(FNAME,'w')
	f.write('SSID/Keys:\n====================\n\n')
	for i in range(0,len(textout)):
		f.write(textout[i]+'\n')
		texto = texto + textout[i] + "\n"
		if not ("SSID" in textout[i]):
			texto = texto + "*************\n"
			f.write('\n=================\n\n')
	w = Label(root, text = texto,  justify=LEFT)
	w.pack()	

#init GUI, make it do stuff
root = Tk()
root.title("SSID Key Grabber")
w = Label(root,text="", anchor="w",    justify=LEFT)
displayInfo(w)

root.mainloop()
