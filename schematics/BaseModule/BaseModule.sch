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
LIBS:can
LIBS:power_reg
LIBS:psoc
LIBS:stm
LIBS:BaseModule-cache
EELAYER 25 0
EELAYER END
$Descr B 17000 11000
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
L Q_NMOS_DGS Q?
U 1 1 581E1513
P 14600 1750
F 0 "Q?" H 14900 1800 50  0000 R CNN
F 1 "Q_NMOS_DGS" H 15250 1700 50  0000 R CNN
F 2 "" H 14800 1850 50  0000 C CNN
F 3 "" H 14600 1750 50  0000 C CNN
	1    14600 1750
	0    1    1    0   
$EndComp
$Comp
L GND #PWR034
U 1 1 581E1516
P 13000 2550
F 0 "#PWR034" H 13000 2300 50  0001 C CNN
F 1 "GND" H 13000 2400 50  0000 C CNN
F 2 "" H 13000 2550 50  0000 C CNN
F 3 "" H 13000 2550 50  0000 C CNN
	1    13000 2550
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR035
U 1 1 581E1517
P 13850 2350
F 0 "#PWR035" H 13850 2100 50  0001 C CNN
F 1 "GND" H 13850 2200 50  0000 C CNN
F 2 "" H 13850 2350 50  0000 C CNN
F 3 "" H 13850 2350 50  0000 C CNN
	1    13850 2350
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR036
U 1 1 581E1518
P 14400 2150
F 0 "#PWR036" H 14400 1900 50  0001 C CNN
F 1 "GND" H 14400 2000 50  0000 C CNN
F 2 "" H 14400 2150 50  0000 C CNN
F 3 "" H 14400 2150 50  0000 C CNN
	1    14400 2150
	1    0    0    -1  
$EndComp
Text Label 14800 2850 3    60   ~ 0
PH_GND
$Comp
L D D?
U 1 1 581E1519
P 13550 2750
F 0 "D?" H 13550 2850 50  0000 C CNN
F 1 "D" H 13550 2650 50  0000 C CNN
F 2 "" H 13550 2750 50  0000 C CNN
F 3 "" H 13550 2750 50  0000 C CNN
	1    13550 2750
	-1   0    0    1   
$EndComp
$Comp
L D D?
U 1 1 581E151A
P 14400 2750
F 0 "D?" H 14400 2850 50  0000 C CNN
F 1 "D" H 14400 2650 50  0000 C CNN
F 2 "" H 14400 2750 50  0000 C CNN
F 3 "" H 14400 2750 50  0000 C CNN
	1    14400 2750
	-1   0    0    1   
$EndComp
$Comp
L D D?
U 1 1 581E151B
P 14950 2750
F 0 "D?" H 14950 2850 50  0000 C CNN
F 1 "D" H 14950 2650 50  0000 C CNN
F 2 "" H 14950 2750 50  0000 C CNN
F 3 "" H 14950 2750 50  0000 C CNN
	1    14950 2750
	-1   0    0    1   
$EndComp
Text Label 13700 2850 3    60   ~ 0
PUMP_12V
Text Label 14550 2850 3    60   ~ 0
NUTR_12V
$Comp
L R R?
U 1 1 581E152C
P 12900 2250
F 0 "R?" V 12980 2250 50  0000 C CNN
F 1 "10k" V 12900 2250 50  0000 C CNN
F 2 "" V 12830 2250 50  0000 C CNN
F 3 "" H 12900 2250 50  0000 C CNN
	1    12900 2250
	-1   0    0    1   
$EndComp
Text Label 13400 2850 3    60   ~ 0
PUMP_GND
$Comp
L R R?
U 1 1 581E152D
P 13600 2050
F 0 "R?" V 13680 2050 50  0000 C CNN
F 1 "10k" V 13600 2050 50  0000 C CNN
F 2 "" V 13530 2050 50  0000 C CNN
F 3 "" H 13600 2050 50  0000 C CNN
	1    13600 2050
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR044
U 1 1 581E152E
P 13600 2300
F 0 "#PWR044" H 13600 2050 50  0001 C CNN
F 1 "GND" H 13600 2150 50  0000 C CNN
F 2 "" H 13600 2300 50  0000 C CNN
F 3 "" H 13600 2300 50  0000 C CNN
	1    13600 2300
	1    0    0    -1  
$EndComp
$Comp
L R R?
U 1 1 581E152F
P 15100 1550
F 0 "R?" V 15180 1550 50  0000 C CNN
F 1 "10k" V 15100 1550 50  0000 C CNN
F 2 "" V 15030 1550 50  0000 C CNN
F 3 "" H 15100 1550 50  0000 C CNN
	1    15100 1550
	0    1    1    0   
$EndComp
$Comp
L GND #PWR045
U 1 1 581E1530
P 15450 1550
F 0 "#PWR045" H 15450 1300 50  0001 C CNN
F 1 "GND" H 15450 1400 50  0000 C CNN
F 2 "" H 15450 1550 50  0000 C CNN
F 3 "" H 15450 1550 50  0000 C CNN
	1    15450 1550
	0    -1   -1   0   
$EndComp
$Comp
L CONN_01X02 P?
U 1 1 581E1537
P 1100 4400
F 0 "P?" H 1100 4550 50  0000 C CNN
F 1 "EC PROBE" V 1200 4400 50  0000 C CNN
F 2 "" H 1100 4400 50  0000 C CNN
F 3 "" H 1100 4400 50  0000 C CNN
	1    1100 4400
	0    -1   -1   0   
