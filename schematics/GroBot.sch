EESchema Schematic File Version 2
LIBS:power
LIBS:device
LIBS:transistors
LIBS:conn
LIBS:linear
LIBS:regul
LIBS:74xx
LIBS:cmos4000
LIBS:adc-dac
LIBS:memory
LIBS:xilinx
LIBS:microcontrollers
LIBS:dsp
LIBS:microchip
LIBS:analog_switches
LIBS:motorola
LIBS:texas
LIBS:intel
LIBS:audio
LIBS:interface
LIBS:digital-audio
LIBS:philips
LIBS:display
LIBS:cypress
LIBS:siliconi
LIBS:opto
LIBS:atmel
LIBS:contrib
LIBS:valves
LIBS:psoc
LIBS:stm
LIBS:GroBot-cache
EELAYER 25 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title "GROBOT SENSOR SCHEMATIC"
Date "2016-10-30"
Rev "A"
Comp "PLANTAE"
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L D D?
U 1 1 58165221
P 6850 4950
F 0 "D?" H 6850 5050 50  0000 C CNN
F 1 "D" H 6850 4850 50  0000 C CNN
F 2 "" H 6850 4950 50  0000 C CNN
F 3 "" H 6850 4950 50  0000 C CNN
	1    6850 4950
	-1   0    0    -1  
$EndComp
$Comp
L R R?
U 1 1 58167583
P 4000 4850
F 0 "R?" V 4080 4850 50  0000 C CNN
F 1 "10k" V 4000 4850 50  0000 C CNN
F 2 "" V 3930 4850 50  0000 C CNN
F 3 "" H 4000 4850 50  0000 C CNN
	1    4000 4850
	0    1    1    0   
$EndComp
$Comp
L R R?
U 1 1 5816767A
P 4050 5250
F 0 "R?" V 4130 5250 50  0000 C CNN
F 1 "10k" V 4050 5250 50  0000 C CNN
F 2 "" V 3980 5250 50  0000 C CNN
F 3 "" H 4050 5250 50  0000 C CNN
	1    4050 5250
	0    1    1    0   
$EndComp
$Comp
L R R?
U 1 1 581676DF
P 4150 5650
F 0 "R?" V 4230 5650 50  0000 C CNN
F 1 "10k" V 4150 5650 50  0000 C CNN
F 2 "" V 4080 5650 50  0000 C CNN
F 3 "" H 4150 5650 50  0000 C CNN
	1    4150 5650
	0    1    1    0   
$EndComp
$Comp
L GND #PWR010
U 1 1 5816AC9D
P 5950 6550
F 0 "#PWR010" H 5950 6300 50  0001 C CNN
F 1 "GND" H 5950 6400 50  0000 C CNN
F 2 "" H 5950 6550 50  0000 C CNN
F 3 "" H 5950 6550 50  0000 C CNN
	1    5950 6550
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR013
U 1 1 5816C80F
P 3850 4650
F 0 "#PWR013" H 3850 4400 50  0001 C CNN
F 1 "GND" H 3850 4500 50  0000 C CNN
F 2 "" H 3850 4650 50  0000 C CNN
F 3 "" H 3850 4650 50  0000 C CNN
	1    3850 4650
	0    1    1    0   
$EndComp
Wire Wire Line
	6050 2050 6500 2050
Wire Wire Line
	5950 1850 7350 1850
Wire Wire Line
	5950 1850 5950 3150
Wire Wire Line
	5850 1650 8250 1650
Wire Wire Line
	5850 1650 5850 3150
Wire Wire Line
	6300 2650 6300 2350
Wire Wire Line
	7150 2450 7150 2150
Wire Wire Line
	7700 2250 7700 1950
Wire Wire Line
	6700 2350 6700 2950
Wire Wire Line
	7550 2150 7550 2950
Wire Wire Line
	8100 1950 8100 2950
Wire Wire Line
	7000 2950 7000 2850
Wire Wire Line
	7850 2950 7850 2850
Wire Wire Line
	8400 2950 8400 2850
Wire Wire Line
	5750 5750 6500 5750
Wire Wire Line
	6300 5150 6300 5450
Wire Wire Line
	6700 5450 6700 4850
Wire Wire Line
	7000 4850 7000 4950
Wire Wire Line
	5750 4650 5750 5750
Wire Wire Line
	5650 4650 5650 5950
Wire Wire Line
	7550 4850 7550 4950
Wire Wire Line
	4250 4650 4250 5100
Wire Wire Line
	4450 5900 4450 4650
Wire Wire Line
	4150 4850 4250 4850
Connection ~ 4250 4850
Wire Wire Line
	4200 5250 4350 5250
Connection ~ 4350 5250
Wire Wire Line
	4300 5650 4450 5650
Connection ~ 4450 5650
Wire Wire Line
	3700 4850 3850 4850
Wire Wire Line
	3750 5250 3900 5250
Wire Wire Line
	3850 5650 4000 5650
Wire Wire Line
	4450 2550 4450 3150
Wire Wire Line
	4550 2400 4550 3150
Wire Wire Line
	4650 3150 4650 2250
Wire Wire Line
	4750 2100 4750 3150
Wire Wire Line
	5550 2550 5550 3150
Wire Wire Line
	5700 2400 5700 2550
Wire Wire Line
	5700 2550 5650 2550
Wire Wire Line
	5650 2550 5650 3150
Wire Wire Line
	5450 2700 5450 3150
