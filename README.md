# Project Location for Ensemble Perception VR Experiment
testing rapid estimation of an ensemble average size with varying distance within a virtual reality envrionement.  

## To run the experiment
- download [vizard 7](https://www.worldviz.com/releases/vizard-7)
- have your steamVR enabled VR headset turned on and ready
- run the Experiment.py file within the repo

## Information
- 'ParticipantData': file where each participant's data is stored in csv format
- 'textures': stores jpg files for use within the experiment as textures if setting is turen on
- 'currentParticipant': stores the number of the next participant, used to automatically write file names within 'ParticipantData'. If you run this experiment again, make sure to check that this value is reset to 1 before the first participant.
- 'Experiment.py': where the experiment is run from. You must have the vizard 7 software downloaded to run the file.
- 'analysis.rmd': where the data analysis occurs on the data within 'ParticipantData'
