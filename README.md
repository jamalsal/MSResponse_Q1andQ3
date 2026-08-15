# MSResponse_Q1andQ3
## Question 1
### Choice of Microcontroller [1]
* MCU: STM32L476
* Clock speed: 80 MHz
* Flash memory: 1MB
* SRAM memory: 128kB 

The STM32L4 family is a Cortex M4 ulta-low power class of microcontrollers, with applications in wearable devices. The required sustained rate of data writing is 10 Mb/min, or about 20.8 kB/s. This is a low data rate compared to the 80 MHz clock speed of the STM32L476. Writing continuously at such a rate for an extended period of time, such as a day, would use 1.8 GB. The internal 1MB flash memory is not sufficient for this purpose; therefore, an SD-card interface would be required. 

### Buffer Sizing and Strategy
The size of the double buffer would have to take the 128kB SRAM into consideration. An interrupt Service routing can be used instead of polling.

### References
[1]“STM32L476RG - Ultra-low-power with FPU Arm Cortex-M4 MCU 80 MHz with 1 Mbyte of Flash memory, LCD, USB OTG, DFSDM - STMicroelectronics.” Accessed: Aug. 15, 2026. [Online]. Available: https://www.st.com/en/microcontrollers-microprocessors/stm32l476rg.html

___

## Question 3
### Overview
A python script implements peak detection of PPG signals, beat segmentation and autocorrelation.

### Installation
#### Prerequisites
Python 3.12
#### Installation
Download and open directory
```
git clone https://github.com/jamalsal/MSResponse_Q1andQ3
cd MSResponse_Q1andQ3
```
Install the required libraries
```
pip install matplotlib numpy
```

### Running
Ensure "Human_example_ppg.txt" is in the project directory, and run from the command line:
```
python main.py
```

### Dataset
The dataset used is from the work of Goda et al., and contains 3 minutes of PPG recordings, sampled at 100Hz.
The dataset can be found here:
[PhysioZoo PPG](https://pyppg.readthedocs.io/en/latest/tutorials/PZ_PPG.html) [1]

### Methodology and Results
For systolic peak detection, a threshold of 0.75 of the maximum intensity of the PPG signal is used. In a loop, each element of the signal is tested if it is larger than both elements preceding and succeeding it, and if it crosses the threshold. The index of the element is added to an array. Figure 1 shows the peaks overlaid on the raw signal:

<img width="400" height="300" alt="Figure_1" src="https://github.com/user-attachments/assets/55003f7c-04f6-4d03-847c-23b9bbfde2bc" />

The beat segmentation was performed from the peaks indexed during peak detection. Although this function was not used in the final version, it was kept for potential future uses.

The autocorrelation function (figure 2) [2] was used to calculate the correlation between successive beats in the signal.

<img width="488" height="82" alt="autocorrelation" src="https://github.com/user-attachments/assets/7f13e5e6-6fc5-4f26-8802-5f0189d27867" />

The correlation for the successive 10 cycles is shown in figure 3. The graph shows the correlation decreasing, despite the PPG graph exhibiting a normal shape. This is caused by the change in intensity of the signals, which could have been caused by a change in the position of the photoplethysmographic sensor. This could be mitigated by dividing the signal into smaller windows, where the autocorrelation function is performed on neighbouring beats.

<img width="400" height="300" alt="Figure_2" src="https://github.com/user-attachments/assets/cf724e4f-7c43-46f6-a85b-bb59c2f6fd32" />

### Future Improvements
* A bandpass filter can be implemented to allow the use on noisy data
* The peak detection function can be affected by outliers. The use of a different peak detection solution, such as an Aboy algorithm [3] 
* The autocorrelation function can be updated to allow for more accurate correlation figures between neighbouring beats
### Use of LLMs 
Claude was used in the debugging of the Python script.

### References
[1]M. Á. Goda, P. H. Charlton, and J. A. Behar, “pyPPG: a Python toolbox for comprehensive photoplethysmography signal analysis,” Physiological Measurement, Mar. 2024, doi: 10.1088/1361-6579/ad33a2.

[2]M. Angel Garcia-Gonzalez, M. Mohammadpoorfaskhodi, M. Fernandez Chimeno, and J. Jose Ramos-Castro, “Autocorrelation Function Based Signal Quality Assessment on Photoplethysmographic Recordings for Opportunistic Accurate Estimation of RR Time Series,” Computing in Cardiology Conference (CinC), vol. 51, Dec. 2024, doi: 10.22489/cinc.2024.020.

[3] M. Aboy, J. McNames, T. Thong, D. Tsunami, M. S. Ellenby, and B. Goldstein, “An Automatic Beat Detection Algorithm for Pressure Signals,” IEEE Transactions on Biomedical Engineering, vol. 52, no. 10, pp. 1662–1670, Oct. 2005, doi: 10.1109/tbme.2005.855725.
