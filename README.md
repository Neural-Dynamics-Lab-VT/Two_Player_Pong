# Playing pong using EEG
<p align="center">
<img src="/README/pong.png" alt="Pong_screen" width="600px"/>
</p>


## Getting started

### Requirements

Runs only on python 2.7 32-bit. 

1. [Kivy (1.10.0)](https://kivy.org/#home) or later. Follow the instruction on their website to install kivy.
2. Python Lab Streaming Layer. TL;DR `pip install pylsl`. Follow [this](https://github.com/sccn/labstreaminglayer) repo.
3. [OpenVibe](http://openvibe.inria.fr/)
4. Headset software from the vendor.


### Running
1. Connect your EEG headset and stream the EEG signals as an LSL stream. Checkout this [repo](https://github.com/sccn/labstreaminglayer)
  for more details.
2. Start OpenVibe Acquisition server and connect to the desired LSL stream. Ensure that you know the port its streaming to.
3. Start OpenVibe Designer and run the provided xml files under the `OpenVibe_scenarios` folder. This processes the EEG signal and extracts the alpha power which is later streamed using LSL. Ensure the port number in the Acquisition stream box matches the one in OpenVibe acquisition.
4. Run `play_pong.py` to start the game.

### Have fun!