Wire Wire Line
	4950 5300 4950 4650
Wire Wire Line
	4850 1950 4850 3150
Wire Wire Line
	5950 5600 5950 5750
Connection ~ 5950 5750
Wire Wire Line
	5950 5150 5950 5300
Wire Wire Line
	5950 6100 5950 5950
Connection ~ 5950 5950
Wire Wire Line
	5950 6550 5950 6400
Wire Wire Line
	6200 2200 6200 2050
Connection ~ 6200 2050
Wire Wire Line
	6200 2500 6200 2600
Wire Wire Line
	6200 2600 6300 2600
Connection ~ 6300 2600
Wire Wire Line
	6900 2000 6900 1850
Connection ~ 6900 1850
Wire Wire Line
	6900 2400 6900 2300
Wire Wire Line
	8750 1650 8550 1650
Connection ~ 7900 1650
Wire Wire Line
	3850 4650 4150 4650
Wire Wire Line
	3250 3150 4150 3150
Wire Wire Line
	2650 1400 2900 1400
Wire Wire Line
	2150 1050 2150 1650
Connection ~ 2150 1400
Wire Wire Line
	2150 1950 2150 2200
Wire Wire Line
	1650 1050 1650 1650
Wire Wire Line
	1650 2200 1650 1950
Connection ~ 1650 1400
Wire Wire Line
	850  1400 1150 1400
Wire Wire Line
	750  7050 750  7250
Wire Wire Line
	850  7050 850  7500
Wire Wire Line
	850  7150 1000 7150
Wire Wire Line
	1300 7150 1450 7150
Connection ~ 850  7150
Wire Wire Line
	2150 7050 2150 7250
Wire Wire Line
	2250 7050 2250 7500
Wire Wire Line
	2250 7150 2400 7150
Wire Wire Line
	2700 7150 2850 7150
Connection ~ 2250 7150
Wire Wire Line
	10500 5250 10500 5400
Wire Wire Line
	10500 5400 10350 5400
Wire Wire Line
	10300 5600 10600 5600
Wire Wire Line
	10700 5250 10700 5750
Wire Wire Line
	10450 5700 10450 5600
Connection ~ 10450 5600
Wire Wire Line
	750  3300 750  3750
Wire Wire Line
	1250 3300 1800 3300
Connection ~ 1500 3300
Wire Wire Line
	8650 5600 8650 6250
Connection ~ 8650 5750
Wire Wire Line
	8650 5150 8650 5300
Wire Wire Line
	9250 5950 9250 5750
Wire Wire Line
	1000 5600 1000 5350
Wire Wire Line
	1250 5250 1000 5250
Wire Wire Line
	1000 5150 1250 5150
Wire Wire Line
	1250 5150 1250 5050
Wire Wire Line
	1000 5050 1000 4750
Wire Wire Line
	1500 3400 1500 3300
Wire Wire Line
	1500 3700 1500 3750
Wire Wire Line
	4350 2750 4350 3150
Wire Wire Line
	3100 2750 4350 2750
Wire Wire Line
	3550 2750 3550 2600
Wire Wire Line
	3550 2300 3550 2150
Connection ~ 3550 2750
Wire Wire Line
	3550 3300 3550 3150
Connection ~ 3550 3150
Wire Wire Line
	3550 3600 3550 3800
Wire Wire Line
	3250 2300 3250 2200
Wire Wire Line
	3250 2200 3850 2200
Connection ~ 3550 2200
Wire Wire Line
	3250 2600 3250 2750
Connection ~ 3250 2750
Wire Wire Line
	2700 2750 2800 2750
Wire Wire Line
	3850 2600 3850 2750
Connection ~ 3850 2750
Wire Wire Line
	3850 2200 3850 2300
Wire Wire Line
	4950 1950 4950 3150
$Comp
L CY8CKIT-049 U?
U 1 1 581E1512
P 5300 3900
F 0 "U?" H 5300 3800 60  0000 C CNN
F 1 "CY8CKIT-049" H 5300 4000 60  0000 C CNN
F 2 "" H 5700 2750 60  0000 C CNN
F 3 "" H 5700 2750 60  0000 C CNN
	1    5300 3900
	0    -1   -1   0   
$EndComp
NoConn ~ 6250 3150
NoConn ~ 6150 3150
$Comp
L Q_NMOS_DGS Q?
U 1 1 581E1513
P 7900 1850
F 0 "Q?" H 8200 1900 50  0000 R CNN
F 1 "Q_NMOS_DGS" H 8550 1800 50  0000 R CNN
F 2 "" H 8100 1950 50  0000 C CNN
F 3 "" H 7900 1850 50  0000 C CNN
	1    7900 1850
	0    1    1    0   
$EndComp
$Comp
L GND #PWR034
U 1 1 581E1516
P 6300 2650
F 0 "#PWR034" H 6300 2400 50  0001 C CNN
F 1 "GND" H 6300 2500 50  0000 C CNN
F 2 "" H 6300 2650 50  0000 C CNN
F 3 "" H 6300 2650 50  0000 C CNN
	1    6300 2650
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR035
U 1 1 581E1517
P 7150 2450
F 0 "#PWR035" H 7150 2200 50  0001 C CNN
F 1 "GND" H 7150 2300 50  0000 C CNN
F 2 "" H 7150 2450 50  0000 C CNN
F 3 "" H 7150 2450 50  0000 C CNN
	1    7150 2450
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR036
U 1 1 581E1518
P 7700 2250
F 0 "#PWR036" H 7700 2000 50  0001 C CNN
F 1 "GND" H 7700 2100 50  0000 C CNN
F 2 "" H 7700 2250 50  0000 C CNN
F 3 "" H 7700 2250 50  0000 C CNN
	1    7700 2250
	1    0    0    -1  
