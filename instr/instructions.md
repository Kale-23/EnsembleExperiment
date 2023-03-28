# Instructions for VR Experiment
- if you have any questions, don't be afraid to text Kaleb for help, my number is (603) 948 5346

## Setup Before Participant Arrives
- Make sure HDMI cable is connected to both the headset and computer through the GPU HDMI port
    - this should already be plugged in correctly, but if it is unplugged for any reason text me and I can tell you how to plug it back in if you don't know how
- press the power button on the top of the computer, and wait for the screen to startup
- once screen is on, select the lab profile, and log in
    - user ID: svc_UNH_Psy_Ksk01
    - password: interdisciplinary perception lab 
        - **(spaces included, no caps)**
- open the "Vizard 7" app, you will see the icon in the bottom bar **(seen below)**
  
<img src="viz.jpg" alt="vizard logo" width="10%" height="10%">

- within vizard, the experiment should already be opened, and you should see "Experiment.py" open in the top left **(Seen below with a red box around it)**
    - if "Experiment.py" is not already open, locate the "EnsembleExperiment" folder on the desktop, and drag the "Experiment.py" file into Vizard. You should then see it in the top left, and it should be highlighted yellow to show it is open

<img src="InkedvizIDE.jpg" alt="vizard IDE" width="80%">

- press the green arrow that is above and to the left of the "Experiment.py" label **(seen above with a red arrow pointing towards it)**
    - a new screen should pop up with a text entry field labeled "Please put in your information"
        - during setup, we skip putting in information and just click "Submit" right away
    
- another new screen called "Mixed Reality Portal" should open, and the headset should now be connected. You can verify this by looking through the headset and making sure it is turned on

## After Participant Arrives
- make sure to be on the lookout for the participant arriving, this hallway is confusing so they may get lost around here
- when the participant arrives, greet them and bring them into the lab room.
  - on your way in, make sure to switch the sign to say "Experiment in progress" on the door
  - Ask the participant to put all thier devices on silent **(and you should do the same)** and place their phone/ smart watch/ anything that could cause a distraction on the shelf or table nearby
- Ask the participant to sit down at a desk, and hand them the consent form to fill out. Tell them if they have any questions about it or are confused that they can ask you for help or clarification.
- Once they complete the consent form and you check to make sure everything is filled out correctly, you can sit the participant out front of the desk with the VR headset on it.
  
### Taking IPD
- Tell the participant you will now measure their inter pupulary distance. Warn the participant that you will get close and touch the bridge of their nose with a ruler
- Once the participant consents to getting their IPD taken, use the ruler branded "zyaid" on the side to take their IDP
  - Ask the participant to stare directly over your shoulder, line the 0mm mark up with the middle of their left pupil, and measure the distance to the middle of their right pupil. Make sure to write this numebr down or remember it for later.

### Starting the Experiment
- Once everything is ready, ask the participant to remove any head covering or hair style that may get in the way of putting on the VR headset **(If they have a religious headcovering please don't ask them to remove it, try to work around it)**
- Start up the experiment again using the green arrow.
- Have the participant fill out the form this time, making sure to put in the correct IPD.
- Ask the participant which hand they would prefer to hold the controller in, and turn that one on. **(if both controllers are on, hold the windows button to turn the one not in use off before the participant presses submit)**
- look at the Vizard screen at the bottom, if you see the message below **(it will be highlighted in red in vizard)**, you need to restart the program by closing out and pressing the green arrow again
  - the controller will not work if this message is seen

<span style="color:red"> 
Traceback (most recent call last):  <br />
&nbsp; File "C:\Program Files\WorldViz\Vizard7\python\viztask.py", line 773, in updateAndKillOnException  <br />
  &nbsp;&nbsp;&nbsp;&nbsp;  return self.update()  <br />
&nbsp;  File "C:\Program Files\WorldViz\Vizard7\python\viztask.py", line 738, in update  <br />
  &nbsp;&nbsp;&nbsp;&nbsp;  val = self._stack[-1].send(sendData)  <br />
&nbsp; File "C:\Users\svc_UNH_Psy_Ksk01\Desktop\EnsembleExperiment\Experiment.py", line 525, in learningPhase  <br />
  &nbsp;&nbsp;&nbsp;&nbsp;  yield viztask.waitSensorDown(controller, [steamvr.BUTTON_TRIGGER])  <br />
NameError: name 'controller' is not defined  <br />
</span>
<br />

- if this message does not show up, the experiment is ready to be run
- put the headset on the participant, making sure to adjust the back knob to make it tight, as well as the velcrow top to pull it higher up **(if the headset is not properly adjusted, the participant will have blurry vision, ask to make sure it is comfortable and they can see clearly)**
- Either ask to adjust the IPD using the slider below their right eye, or have the participant do it themselves. Get it as close as possible to the number you measured earlier
- Hand the participant the controller, **make sure to slide the wrist wrap over their wrist, these controllers are expensive**

### Guiding Participant Through the Experiment
- When the participant begins, keep track of their progress using both the "Mixed reality Portal" and "Experiment" windows. 
  - You will see when they reach the tutorials through these windows, so Ask them if they understand, and talk them through the learning phases.
    - They have a learning phase for the depth test as well as the overall experiment, so make sure they seem to know what they are doing 
    - **do not guide them or give tips or any information through the actual test and experiment, we want as little instructor input after the learning phases so as not to skew the results. Do not tell them how many trials there are, or answer questions about how good they are doing for example. You can tell them "I can answer that at the end of the experiment"**
- When the participant gets through around 50 trials of the experiment, they will reach a break period. The participant can rest here as long as they like, but make sure they do not take off their headset.
- When the participant finishes, they will be told to take off their headset. Help the participant if they need it.
- If the participant sees the experiment over screen, all the data has already been saved, it is safe to exit out of all programs
  - If another participant is scheduled, you can keep the "Vizard" and "Mixed Reality Portal" windows open, but need to close the "Experiment" window
- Ask the participant if they have any questions about the experiment. Try to answer as best as possible.
- Tell the participant that you will put their sona credit into the system, and they should see it within a couple of minutes. **Make sure they grab all of their belongings before leaving, and to thank them for their time**
- Put information into the Excel Spreadsheet "Participant LogBook" 
  - Participant number should be the last entry within the "Participant Data" folder within the "EnsembleExperiment" folder.