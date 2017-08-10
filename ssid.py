import subprocess
import time
from Tkinter import *



def nabProfiles():
	cmd = "netsh wlan show profiles"
	output = subprocess.check_output(cmd)
	output = output.split("\r\n")
	profileList = []
	for i in range(0,len(output)):
		if ("Profile" in output[i]):
			if not ("Profiles" in output[i]):
				profileName = output[i].split(": ")
				profileList.append(profileName[1])
	return profileList

def nabKeys(profileList):
	entry = []
	bulkout = []
	WEP = False
	textout = []
	for i in range(0,len(profileList)):
		cmd = 'netsh wlan show profile name="' + profileList[i] + '" key=clear'
		output = subprocess.check_output(cmd)
		output = output.split("\r\n")
		for j in range(0,len(output)):
			if ("SSID name" in output[j]):
				output[j] = output[j].replace("    ","")
				textout.append(output[j])
			if ("WEP" in output[j]):
				WEP = True
			if ("Key Content" in output[j]):
				output[j] = output[j].split(": ")[1]
				if WEP:
					WEP = False
					textout.append("WEP KEY: " + output[j].decode("hex"))
				else:
					textout.append("WPA KEY: " + output[j])
			if ("None" in output[j]):
				textout.append("No key information for this profile.")
	return textout
	
def gatherInfo():
	profiles = nabProfiles()
	textout = nabKeys(profiles)
	return textout

def displayInfo(w):
	textout = gatherInfo()
	w = Label(root, text= "SSID Key Info:", justify=LEFT, width=30)
	w.pack()
	w = Label(root, text= "============")

	w.pack()
	texto = ""
	for i in range(0,len(textout)):
		texto = texto + textout[i] + "\n"
		if not ("SSID" in textout[i]):
			texto = texto + "*************\n"
	w = Label(root, text = texto,  justify=LEFT, width=30)
	w.pack()	
	
root = Tk()
root.title("SSID Grabber")
w = Label(root,text="", anchor="w",    justify=LEFT, width=30)
displayInfo(w)

root.mainloop()