$EndComp
$Comp
L R R?
U 1 1 581E1539
P 1450 4700
F 0 "R?" V 1530 4700 50  0000 C CNN
F 1 "1.1k" V 1450 4700 50  0000 C CNN
F 2 "" V 1380 4700 50  0000 C CNN
F 3 "" H 1450 4700 50  0000 C CNN
	1    1450 4700
	0    1    1    0   
$EndComp
$Comp
L CONN_01X02 P?
U 1 1 581E153A
P 2500 4400
F 0 "P?" H 2500 4550 50  0000 C CNN
F 1 "WATER TEMP PROBE" V 2600 4400 50  0000 C CNN
F 2 "" H 2500 4400 50  0000 C CNN
F 3 "" H 2500 4400 50  0000 C CNN
	1    2500 4400
	0    -1   -1   0   
$EndComp
$Comp
L R R?
U 1 1 581E153C
P 2850 4700
F 0 "R?" V 2930 4700 50  0000 C CNN
F 1 "15k" V 2850 4700 50  0000 C CNN
F 2 "" V 2780 4700 50  0000 C CNN
F 3 "" H 2850 4700 50  0000 C CNN
	1    2850 4700
	0    1    1    0   
$EndComp
$Comp
L +5V #PWR050
U 1 1 581E153D
P 3150 4700
F 0 "#PWR050" H 3150 4550 50  0001 C CNN
F 1 "+5V" H 3150 4840 50  0000 C CNN
F 2 "" H 3150 4700 50  0000 C CNN
F 3 "" H 3150 4700 50  0000 C CNN
	1    3150 4700
	0    1    1    0   
$EndComp
Text Notes 850  4050 0    99   ~ 0
WATER TEMP & CONDUCTIVITY
Text Notes 13400 4650 0    99   ~ 0
AIR TEMP &\nHUMIDITY
$Comp
L CONN_01X04 P?
U 1 1 581E154A
P 1100 1750
F 0 "P?" H 1100 2000 50  0000 C CNN
F 1 "CONN_01X04" V 1200 1750 50  0000 C CNN
F 2 "" H 1100 1750 50  0000 C CNN
F 3 "" H 1100 1750 50  0000 C CNN
	1    1100 1750
	-1   0    0    1   
$EndComp
$Comp
L GND #PWR058
U 1 1 581E154B
P 1300 2150
F 0 "#PWR058" H 1300 1900 50  0001 C CNN
F 1 "GND" H 1300 2000 50  0000 C CNN
F 2 "" H 1300 2150 50  0000 C CNN
F 3 "" H 1300 2150 50  0000 C CNN
	1    1300 2150
	1    0    0    -1  
$EndComp
Text Label 1550 1800 0    99   ~ 0
LCD_TX
Text Label 1550 1600 0    99   ~ 0
LCD_RX
$Comp
L +5V #PWR059
U 1 1 581E154C
P 1300 1300
F 0 "#PWR059" H 1300 1150 50  0001 C CNN
F 1 "+5V" H 1300 1440 50  0000 C CNN
F 2 "" H 1300 1300 50  0000 C CNN
F 3 "" H 1300 1300 50  0000 C CNN
	1    1300 1300
	1    0    0    -1  
$EndComp
Text Notes 1150 1050 0    99   ~ 0
LCD DISPLAY
Text Label 15100 2850 3    60   ~ 0
PH_12V
$Comp
L Q_NMOS_DGS Q?
U 1 1 581E1514
P 14050 1950
F 0 "Q?" H 14350 2000 50  0000 R CNN
F 1 "Q_NMOS_DGS" H 14700 1900 50  0000 R CNN
F 2 "" H 14250 2050 50  0000 C CNN
F 3 "" H 14050 1950 50  0000 C CNN
	1    14050 1950
	0    1    1    0   
$EndComp
$Comp
L Q_NMOS_DGS Q?
U 1 1 581E1515
P 13200 2150
F 0 "Q?" H 13500 2200 50  0000 R CNN
F 1 "Q_NMOS_DGS" H 13850 2100 50  0000 R CNN
F 2 "" H 13400 2250 50  0000 C CNN
F 3 "" H 13200 2150 50  0000 C CNN
	1    13200 2150
	0    1    1    0   
$EndComp
Text Label 14250 2850 3    60   ~ 0
NUTR_GND
Text Label 2550 5050 0    60   ~ 0
WTEMP_OUT
$Comp
L GND #PWR049
U 1 1 581E153B
P 2450 4800
F 0 "#PWR049" H 2450 4550 50  0001 C CNN
F 1 "GND" H 2450 4650 50  0000 C CNN
F 2 "" H 2450 4800 50  0000 C CNN
F 3 "" H 2450 4800 50  0000 C CNN
	1    2450 4800
	1    0    0    -1  
$EndComp
Text Label 1750 4700 0    60   ~ 0
EC_POWER
Text Label 1150 5050 0    60   ~ 0
EC_OUT
$Comp
L GND #PWR048
U 1 1 581E1538
P 1050 4800
F 0 "#PWR048" H 1050 4550 50  0001 C CNN
F 1 "GND" H 1050 4650 50  0000 C CNN
F 2 "" H 1050 4800 50  0000 C CNN
F 3 "" H 1050 4800 50  0000 C CNN
	1    1050 4800
	1    0    0    -1  