$EndComp
Text Label 8100 2950 3    60   ~ 0
PH_GND
$Comp
L D D?
U 1 1 581E1519
P 6850 2850
F 0 "D?" H 6850 2950 50  0000 C CNN
F 1 "D" H 6850 2750 50  0000 C CNN
F 2 "" H 6850 2850 50  0000 C CNN
F 3 "" H 6850 2850 50  0000 C CNN
	1    6850 2850
	-1   0    0    1   
$EndComp
$Comp
L D D?
U 1 1 581E151A
P 7700 2850
F 0 "D?" H 7700 2950 50  0000 C CNN
F 1 "D" H 7700 2750 50  0000 C CNN
F 2 "" H 7700 2850 50  0000 C CNN
F 3 "" H 7700 2850 50  0000 C CNN
	1    7700 2850
	-1   0    0    1   
$EndComp
$Comp
L D D?
U 1 1 581E151B
P 8250 2850
F 0 "D?" H 8250 2950 50  0000 C CNN
F 1 "D" H 8250 2750 50  0000 C CNN
F 2 "" H 8250 2850 50  0000 C CNN
F 3 "" H 8250 2850 50  0000 C CNN
	1    8250 2850
	-1   0    0    1   
$EndComp
Text Label 7000 2950 3    60   ~ 0
PUMP_12V
Text Label 7850 2950 3    60   ~ 0
NUTR_12V
$Comp
L Q_NMOS_DGS Q?
U 1 1 581E151C
P 6500 5550
F 0 "Q?" H 6800 5600 50  0000 R CNN
F 1 "Q_NMOS_DGS" H 7150 5500 50  0000 R CNN
F 2 "" H 6700 5650 50  0000 C CNN
F 3 "" H 6500 5550 50  0000 C CNN
	1    6500 5550
	0    1    -1   0   
$EndComp
$Comp
L GND #PWR037
U 1 1 581E151D
P 6300 5150
F 0 "#PWR037" H 6300 4900 50  0001 C CNN
F 1 "GND" H 6300 5000 50  0000 C CNN
F 2 "" H 6300 5150 50  0000 C CNN
F 3 "" H 6300 5150 50  0000 C CNN
	1    6300 5150
	1    0    0    1   
$EndComp
Text Label 6700 4850 1    60   ~ 0
LED_GND
$Comp
L D D?
U 1 1 581E151F
P 6850 4950
F 0 "D?" H 6850 5050 50  0000 C CNN
F 1 "D" H 6850 4850 50  0000 C CNN
F 2 "" H 6850 4950 50  0000 C CNN
F 3 "" H 6850 4950 50  0000 C CNN
	1    6850 4950
	-1   0    0    -1  
$EndComp
Text Label 7000 4850 1    60   ~ 0
LED_24V
Text Label 7550 4850 1    60   ~ 0
FAN_24V
$Comp
L D D?
U 1 1 581E1520
P 7400 4950
F 0 "D?" H 7400 5050 50  0000 C CNN
F 1 "D" H 7400 4850 50  0000 C CNN
F 2 "" H 7400 4950 50  0000 C CNN
F 3 "" H 7400 4950 50  0000 C CNN
	1    7400 4950
	-1   0    0    -1  
$EndComp
Text Label 7250 4850 1    60   ~ 0
FAN_GND
Text Label 4250 5100 2    60   ~ 0
LED_WHT_PWM
Text Label 4350 5500 2    60   ~ 0
LED_RED_PWM
Text Label 4450 5900 2    60   ~ 0
LED_BLUE_PWM
$Comp
L R R?
U 1 1 581E1522
P 4000 4850
F 0 "R?" V 4080 4850 50  0000 C CNN
F 1 "10k" V 4000 4850 50  0000 C CNN
F 2 "" V 3930 4850 50  0000 C CNN
F 3 "" H 4000 4850 50  0000 C CNN
	1    4000 4850
	0    1    1    0   
$EndComp
$Comp
L R R?
U 1 1 581E1523
P 4050 5250
F 0 "R?" V 4130 5250 50  0000 C CNN
F 1 "10k" V 4050 5250 50  0000 C CNN
F 2 "" V 3980 5250 50  0000 C CNN
F 3 "" H 4050 5250 50  0000 C CNN
	1    4050 5250
	0    1    1    0   
$EndComp
$Comp
L R R?
U 1 1 581E1524
P 4150 5650
F 0 "R?" V 4230 5650 50  0000 C CNN
F 1 "10k" V 4150 5650 50  0000 C CNN
F 2 "" V 4080 5650 50  0000 C CNN
F 3 "" H 4150 5650 50  0000 C CNN
	1    4150 5650
	0    1    1    0   
