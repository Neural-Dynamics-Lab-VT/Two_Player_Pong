# Playing pong using EEG
## Not ready yet!

<center> ![Pong_screen](/README/pong.png) </center>

## Getting started

### Requirements
1. [Kivy (1.10.0)](https://kivy.org/#home) or later.

2. Python Lab Streaming Layer. TL;DR `pip install pylsl`. Follow [this](https://github.com/sccn/labstreaminglayer) repo.


### Running
1. Connect your EEG headset and stream the EEG signals as an LSL stream. Checkout this [repo](https://github.com/sccn/labstreaminglayer)
for more details.

2. Start OpenVibe Designer and run the provided xml files under the `OpenVibe_scenarios` folder. This processes the 
EEG signal and extracts the beta power which is later streamed using LSL.

3. Run `play_pong.py` to start the game.

### Have fun!
 