$EndComp
Text Label 13600 5450 2    60   ~ 0
DHT_DATA
$Comp
L +5V #PWR051
U 1 1 581E153F
P 13650 5250
F 0 "#PWR051" H 13650 5100 50  0001 C CNN
F 1 "+5V" H 13650 5390 50  0000 C CNN
F 2 "" H 13650 5250 50  0000 C CNN
F 3 "" H 13650 5250 50  0000 C CNN
	1    13650 5250
	0    -1   -1   0   
$EndComp
$Comp
L CONN_01X03 P?
U 1 1 581E153E
P 13900 4900
F 0 "P?" H 13900 5100 50  0000 C CNN
F 1 "DHT11 MODULE" V 14000 4900 50  0000 C CNN
F 2 "" H 13900 4900 50  0000 C CNN
F 3 "" H 13900 4900 50  0000 C CNN
	1    13900 4900
	0    -1   -1   0   
$EndComp
$Comp
L GND #PWR052
U 1 1 581E1540
P 14000 5600
F 0 "#PWR052" H 14000 5350 50  0001 C CNN
F 1 "GND" H 14000 5450 50  0000 C CNN
F 2 "" H 14000 5600 50  0000 C CNN
F 3 "" H 14000 5600 50  0000 C CNN
	1    14000 5600
	1    0    0    -1  
$EndComp
$Comp
L R R?
U 1 1 581E1541
P 13750 5700
F 0 "R?" V 13830 5700 50  0000 C CNN
F 1 "5k" V 13750 5700 50  0000 C CNN
F 2 "" V 13680 5700 50  0000 C CNN
F 3 "" H 13750 5700 50  0000 C CNN
	1    13750 5700
	1    0    0    -1  
$EndComp
$Comp
L +5V #PWR053
U 1 1 581E1542
P 13750 6000
F 0 "#PWR053" H 13750 5850 50  0001 C CNN
F 1 "+5V" H 13750 6140 50  0000 C CNN
F 2 "" H 13750 6000 50  0000 C CNN
F 3 "" H 13750 6000 50  0000 C CNN
	1    13750 6000
	-1   0    0    1   
$EndComp
$Comp
L STM32F091CBU6 U?
U 1 1 58EAEB8D
P 8500 4550
F 0 "U?" H 8600 4150 60  0000 C CNN
F 1 "STM32F091CBU6" H 8600 4450 60  0000 C CNN
F 2 "" H 8600 4150 60  0000 C CNN
F 3 "" H 8600 4150 60  0000 C CNN
	1    8500 4550
	1    0    0    -1  
$EndComp
$Comp
L TPS62177DQCR U?
U 1 1 58EB0A03
P 2600 7850
F 0 "U?" H 2600 8250 60  0000 C CNN
F 1 "TPS62177DQCR" V 2450 8300 60  0000 C CNN
F 2 "" H 2600 7850 60  0000 C CNN
F 3 "" H 2600 7850 60  0000 C CNN
	1    2600 7850
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR?
U 1 1 58EB15EE
P 1200 7300
F 0 "#PWR?" H 1200 7050 50  0001 C CNN
F 1 "GND" H 1200 7150 50  0000 C CNN
F 2 "" H 1200 7300 50  0000 C CNN
F 3 "" H 1200 7300 50  0000 C CNN
	1    1200 7300
	1    0    0    -1  
$EndComp
$Comp
L C C?
U 1 1 58EB17F7
P 1350 7750
F 0 "C?" H 1375 7850 50  0000 L CNN
F 1 "2.2 uF" H 1375 7650 50  0000 L CNN
F 2 "" H 1388 7600 50  0000 C CNN
F 3 "" H 1350 7750 50  0000 C CNN
	1    1350 7750
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR?
U 1 1 58EB1888
P 1350 8050
F 0 "#PWR?" H 1350 7800 50  0001 C CNN
F 1 "GND" H 1350 7900 50  0000 C CNN
F 2 "" H 1350 8050 50  0000 C CNN
F 3 "" H 1350 8050 50  0000 C CNN
	1    1350 8050
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR?
U 1 1 58EB1C18
P 3350 7750
F 0 "#PWR?" H 3350 7500 50  0001 C CNN
F 1 "GND" H 3350 7600 50  0000 C CNN
F 2 "" H 3350 7750 50  0000 C CNN
F 3 "" H 3350 7750 50  0000 C CNN
	1    3350 7750
	1    0    0    -1  
$EndComp
$Comp
L L_Small L?
U 1 1 58EB2174
P 3650 7300
F 0 "L?" H 3680 7340 50  0000 L CNN
F 1 "10 uH" H 3680 7260 50  0000 L CNN
F 2 "" H 3650 7300 50  0000 C CNN
F 3 "" H 3650 7300 50  0000 C CNN
	1    3650 7300
	0    1    1    0   
$EndComp
$Comp
L R R?
U 1 1 58EB2720
P 3800 7500
F 0 "R?" V 3880 7500 50  0000 C CNN
F 1 "100k" V 3800 7500 50  0000 C CNN
F 2 "" V 3730 7500 50  0000 C CNN
F 3 "" H 3800 7500 50  0000 C CNN
	1    3800 7500
	1    0    0    -1  
