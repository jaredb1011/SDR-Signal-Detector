# SDR-Signal-Detector
Senior design project by Jared Boggs, Matthew Buker, Christopher Nguyen, and Seth Graham that is built off of GNU Radio. The project utilizes an OSMOCOM - type SDR (we developed with HackRF One) and uses the device to scan for, detect, and record signals within a user-specified RF range.

The user can specify parameters such as frequency range, peak detection sensitivity, and signal scaling to modify how the program looks for and identifies a signal being present on a certain frequency. 

After a signal is detected, a user can choose to record raw data from the signal for a specified duration and store the data in a compressed format for analysis with another tool or model if desired.