$EndComp
Text Label 4450 2550 2    60   ~ 0
PH_OUT
Text Label 4550 2400 2    60   ~ 0
EC_OUT
Text Label 4650 2250 2    60   ~ 0
DHT_DATA
Text Label 4750 2100 2    60   ~ 0
WTEMP_OUT
Text Label 5550 2550 2    60   ~ 0
LED_TEMP1
Text Label 5700 2400 2    60   ~ 0
LED_TEMP2
Text Label 5450 2700 2    60   ~ 0
PR_OUT
Text Label 4850 5150 2    60   ~ 0
SBC_TX
Text Label 4950 5300 2    60   ~ 0
SBC_RX
Text Label 4850 1950 2    60   ~ 0
DS_OUT
$Comp
L R R?
U 1 1 581E1528
P 5950 5450
F 0 "R?" V 6030 5450 50  0000 C CNN
F 1 "10k" V 5950 5450 50  0000 C CNN
F 2 "" V 5880 5450 50  0000 C CNN
F 3 "" H 5950 5450 50  0000 C CNN
	1    5950 5450
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR042
U 1 1 581E1529
P 5950 5150
F 0 "#PWR042" H 5950 4900 50  0001 C CNN
F 1 "GND" H 5950 5000 50  0000 C CNN
F 2 "" H 5950 5150 50  0000 C CNN
F 3 "" H 5950 5150 50  0000 C CNN
	1    5950 5150
	-1   0    0    1   
$EndComp
$Comp
L R R?
U 1 1 581E152A
P 5950 6250
F 0 "R?" V 6030 6250 50  0000 C CNN
F 1 "10k" V 5950 6250 50  0000 C CNN
F 2 "" V 5880 6250 50  0000 C CNN
F 3 "" H 5950 6250 50  0000 C CNN
	1    5950 6250
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR043
U 1 1 581E152B
P 5950 6550
F 0 "#PWR043" H 5950 6300 50  0001 C CNN
F 1 "GND" H 5950 6400 50  0000 C CNN
F 2 "" H 5950 6550 50  0000 C CNN
F 3 "" H 5950 6550 50  0000 C CNN
	1    5950 6550
	1    0    0    -1  
$EndComp
$Comp
L R R?
U 1 1 581E152C
P 6200 2350
F 0 "R?" V 6280 2350 50  0000 C CNN
F 1 "10k" V 6200 2350 50  0000 C CNN
F 2 "" V 6130 2350 50  0000 C CNN
F 3 "" H 6200 2350 50  0000 C CNN
	1    6200 2350
	-1   0    0    1   
$EndComp
Text Label 6700 2950 3    60   ~ 0
PUMP_GND
$Comp
L R R?
U 1 1 581E152D
P 6900 2150
F 0 "R?" V 6980 2150 50  0000 C CNN
F 1 "10k" V 6900 2150 50  0000 C CNN
F 2 "" V 6830 2150 50  0000 C CNN
F 3 "" H 6900 2150 50  0000 C CNN
	1    6900 2150
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR044
U 1 1 581E152E
P 6900 2400
F 0 "#PWR044" H 6900 2150 50  0001 C CNN
F 1 "GND" H 6900 2250 50  0000 C CNN
F 2 "" H 6900 2400 50  0000 C CNN
F 3 "" H 6900 2400 50  0000 C CNN
	1    6900 2400
	1    0    0    -1  
$EndComp
$Comp
L R R?
U 1 1 581E152F
P 8400 1650
F 0 "R?" V 8480 1650 50  0000 C CNN
F 1 "10k" V 8400 1650 50  0000 C CNN
F 2 "" V 8330 1650 50  0000 C CNN
F 3 "" H 8400 1650 50  0000 C CNN
	1    8400 1650
	0    1    1    0   
$EndComp
$Comp
L GND #PWR045
U 1 1 581E1530
P 8750 1650
F 0 "#PWR045" H 8750 1400 50  0001 C CNN
F 1 "GND" H 8750 1500 50  0000 C CNN
F 2 "" H 8750 1650 50  0000 C CNN
F 3 "" H 8750 1650 50  0000 C CNN
	1    8750 1650
	0    -1   -1   0   
$EndComp
NoConn ~ 4250 3150
NoConn ~ 5050 3150
NoConn ~ 5150 3150
NoConn ~ 5250 3150
NoConn ~ 5750 3150
$Comp
L GND #PWR046
U 1 1 581E1531
P 3850 4650
F 0 "#PWR046" H 3850 4400 50  0001 C CNN
F 1 "GND" H 3850 4500 50  0000 C CNN
F 2 "" H 3850 4650 50  0000 C CNN
F 3 "" H 3850 4650 50  0000 C CNN
	1    3850 4650
	0    1    1    0   
$EndComp
NoConn ~ 6250 4650
NoConn ~ 6150 4650
NoConn ~ 6050 4650
NoConn ~ 5950 4650
NoConn ~ 5850 4650
NoConn ~ 5550 4650
NoConn ~ 4750 4650
NoConn ~ 4650 4650
NoConn ~ 4550 4650
$Comp
L THERMISTOR TH?
U 1 1 581E1533
P 1400 1400
F 0 "TH?" V 1500 1450 50  0000 C CNN
F 1 "THERMISTOR" V 1300 1400 50  0000 C BNN
F 2 "" H 1400 1400 50  0000 C CNN
F 3 "" H 1400 1400 50  0000 C CNN
	1    1400 1400
	0    1    1    0   
$EndComp
$Comp
L R R?
U 1 1 581E1536
P 1650 1800
F 0 "R?" V 1730 1800 50  0000 C CNN
F 1 "12k" V 1650 1800 50  0000 C CNN
F 2 "" V 1580 1800 50  0000 C CNN
F 3 "" H 1650 1800 50  0000 C CNN
	1    1650 1800
	1    0    0    -1  