$EndComp
Text Label 4000 7650 0    60   ~ 0
3.3_PG
$Comp
L C C?
U 1 1 58EB2D7E
P 4550 7500
F 0 "C?" H 4575 7600 50  0000 L CNN
F 1 "22uF" H 4575 7400 50  0000 L CNN
F 2 "" H 4588 7350 50  0000 C CNN
F 3 "" H 4550 7500 50  0000 C CNN
	1    4550 7500
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR?
U 1 1 58EB2ECB
P 4550 7800
F 0 "#PWR?" H 4550 7550 50  0001 C CNN
F 1 "GND" H 4550 7650 50  0000 C CNN
F 2 "" H 4550 7800 50  0000 C CNN
F 3 "" H 4550 7800 50  0000 C CNN
	1    4550 7800
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR?
U 1 1 58EB8C58
P 1750 7750
F 0 "#PWR?" H 1750 7500 50  0001 C CNN
F 1 "GND" H 1750 7600 50  0000 C CNN
F 2 "" H 1750 7750 50  0000 C CNN
F 3 "" H 1750 7750 50  0000 C CNN
	1    1750 7750
	1    0    0    -1  
$EndComp
Text Notes 2150 6900 0    60   ~ 0
3.3 V REGULATOR
Text Label 3300 7400 0    60   ~ 0
SLEEP
Text Label 7200 4000 0    60   ~ 0
3.3V
$Comp
L C C?
U 1 1 58EBCABB
P 7600 3250
F 0 "C?" H 7625 3350 50  0000 L CNN
F 1 "100nF" H 7625 3150 50  0000 L CNN
F 2 "" H 7638 3100 50  0000 C CNN
F 3 "" H 7600 3250 50  0000 C CNN
	1    7600 3250
	0    1    1    0   
$EndComp
$Comp
L GND #PWR?
U 1 1 58EBCD18
P 7350 3400
F 0 "#PWR?" H 7350 3150 50  0001 C CNN
F 1 "GND" H 7350 3250 50  0000 C CNN
F 2 "" H 7350 3400 50  0000 C CNN
F 3 "" H 7350 3400 50  0000 C CNN
	1    7350 3400
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR?
U 1 1 58EBD12B
P 8250 3100
F 0 "#PWR?" H 8250 2850 50  0001 C CNN
F 1 "GND" H 8250 2950 50  0000 C CNN
F 2 "" H 8250 3100 50  0000 C CNN
F 3 "" H 8250 3100 50  0000 C CNN
	1    8250 3100
	0    -1   -1   0   
$EndComp
$Comp
L C C?
U 1 1 58EBF4D0
P 6550 5050
F 0 "C?" H 6575 5150 50  0000 L CNN
F 1 "10nF" H 6575 4950 50  0000 L CNN
F 2 "" H 6588 4900 50  0000 C CNN
F 3 "" H 6550 5050 50  0000 C CNN
	1    6550 5050
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR?
U 1 1 58EBF632
P 6550 5300
F 0 "#PWR?" H 6550 5050 50  0001 C CNN
F 1 "GND" H 6550 5150 50  0000 C CNN
F 2 "" H 6550 5300 50  0000 C CNN
F 3 "" H 6550 5300 50  0000 C CNN
	1    6550 5300
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR?
U 1 1 58EBF8F0
P 6800 5300
F 0 "#PWR?" H 6800 5050 50  0001 C CNN
F 1 "GND" H 6800 5150 50  0000 C CNN
F 2 "" H 6800 5300 50  0000 C CNN
F 3 "" H 6800 5300 50  0000 C CNN
	1    6800 5300
	1    0    0    -1  
$EndComp
$Comp
L C C?
U 1 1 58ED4518
P 6800 5050
F 0 "C?" H 6825 5150 50  0000 L CNN
F 1 "1uF" H 6825 4950 50  0000 L CNN
F 2 "" H 6838 4900 50  0000 C CNN
F 3 "" H 6800 5050 50  0000 C CNN
	1    6800 5050
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR?
U 1 1 58ED4978
P 8950 6200
F 0 "#PWR?" H 8950 5950 50  0001 C CNN
F 1 "GND" H 8950 6050 50  0000 C CNN
F 2 "" H 8950 6200 50  0000 C CNN
F 3 "" H 8950 6200 50  0000 C CNN
	1    8950 6200
	1    0    0    -1  
$EndComp
Wire Wire Line
	12500 1950 13200 1950
Wire Wire Line
	12500 1750 14050 1750
Wire Wire Line
	12500 1550 14950 1550
Wire Wire Line
	13000 2550 13000 2250
Wire Wire Line
	13850 2350 13850 2050
Wire Wire Line
	14400 2150 14400 1850
Wire Wire Line
	13400 2250 13400 2850
Wire Wire Line
	14250 2050 14250 2850
Wire Wire Line
	14800 1850 14800 2850
Wire Wire Line
	13700 2850 13700 2750
Wire Wire Line
	14550 2850 14550 2750
Wire Wire Line
	15100 2850 15100 2750
Wire Wire Line
	12900 2100 12900 1950
Connection ~ 12900 1950
Wire Wire Line
	12900 2400 12900 2500
Wire Wire Line
	12900 2500 13000 2500
Connection ~ 13000 2500
Wire Wire Line
	13600 1900 13600 1750
Connection ~ 13600 1750
Wire Wire Line
	13600 2300 13600 2200
Wire Wire Line
	15450 1550 15250 1550
Connection ~ 14600 1550
Wire Wire Line
	1050 4600 1050 4800
Wire Wire Line
	1150 4600 1150 5050
Wire Wire Line
	1150 4700 1300 4700
Wire Wire Line
	1600 4700 1750 4700
Connection ~ 1150 4700
Wire Wire Line
	2450 4600 2450 4800
Wire Wire Line
	2550 4600 2550 5050
Wire Wire Line
	2550 4700 2700 4700
Wire Wire Line
	3000 4700 3150 4700
Connection ~ 2550 4700
Wire Wire Line
	13800 5100 13800 5250
Wire Wire Line
	13800 5250 13650 5250
Wire Wire Line
	13600 5450 13900 5450
Wire Wire Line
	14000 5100 14000 5600
Wire Wire Line
	13750 5550 13750 5450
Connection ~ 13750 5450
Wire Wire Line
	1300 2150 1300 1900
Wire Wire Line
	1550 1800 1300 1800
Wire Wire Line
	1300 1700 1550 1700
Wire Wire Line
	1550 1700 1550 1600
Wire Wire Line
	1300 1600 1300 1300
Wire Wire Line
	13900 5450 13900 5100
Wire Wire Line
	13750 5850 13750 6000
Connection ~ 13400 2750
Connection ~ 14250 2750
Connection ~ 14800 2750
Wire Wire Line
	1200 7300 1200 7200
Wire Wire Line
	1200 7200 1850 7200
Wire Wire Line
	1850 7300 1350 7300
Wire Wire Line
	1350 7300 1350 7600
Wire Wire Line
	1350 8050 1350 7900
Wire Wire Line
	1850 7400 1750 7400
Wire Wire Line
	1750 7400 1750 7300
Connection ~ 1750 7300
Wire Wire Line
	3200 7600 3350 7600
Wire Wire Line
	3200 7200 4650 7200
Wire Wire Line
	3200 7300 3550 7300
Wire Wire Line
	3750 7300 3800 7300
Wire Wire Line
	3800 7200 3800 7350
Connection ~ 3800 7200
Wire Wire Line
	3350 7600 3350 7750
Connection ~ 3800 7300
Wire Wire Line
	3200 7500 3500 7500
Wire Wire Line
	3500 7500 3500 7650
Wire Wire Line
	3500 7650 4000 7650
Connection ~ 3800 7650
Wire Wire Line
	4550 7350 4550 7200
Connection ~ 4550 7200
Wire Wire Line
	4550 7800 4550 7650
Wire Wire Line
	1750 7750 1750 7600
Wire Wire Line
	1750 7600 1850 7600
Wire Wire Line
	3300 7400 3200 7400
Wire Wire Line
	9050 5550 9050 5900
Wire Wire Line
	9500 4000 10550 4000
Wire Wire Line
	7950 3050 7950 3550
Wire Wire Line
	7750 3250 7950 3250
Connection ~ 7950 3250
Wire Wire Line
	7450 3250 7350 3250
Wire Wire Line
	7350 3250 7350 3400
Wire Wire Line
	8050 3550 8050 3100
Wire Wire Line
	8050 3100 8250 3100
Wire Wire Line
	7200 4000 7500 4000
Wire Wire Line
	6550 4900 6550 4800
Connection ~ 6550 4800
Wire Wire Line
	6550 5300 6550 5200
Wire Wire Line
	6800 4800 6800 4900
Connection ~ 6800 4800
Wire Wire Line
	6800 5300 6800 5200
Wire Wire Line
	6100 4700 7500 4700
Wire Wire Line
	8950 5550 8950 6200
Connection ~ 9050 5700
$Comp
L C C?
U 1 1 58ED5F2A
P 9450 5950
F 0 "C?" H 9475 6050 50  0000 L CNN
F 1 "4.7uF" H 9475 5850 50  0000 L CNN
F 2 "" H 9488 5800 50  0000 C CNN
F 3 "" H 9450 5950 50  0000 C CNN
	1    9450 5950
	1    0    0    -1  
$EndComp
$Comp
L C C?
U 1 1 58ED5FAF
P 9800 5950
F 0 "C?" H 9825 6050 50  0000 L CNN
F 1 "100nF" H 9825 5850 50  0000 L CNN
F 2 "" H 9838 5800 50  0000 C CNN
F 3 "" H 9800 5950 50  0000 C CNN
	1    9800 5950
	1    0    0    -1  
$EndComp
Wire Wire Line
	9450 5800 9450 5700
Wire Wire Line
	9050 5700 9800 5700
Connection ~ 9450 5700
$Comp
L GND #PWR?
U 1 1 58ED6352
P 9450 6200
F 0 "#PWR?" H 9450 5950 50  0001 C CNN
F 1 "GND" H 9450 6050 50  0000 C CNN
F 2 "" H 9450 6200 50  0000 C CNN
F 3 "" H 9450 6200 50  0000 C CNN
	1    9450 6200
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR?
U 1 1 58ED63D2
P 9800 6200
F 0 "#PWR?" H 9800 5950 50  0001 C CNN
F 1 "GND" H 9800 6050 50  0000 C CNN
F 2 "" H 9800 6200 50  0000 C CNN
F 3 "" H 9800 6200 50  0000 C CNN
	1    9800 6200
	1    0    0    -1  
$EndComp
Wire Wire Line
	9800 6100 9800 6200
Wire Wire Line
	9450 6100 9450 6200
Wire Wire Line
	9800 5700 9800 5800