$EndComp
Text Label 2150 1050 0    60   ~ 0
LED_TEMP2
Text Label 1650 1050 2    60   ~ 0
LED_TEMP1
$Comp
L CONN_01X02 P?
U 1 1 581E1537
P 800 6850
F 0 "P?" H 800 7000 50  0000 C CNN
F 1 "EC PROBE" V 900 6850 50  0000 C CNN
F 2 "" H 800 6850 50  0000 C CNN
F 3 "" H 800 6850 50  0000 C CNN
	1    800  6850
	0    -1   -1   0   
$EndComp
$Comp
L R R?
U 1 1 581E1539
P 1150 7150
F 0 "R?" V 1230 7150 50  0000 C CNN
F 1 "2.2k" V 1150 7150 50  0000 C CNN
F 2 "" V 1080 7150 50  0000 C CNN
F 3 "" H 1150 7150 50  0000 C CNN
	1    1150 7150
	0    1    1    0   
$EndComp
$Comp
L CONN_01X02 P?
U 1 1 581E153A
P 2200 6850
F 0 "P?" H 2200 7000 50  0000 C CNN
F 1 "WATER TEMP PROBE" V 2300 6850 50  0000 C CNN
F 2 "" H 2200 6850 50  0000 C CNN
F 3 "" H 2200 6850 50  0000 C CNN
	1    2200 6850
	0    -1   -1   0   
$EndComp
$Comp
L R R?
U 1 1 581E153C
P 2550 7150
F 0 "R?" V 2630 7150 50  0000 C CNN
F 1 "30k" V 2550 7150 50  0000 C CNN
F 2 "" V 2480 7150 50  0000 C CNN
F 3 "" H 2550 7150 50  0000 C CNN
	1    2550 7150
	0    1    1    0   
$EndComp
$Comp
L +5V #PWR050
U 1 1 581E153D
P 2850 7150
F 0 "#PWR050" H 2850 7000 50  0001 C CNN
F 1 "+5V" H 2850 7290 50  0000 C CNN
F 2 "" H 2850 7150 50  0000 C CNN
F 3 "" H 2850 7150 50  0000 C CNN
	1    2850 7150
	0    1    1    0   
$EndComp
$Comp
L Photores R?
U 1 1 581E1543
P 1000 3300
F 0 "R?" V 1080 3300 50  0000 C CNN
F 1 "Photores" V 1210 3300 50  0000 C TNN
F 2 "" V 930 3300 50  0000 C CNN
F 3 "" H 1000 3300 50  0000 C CNN
	1    1000 3300
	0    1    1    0   
$EndComp
$Comp
L GND #PWR054
U 1 1 581E1544
P 750 3750
F 0 "#PWR054" H 750 3500 50  0001 C CNN
F 1 "GND" H 750 3600 50  0000 C CNN
F 2 "" H 750 3750 50  0000 C CNN
F 3 "" H 750 3750 50  0000 C CNN
	1    750  3750
	1    0    0    -1  
$EndComp
Text Label 1800 3300 0    60   ~ 0
PR_OUT
$Comp
L +5V #PWR055
U 1 1 581E1545
P 1500 3750
F 0 "#PWR055" H 1500 3600 50  0001 C CNN
F 1 "+5V" H 1500 3890 50  0000 C CNN
F 2 "" H 1500 3750 50  0000 C CNN
F 3 "" H 1500 3750 50  0000 C CNN
	1    1500 3750
	-1   0    0    1   
$EndComp
Text Label 8650 6250 2    60   ~ 0
DS_OUT
$Comp
L SW_PUSH SW?
U 1 1 581E1546
P 8950 5750
F 0 "SW?" H 9100 5860 50  0000 C CNN
F 1 "SW_PUSH" H 8950 5670 50  0000 C CNN
F 2 "" H 8950 5750 50  0000 C CNN
F 3 "" H 8950 5750 50  0000 C CNN
	1    8950 5750
	1    0    0    -1  
$EndComp
$Comp
L R R?
U 1 1 581E1547
P 8650 5450
F 0 "R?" V 8730 5450 50  0000 C CNN
F 1 "10k" V 8650 5450 50  0000 C CNN
F 2 "" V 8580 5450 50  0000 C CNN
F 3 "" H 8650 5450 50  0000 C CNN
	1    8650 5450
	1    0    0    -1  
$EndComp
$Comp
L +5V #PWR056
U 1 1 581E1548
P 8650 5150
F 0 "#PWR056" H 8650 5000 50  0001 C CNN
F 1 "+5V" H 8650 5290 50  0000 C CNN
F 2 "" H 8650 5150 50  0000 C CNN
F 3 "" H 8650 5150 50  0000 C CNN
	1    8650 5150
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR057
U 1 1 581E1549
P 9250 5950
F 0 "#PWR057" H 9250 5700 50  0001 C CNN
F 1 "GND" H 9250 5800 50  0000 C CNN
F 2 "" H 9250 5950 50  0000 C CNN
F 3 "" H 9250 5950 50  0000 C CNN
	1    9250 5950
	1    0    0    -1  