$Comp
L C C?
U 1 1 58ED8B6C
P 10250 4250
F 0 "C?" H 10275 4350 50  0000 L CNN
F 1 "4.7uF" H 10275 4150 50  0000 L CNN
F 2 "" H 10288 4100 50  0000 C CNN
F 3 "" H 10250 4250 50  0000 C CNN
	1    10250 4250
	1    0    0    -1  
$EndComp
$Comp
L C C?
U 1 1 58ED8BFB
P 10550 4250
F 0 "C?" H 10575 4350 50  0000 L CNN
F 1 "100nF" H 10575 4150 50  0000 L CNN
F 2 "" H 10588 4100 50  0000 C CNN
F 3 "" H 10550 4250 50  0000 C CNN
	1    10550 4250
	1    0    0    -1  
$EndComp
Wire Wire Line
	10250 4000 10250 4100
Wire Wire Line
	10550 4000 10550 4100
Connection ~ 10250 4000
$Comp
L GND #PWR?
U 1 1 58ED8E70
P 10250 4500
F 0 "#PWR?" H 10250 4250 50  0001 C CNN
F 1 "GND" H 10250 4350 50  0000 C CNN
F 2 "" H 10250 4500 50  0000 C CNN
F 3 "" H 10250 4500 50  0000 C CNN
	1    10250 4500
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR?
U 1 1 58ED8EF4
P 10550 4500
F 0 "#PWR?" H 10550 4250 50  0001 C CNN
F 1 "GND" H 10550 4350 50  0000 C CNN
F 2 "" H 10550 4500 50  0000 C CNN
F 3 "" H 10550 4500 50  0000 C CNN
	1    10550 4500
	1    0    0    -1  
$EndComp
Wire Wire Line
	10550 4400 10550 4500
Wire Wire Line
	10250 4400 10250 4500
Wire Wire Line
	9500 4100 10100 4100
Wire Wire Line
	10100 4100 10100 4450
Wire Wire Line
	10100 4450 10250 4450
Connection ~ 10250 4450
$Comp
L Crystal Y?
U 1 1 58F81FD1
P 6650 3900
F 0 "Y?" H 6650 4050 50  0000 C CNN
F 1 "Crystal" H 6650 3750 50  0000 C CNN
F 2 "" H 6650 3900 50  0000 C CNN
F 3 "535-10239-1-ND" V 6400 3950 50  0000 C CNN
	1    6650 3900
	0    1    1    0   
$EndComp
Wire Wire Line
	6900 3750 6900 4400
Wire Wire Line
	6900 3750 6200 3750
Wire Wire Line
	6650 4050 6650 4500
$Comp
L C C?
U 1 1 58F822E5
P 6200 3900
F 0 "C?" H 6225 4000 50  0000 L CNN
F 1 "27pF" H 6225 3800 50  0000 L CNN
F 2 "" H 6238 3750 50  0000 C CNN
F 3 "" H 6200 3900 50  0000 C CNN
	1    6200 3900
	1    0    0    -1  
$EndComp
$Comp
L C C?
U 1 1 58F8237A
P 6450 4150
F 0 "C?" H 6475 4250 50  0000 L CNN
F 1 "27pF" H 6475 4050 50  0000 L CNN
F 2 "" H 6488 4000 50  0000 C CNN
F 3 "" H 6450 4150 50  0000 C CNN
	1    6450 4150
	0    1    1    0   
$EndComp
Wire Wire Line
	6600 4150 6650 4150
Connection ~ 6650 4150
Connection ~ 6650 3750
Wire Wire Line
	6200 4050 6200 4300
Wire Wire Line
	6200 4150 6300 4150
Connection ~ 6200 4150
$Comp
L GND #PWR?
U 1 1 58F8283F
P 6200 4300
F 0 "#PWR?" H 6200 4050 50  0001 C CNN
F 1 "GND" H 6200 4150 50  0000 C CNN
F 2 "" H 6200 4300 50  0000 C CNN
F 3 "" H 6200 4300 50  0000 C CNN
	1    6200 4300
	1    0    0    -1  
$EndComp
Wire Wire Line
	6900 4400 7500 4400
Wire Wire Line
	6650 4500 7500 4500
$Comp
L GND #PWR?
U 1 1 58F8576D
P 6100 4850
F 0 "#PWR?" H 6100 4600 50  0001 C CNN
F 1 "GND" H 6100 4700 50  0000 C CNN
F 2 "" H 6100 4850 50  0000 C CNN
F 3 "" H 6100 4850 50  0000 C CNN
	1    6100 4850
	1    0    0    -1  
$EndComp
Wire Wire Line
	6100 4850 6100 4700
Wire Wire Line
	5100 4600 7500 4600
Text Label 5100 4600 0    60   ~ 0
RESET
$Comp
L C C?
U 1 1 58F8605C
P 5750 4850
F 0 "C?" H 5775 4950 50  0000 L CNN
F 1 "0.1uF" H 5775 4750 50  0000 L CNN
F 2 "" H 5788 4700 50  0000 C CNN
F 3 "" H 5750 4850 50  0000 C CNN
	1    5750 4850
	1    0    0    -1  
$EndComp
Wire Wire Line
	5750 4700 5750 4600
Connection ~ 5750 4600
Wire Wire Line
	5750 5000 5750 5100