$EndComp
Text Notes 4000 1450 0    178  ~ 0
BASE CONTROLLER
Text Notes 550  6500 0    99   ~ 0
WATER TEMP & CONDUCTIVITY
Text Notes 1550 800  0    99   ~ 0
LED TEMP\n
Text Notes 850  2850 0    99   ~ 0
LIGHT OUTPUT
Text Notes 8400 4800 0    99   ~ 0
DOOR CLOSED\nDETECT
Text Notes 10100 4800 0    99   ~ 0
AIR TEMP &\nHUMIDITY
$Comp
L CONN_01X04 P?
U 1 1 581E154A
P 800 5200
F 0 "P?" H 800 5450 50  0000 C CNN
F 1 "CONN_01X04" V 900 5200 50  0000 C CNN
F 2 "" H 800 5200 50  0000 C CNN
F 3 "" H 800 5200 50  0000 C CNN
	1    800  5200
	-1   0    0    1   
$EndComp
$Comp
L GND #PWR058
U 1 1 581E154B
P 1000 5600
F 0 "#PWR058" H 1000 5350 50  0001 C CNN
F 1 "GND" H 1000 5450 50  0000 C CNN
F 2 "" H 1000 5600 50  0000 C CNN
F 3 "" H 1000 5600 50  0000 C CNN
	1    1000 5600
	1    0    0    -1  
$EndComp
Text Label 1250 5250 0    99   ~ 0
LCD_TX
Text Label 1250 5050 0    99   ~ 0
LCD_RX
$Comp
L +5V #PWR059
U 1 1 581E154C
P 1000 4750
F 0 "#PWR059" H 1000 4600 50  0001 C CNN
F 1 "+5V" H 1000 4890 50  0000 C CNN
F 2 "" H 1000 4750 50  0000 C CNN
F 3 "" H 1000 4750 50  0000 C CNN
	1    1000 4750
	1    0    0    -1  
$EndComp
Text Notes 850  4500 0    99   ~ 0
LCD DISPLAY
$Comp
L R R?
U 1 1 581E154D
P 1500 3550
F 0 "R?" V 1580 3550 50  0000 C CNN
F 1 "100k" V 1500 3550 50  0000 C CNN
F 2 "" V 1430 3550 50  0000 C CNN
F 3 "" H 1500 3550 50  0000 C CNN
	1    1500 3550
	1    0    0    -1  
$EndComp
$Comp
L C C?
U 1 1 581E154E
P 3550 2450
F 0 "C?" H 3575 2550 50  0000 L CNN
F 1 "10uF" H 3575 2350 50  0000 L CNN
F 2 "" H 3588 2300 50  0000 C CNN
F 3 "" H 3550 2450 50  0000 C CNN
	1    3550 2450
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR060
U 1 1 581E154F
P 3550 2150
F 0 "#PWR060" H 3550 1900 50  0001 C CNN
F 1 "GND" H 3550 2000 50  0000 C CNN
F 2 "" H 3550 2150 50  0000 C CNN
F 3 "" H 3550 2150 50  0000 C CNN
	1    3550 2150
	-1   0    0    1   
$EndComp
$Comp
L GND #PWR061
U 1 1 581E1551
P 3550 3800
F 0 "#PWR061" H 3550 3550 50  0001 C CNN
F 1 "GND" H 3550 3650 50  0000 C CNN
F 2 "" H 3550 3800 50  0000 C CNN
F 3 "" H 3550 3800 50  0000 C CNN
	1    3550 3800
	1    0    0    -1  
$EndComp
$Comp
L +5V #PWR064
U 1 1 581E1556
P 1650 2200
F 0 "#PWR064" H 1650 2050 50  0001 C CNN
F 1 "+5V" H 1650 2340 50  0000 C CNN
F 2 "" H 1650 2200 50  0000 C CNN
F 3 "" H 1650 2200 50  0000 C CNN
	1    1650 2200
	-1   0    0    1   
$EndComp
$Comp
L GND #PWR065
U 1 1 581E1557
P 2900 1400
F 0 "#PWR065" H 2900 1150 50  0001 C CNN
F 1 "GND" H 2900 1250 50  0000 C CNN
F 2 "" H 2900 1400 50  0000 C CNN
F 3 "" H 2900 1400 50  0000 C CNN
	1    2900 1400
	0    -1   -1   0   
$EndComp
$Comp
L GND #PWR066
U 1 1 581E1558
P 850 1400
F 0 "#PWR066" H 850 1150 50  0001 C CNN
F 1 "GND" H 850 1250 50  0000 C CNN
F 2 "" H 850 1400 50  0000 C CNN
F 3 "" H 850 1400 50  0000 C CNN
	1    850  1400
	0    1    1    0   
$EndComp
Text Label 4950 1950 0    60   ~ 0
EC_POWER
Wire Wire Line
	5250 4650 5250 5800
$Comp
L GND #PWR?
U 1 1 582F21FB
P 3700 4850
F 0 "#PWR?" H 3700 4600 50  0001 C CNN
F 1 "GND" H 3700 4700 50  0000 C CNN
F 2 "" H 3700 4850 50  0000 C CNN
F 3 "" H 3700 4850 50  0000 C CNN
	1    3700 4850
	0    1    1    0   
$EndComp
$Comp
L GND #PWR?
U 1 1 582F22AB
P 3750 5250
F 0 "#PWR?" H 3750 5000 50  0001 C CNN
F 1 "GND" H 3750 5100 50  0000 C CNN
F 2 "" H 3750 5250 50  0000 C CNN
F 3 "" H 3750 5250 50  0000 C CNN
	1    3750 5250
	0    1    1    0   