$Comp
L GND #PWR?
U 1 1 58F86387
P 5750 5100
F 0 "#PWR?" H 5750 4850 50  0001 C CNN
F 1 "GND" H 5750 4950 50  0000 C CNN
F 2 "" H 5750 5100 50  0000 C CNN
F 3 "" H 5750 5100 50  0000 C CNN
	1    5750 5100
	1    0    0    -1  
$EndComp
$Comp
L SW_PUSH SW?
U 1 1 58F87581
P 5450 5000
F 0 "SW?" H 5600 5110 50  0000 C CNN
F 1 "SW_PUSH" H 5450 4920 50  0000 C CNN
F 2 "" H 5450 5000 50  0000 C CNN
F 3 "" H 5450 5000 50  0000 C CNN
	1    5450 5000
	0    -1   -1   0   
$EndComp
Wire Wire Line
	5450 4700 5450 4600
Connection ~ 5450 4600
Wire Wire Line
	5450 5300 5450 5450
$Comp
L GND #PWR?
U 1 1 58F87860
P 5450 5450
F 0 "#PWR?" H 5450 5200 50  0001 C CNN
F 1 "GND" H 5450 5300 50  0000 C CNN
F 2 "" H 5450 5450 50  0000 C CNN
F 3 "" H 5450 5450 50  0000 C CNN
	1    5450 5450
	1    0    0    -1  
$EndComp
Wire Wire Line
	8350 3550 8350 3250
Wire Wire Line
	8350 3250 8500 3250
Wire Wire Line
	8500 3250 8500 2550
Text Label 8500 2550 0    60   ~ 0
BOOT0
$Comp
L R R?
U 1 1 58F8C61C
P 8250 2700
F 0 "R?" V 8330 2700 50  0000 C CNN
F 1 "10k" V 8250 2700 50  0000 C CNN
F 2 "" V 8180 2700 50  0000 C CNN
F 3 "" H 8250 2700 50  0000 C CNN
	1    8250 2700
	0    1    1    0   
$EndComp
Wire Wire Line
	8400 2700 8500 2700
Connection ~ 8500 2700
$Comp
L GND #PWR?
U 1 1 58F8C7DB
P 8000 2700
F 0 "#PWR?" H 8000 2450 50  0001 C CNN
F 1 "GND" H 8000 2550 50  0000 C CNN
F 2 "" H 8000 2700 50  0000 C CNN
F 3 "" H 8000 2700 50  0000 C CNN
	1    8000 2700
	0    1    1    0   
$EndComp
Wire Wire Line
	8000 2700 8100 2700
Text Label 9700 4500 0    60   ~ 0
BTL_RX
Wire Wire Line
	9700 4500 9500 4500
Text Label 9700 4600 0    60   ~ 0
BTL_TX
Wire Wire Line
	9700 4600 9500 4600
Text Label 9350 3400 0    60   ~ 0
SBC_TX
Wire Wire Line
	9350 3400 9050 3400
Wire Wire Line
	9050 3400 9050 3550
Wire Wire Line
	8950 3550 8950 3250
Wire Wire Line
	8950 3250 9350 3250
Text Label 9350 3250 0    60   ~ 0
SBC_RX
Text Label 8250 6050 0    60   ~ 0
LCD_TX
Wire Wire Line
	8250 6050 8750 6050
Wire Wire Line
	8750 6050 8750 5550
Text Label 8250 6150 0    60   ~ 0
LCD_RX
Wire Wire Line
	8250 6150 8850 6150
Wire Wire Line
	8850 6150 8850 5550
Text Label 9700 4400 0    60   ~ 0
CAN_RX
Wire Wire Line
	9700 4400 9500 4400
Text Label 9700 4300 0    60   ~ 0
CAN_TX
Wire Wire Line
	9700 4300 9500 4300
$Comp
L TLE7251V U?
U 1 1 58F9A09B
P 12900 7850
F 0 "U?" H 12900 7900 60  0000 C CNN
F 1 "TLE7251V" H 12900 8100 60  0000 C CNN
F 2 "" H 12900 7850 60  0000 C CNN
F 3 "" H 12900 7850 60  0000 C CNN
	1    12900 7850
	1    0    0    -1  
$EndComp
Text Label 11750 7550 0    60   ~ 0
CAN_TX
Wire Wire Line
	11750 7550 12200 7550
Text Label 11750 7850 0    60   ~ 0
CAN_RX
Wire Wire Line
	11750 7850 12200 7850
Wire Wire Line
	12200 7650 11350 7650
Wire Wire Line
	11350 7650 11350 7950
$Comp
L GND #PWR?
U 1 1 58F9ABD1
P 11350 7950
F 0 "#PWR?" H 11350 7700 50  0001 C CNN
F 1 "GND" H 11350 7800 50  0000 C CNN
F 2 "" H 11350 7950 50  0000 C CNN
F 3 "" H 11350 7950 50  0000 C CNN
	1    11350 7950
	1    0    0    -1  
$EndComp
Wire Wire Line
	12200 7750 11500 7750
Wire Wire Line
	11500 7750 11500 8300
Wire Wire Line
	11500 8150 11750 8150
$Comp
L +5V #PWR?
U 1 1 58F9B9A2
P 11750 8150
F 0 "#PWR?" H 11750 8000 50  0001 C CNN
F 1 "+5V" H 11750 8290 50  0000 C CNN
F 2 "" H 11750 8150 50  0000 C CNN
F 3 "" H 11750 8150 50  0000 C CNN
	1    11750 8150
	0    1    1    0   