$EndComp
$Comp
L GND #PWR?
U 1 1 582F235B
P 3850 5650
F 0 "#PWR?" H 3850 5400 50  0001 C CNN
F 1 "GND" H 3850 5500 50  0000 C CNN
F 2 "" H 3850 5650 50  0000 C CNN
F 3 "" H 3850 5650 50  0000 C CNN
	1    3850 5650
	0    1    1    0   
$EndComp
Wire Wire Line
	5150 4650 5150 5650
Text Label 5150 5650 2    60   ~ 0
LCD_TX
Text Label 5250 5800 2    60   ~ 0
LCD_RX
NoConn ~ 5350 4650
NoConn ~ 5450 4650
Wire Wire Line
	5050 4650 5050 5450
Text Label 5050 5450 2    60   ~ 0
I2C_SCL
Wire Wire Line
	5350 2850 5350 3150
Wire Wire Line
	7250 5650 7250 4850
Connection ~ 7250 4950
Connection ~ 6700 4950
$Comp
L GND #PWR038
U 1 1 581E151E
P 6850 5350
F 0 "#PWR038" H 6850 5100 50  0001 C CNN
F 1 "GND" H 6850 5200 50  0000 C CNN
F 2 "" H 6850 5350 50  0000 C CNN
F 3 "" H 6850 5350 50  0000 C CNN
	1    6850 5350
	1    0    0    1   
$EndComp
Wire Wire Line
	6850 5350 6850 5650
$Comp
L Q_NMOS_DGS Q?
U 1 1 581E1521
P 7050 5750
F 0 "Q?" H 7350 5800 50  0000 R CNN
F 1 "Q_NMOS_DGS" H 7700 5700 50  0000 R CNN
F 2 "" H 7250 5850 50  0000 C CNN
F 3 "" H 7050 5750 50  0000 C CNN
	1    7050 5750
	0    1    -1   0   
$EndComp
Wire Wire Line
	5650 5950 7050 5950
Wire Wire Line
	10600 5600 10600 5250
$Comp
L R R?
U 1 1 581E1553
P 2950 2750
F 0 "R?" V 3030 2750 50  0000 C CNN
F 1 "10k" V 2950 2750 50  0000 C CNN
F 2 "" V 2880 2750 50  0000 C CNN
F 3 "" H 2950 2750 50  0000 C CNN
	1    2950 2750
	0    1    1    0   
$EndComp
$Comp
L R R?
U 1 1 581E1535
P 2150 1800
F 0 "R?" V 2230 1800 50  0000 C CNN
F 1 "12k" V 2150 1800 50  0000 C CNN
F 2 "" V 2080 1800 50  0000 C CNN
F 3 "" H 2150 1800 50  0000 C CNN
	1    2150 1800
	1    0    0    -1  
$EndComp
Text Label 8400 2950 3    60   ~ 0
PH_12V
$Comp
L Q_NMOS_DGS Q?
U 1 1 581E1514
P 7350 2050
F 0 "Q?" H 7650 2100 50  0000 R CNN
F 1 "Q_NMOS_DGS" H 8000 2000 50  0000 R CNN
F 2 "" H 7550 2150 50  0000 C CNN
F 3 "" H 7350 2050 50  0000 C CNN
	1    7350 2050
	0    1    1    0   
$EndComp
$Comp
L Q_NMOS_DGS Q?
U 1 1 581E1515
P 6500 2250
F 0 "Q?" H 6800 2300 50  0000 R CNN
F 1 "Q_NMOS_DGS" H 7150 2200 50  0000 R CNN
F 2 "" H 6700 2350 50  0000 C CNN
F 3 "" H 6500 2250 50  0000 C CNN
	1    6500 2250
	0    1    1    0   
$EndComp
Wire Wire Line
	6050 2050 6050 3150
Text Label 5350 2850 2    60   ~ 0
I2C_SDA
$Comp
L C C?
U 1 1 581E1559
P 3850 2450
F 0 "C?" H 3875 2550 50  0000 L CNN
F 1 "0.1uF" H 3875 2350 50  0000 L CNN
F 2 "" H 3888 2300 50  0000 C CNN
F 3 "" H 3850 2450 50  0000 C CNN
	1    3850 2450
	1    0    0    -1  
$EndComp
$Comp
L R R?
U 1 1 581E1552
P 3250 2450
F 0 "R?" V 3330 2450 50  0000 C CNN
F 1 "10k" V 3250 2450 50  0000 C CNN
F 2 "" V 3180 2450 50  0000 C CNN
F 3 "" H 3250 2450 50  0000 C CNN
	1    3250 2450
	1    0    0    -1  
$EndComp
$Comp
L +5V #PWR062
U 1 1 581E1554
P 2700 2750
F 0 "#PWR062" H 2700 2600 50  0001 C CNN
F 1 "+5V" H 2700 2890 50  0000 C CNN
F 2 "" H 2700 2750 50  0000 C CNN
F 3 "" H 2700 2750 50  0000 C CNN
	1    2700 2750
	0    -1   -1   0   
$EndComp
$Comp
L +5V #PWR047
U 1 1 581E1532
P 3250 3150
F 0 "#PWR047" H 3250 3000 50  0001 C CNN
F 1 "+5V" H 3250 3290 50  0000 C CNN
F 2 "" H 3250 3150 50  0000 C CNN
F 3 "" H 3250 3150 50  0000 C CNN
	1    3250 3150
	0    -1   -1   0   