$EndComp
$Comp
L C C?
U 1 1 58F9BA34
P 11500 8450
F 0 "C?" H 11525 8550 50  0000 L CNN
F 1 "100nF" H 11525 8350 50  0000 L CNN
F 2 "" H 11538 8300 50  0000 C CNN
F 3 "" H 11500 8450 50  0000 C CNN
	1    11500 8450
	1    0    0    -1  
$EndComp
Connection ~ 11500 8150
$Comp
L GND #PWR?
U 1 1 58F9BD47
P 11500 8700
F 0 "#PWR?" H 11500 8450 50  0001 C CNN
F 1 "GND" H 11500 8550 50  0000 C CNN
F 2 "" H 11500 8700 50  0000 C CNN
F 3 "" H 11500 8700 50  0000 C CNN
	1    11500 8700
	1    0    0    -1  
$EndComp
Wire Wire Line
	11500 8700 11500 8600
$Comp
L +3.3V #PWR?
U 1 1 58F9C712
P 4650 7200
F 0 "#PWR?" H 4650 7050 50  0001 C CNN
F 1 "+3.3V" H 4650 7340 50  0000 C CNN
F 2 "" H 4650 7200 50  0000 C CNN
F 3 "" H 4650 7200 50  0000 C CNN
	1    4650 7200
	0    1    1    0   
$EndComp
Wire Wire Line
	6300 4800 7500 4800
$Comp
L +3.3V #PWR?
U 1 1 58F9CF41
P 6300 4850
F 0 "#PWR?" H 6300 4700 50  0001 C CNN
F 1 "+3.3V" H 6300 4990 50  0000 C CNN
F 2 "" H 6300 4850 50  0000 C CNN
F 3 "" H 6300 4850 50  0000 C CNN
	1    6300 4850
	-1   0    0    1   
$EndComp
Wire Wire Line
	6300 4850 6300 4800
$Comp
L +3.3V #PWR?
U 1 1 58F9D708
P 9150 6000
F 0 "#PWR?" H 9150 5850 50  0001 C CNN
F 1 "+3.3V" H 9150 6140 50  0000 C CNN
F 2 "" H 9150 6000 50  0000 C CNN
F 3 "" H 9150 6000 50  0000 C CNN
	1    9150 6000
	-1   0    0    1   
$EndComp
Wire Wire Line
	9150 6000 9150 5900
Wire Wire Line
	9150 5900 9050 5900
$Comp
L +3.3V #PWR?
U 1 1 58F9DD50
P 7950 3050
F 0 "#PWR?" H 7950 2900 50  0001 C CNN
F 1 "+3.3V" H 7950 3190 50  0000 C CNN
F 2 "" H 7950 3050 50  0000 C CNN
F 3 "" H 7950 3050 50  0000 C CNN
	1    7950 3050
	1    0    0    -1  
$EndComp
$Comp
L +3.3V #PWR?
U 1 1 58F9E264
P 14350 7800
F 0 "#PWR?" H 14350 7650 50  0001 C CNN
F 1 "+3.3V" H 14350 7940 50  0000 C CNN
F 2 "" H 14350 7800 50  0000 C CNN
F 3 "" H 14350 7800 50  0000 C CNN
	1    14350 7800
	1    0    0    -1  
$EndComp
Wire Wire Line
	13600 7850 14350 7850
Text Label 13800 7750 0    60   ~ 0
CANL
Wire Wire Line
	13800 7750 13600 7750
Text Label 13800 7650 0    60   ~ 0
CANH
Wire Wire Line
	13800 7650 13600 7650
Wire Wire Line
	14350 7850 14350 7800
Text Label 9700 4200 0    60   ~ 0
CAN_STB
Wire Wire Line
	9700 4200 9500 4200
Text Label 13800 7550 0    60   ~ 0
CAN_STB
Wire Wire Line
	13800 7550 13600 7550
Text Notes 12500 7300 0    60   ~ 0
CAN TRANCEIVER
Text Label 7050 5000 0    60   ~ 0
EC_OUT
Wire Wire Line
	7050 5000 7500 5000
Text Label 7050 5100 0    60   ~ 0
PH_OUT
Wire Wire Line
	7050 5100 7500 5100
Text Label 7250 5650 0    60   ~ 0
WTEMP_OUT
Wire Wire Line
	7950 5550 7950 5650
Wire Wire Line
	7950 5650 7250 5650
Text Label 7050 4900 0    60   ~ 0
EC_PWR
Wire Wire Line
	7050 4900 7500 4900
Text Label 8150 5950 0    60   ~ 0
DHT_DATA
Wire Wire Line
	8150 5950 8650 5950
Wire Wire Line
	8650 5950 8650 5550
Text Label 9700 5100 0    60   ~ 0
PMP_ON
Wire Wire Line
	9700 5100 9500 5100
Wire Wire Line
	9500 5000 9700 5000
Text Label 9700 5000 0    60   ~ 0
NUTR_ON
Text Label 9700 4900 0    60   ~ 0
PH_ON
Wire Wire Line
	9700 4900 9500 4900
Text Label 12500 1950 0    60   ~ 0
PMP_ON
Text Label 12500 1750 0    60   ~ 0
NUTR_ON
Text Label 12500 1550 0    60   ~ 0
PH_ON
Text Notes 13600 1400 0    60   ~ 0
PUMP CONTROLS
$EndSCHEMATC