$EndComp
$Comp
L C C?
U 1 1 581E1550
P 3550 3450
F 0 "C?" H 3575 3550 50  0000 L CNN
F 1 "0.1uF" H 3575 3350 50  0000 L CNN
F 2 "" H 3588 3300 50  0000 C CNN
F 3 "" H 3550 3450 50  0000 C CNN
	1    3550 3450
	1    0    0    -1  
$EndComp
Text Label 7550 2950 3    60   ~ 0
NUTR_GND
$Comp
L THERMISTOR TH?
U 1 1 581E1534
P 2400 1400
F 0 "TH?" V 2500 1450 50  0000 C CNN
F 1 "THERMISTOR" V 2300 1400 50  0000 C BNN
F 2 "" H 2400 1400 50  0000 C CNN
F 3 "" H 2400 1400 50  0000 C CNN
	1    2400 1400
	0    1    1    0   
$EndComp
$Comp
L +5V #PWR063
U 1 1 581E1555
P 2150 2200
F 0 "#PWR063" H 2150 2050 50  0001 C CNN
F 1 "+5V" H 2150 2340 50  0000 C CNN
F 2 "" H 2150 2200 50  0000 C CNN
F 3 "" H 2150 2200 50  0000 C CNN
	1    2150 2200
	-1   0    0    1   
$EndComp
Text Label 2250 7500 0    60   ~ 0
WTEMP_OUT
$Comp
L GND #PWR049
U 1 1 581E153B
P 2150 7250
F 0 "#PWR049" H 2150 7000 50  0001 C CNN
F 1 "GND" H 2150 7100 50  0000 C CNN
F 2 "" H 2150 7250 50  0000 C CNN
F 3 "" H 2150 7250 50  0000 C CNN
	1    2150 7250
	1    0    0    -1  
$EndComp
Text Label 1450 7150 0    60   ~ 0
EC_POWER
Text Label 850  7500 0    60   ~ 0
EC_OUT
$Comp
L GND #PWR048
U 1 1 581E1538
P 750 7250
F 0 "#PWR048" H 750 7000 50  0001 C CNN
F 1 "GND" H 750 7100 50  0000 C CNN
F 2 "" H 750 7250 50  0000 C CNN
F 3 "" H 750 7250 50  0000 C CNN
	1    750  7250
	1    0    0    -1  
$EndComp
Text Label 10300 5600 2    60   ~ 0
DHT_DATA
$Comp
L +5V #PWR051
U 1 1 581E153F
P 10350 5400
F 0 "#PWR051" H 10350 5250 50  0001 C CNN
F 1 "+5V" H 10350 5540 50  0000 C CNN
F 2 "" H 10350 5400 50  0000 C CNN
F 3 "" H 10350 5400 50  0000 C CNN
	1    10350 5400
	0    -1   -1   0   
$EndComp
$Comp
L CONN_01X03 P?
U 1 1 581E153E
P 10600 5050
F 0 "P?" H 10600 5250 50  0000 C CNN
F 1 "DHT11 MODULE" V 10700 5050 50  0000 C CNN
F 2 "" H 10600 5050 50  0000 C CNN
F 3 "" H 10600 5050 50  0000 C CNN
	1    10600 5050
	0    -1   -1   0   
$EndComp
$Comp
L GND #PWR052
U 1 1 581E1540
P 10700 5750
F 0 "#PWR052" H 10700 5500 50  0001 C CNN
F 1 "GND" H 10700 5600 50  0000 C CNN
F 2 "" H 10700 5750 50  0000 C CNN
F 3 "" H 10700 5750 50  0000 C CNN
	1    10700 5750
	1    0    0    -1  
$EndComp
NoConn ~ 5850 4650
$Comp
L R R?
U 1 1 581E1541
P 10450 5850
F 0 "R?" V 10530 5850 50  0000 C CNN
F 1 "5k" V 10450 5850 50  0000 C CNN
F 2 "" V 10380 5850 50  0000 C CNN
F 3 "" H 10450 5850 50  0000 C CNN
	1    10450 5850
	1    0    0    -1  
$EndComp
$Comp
L +5V #PWR053
U 1 1 581E1542
P 10450 6150
F 0 "#PWR053" H 10450 6000 50  0001 C CNN
F 1 "+5V" H 10450 6290 50  0000 C CNN
F 2 "" H 10450 6150 50  0000 C CNN
F 3 "" H 10450 6150 50  0000 C CNN
	1    10450 6150
	-1   0    0    1   
$EndComp
Wire Wire Line
	10450 6000 10450 6150
Wire Wire Line
	4850 4650 4850 5150
Wire Wire Line
	4350 5500 4350 4650
Connection ~ 6700 2850
Connection ~ 7550 2850
Connection ~ 8100 2850
$Comp
L STM32F091CBU6 U?
U 1 1 58EAEB8D
P 9850 3100
F 0 "U?" H 9950 2700 60  0000 C CNN
F 1 "STM32F091CBU6" H 9950 3000 60  0000 C CNN
F 2 "" H 9950 2700 60  0000 C CNN
F 3 "" H 9950 2700 60  0000 C CNN
	1    9850 3100
	1    0    0    -1  
$EndComp
Text Notes 3300 1900 0    60   ~ 0
ANALOG REF
$EndSCHEMATC