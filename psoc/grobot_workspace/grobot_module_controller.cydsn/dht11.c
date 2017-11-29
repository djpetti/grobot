#include <project.h>

#include "dht11.h"
#include <stdint.h>
#include <stddef.h>
#include <dht.h>

void delay(void);
void unpack_dht_data(void);

uint8_t g_check;
uint8_t g_decode_flag;
uint8_t g_decoded_temperature_data;
uint8_t g_decoded_humidity_data;

int g_temperature_values[8];
int g_humidity_values[8];
int g_diff_count_values[44] = {0};
int g_countvalues_datatimer[44] = {0};
int g_executed;
int g_count;
int g_risingedge_counts;
int g_has_been_executed;

_CY_ISR_PROTO(Delay_Timer_ISR_Handler);
_CY_ISR_PROTO(DHT_Pin_ISR_Handler);

// What Return_Decoded_Temperature does:
//     - This is used to pass the decoded temp data out 
//       through a call in dht11.h
//
// Parameters: None
// Returns: - Data in g_decoded_temperature_data

uint8_t dht_get_temperature(){
    
    if(g_decoded_temperature_data == NULL) {
        return -1;
    }
    else{
        return g_decoded_temperature_data; 
    }    
}    

// What Return_Decoded_Humidity does:
//    -Returns the data in g_decoded_humidity_data
// 
// Parameters: None
// Returns: uint8_t g_decoded_humidity_data

uint8_t dht_get_humidity(){
    
    if(g_decoded_humidity_data == NULL) {
        return -1;
    }else{
        return g_decoded_humidity_data;
    }    
}   


// What delay_funct does:
//    - Enable Delay_Timer_ISR to detect Delay_Timer Terminal Count interrupt
//    - Start the Delay_Timer component.
//    - This function does not use the CPU delay API, CyDelay(),
//        but uses Delay_Timer to generate delay. 
//
// Parameters: None
// Return: None

void delay_funct(void){
    g_count = 1;
    g_executed = 0;
    Delay_Timer_ISR_Enable();
    // Write 0 to Control_Reg_Delay_Timer to starting Delay_Timer component 
    Control_Reg_Delay_Timer_Write(0);
}    


// What decode dht data does:
//    - The value stored in g_countvalues_datatimer[] array is used to decode
//      the data of DHT output
//    - The time difference between g_countvalues_datatimer[i]
//      and g_countvalues_datatimer[i-1] is calculated
//    - If the g_countvalues_datatimer[i] is approximately 70 counts, it is data
 //     0, and if g_countvalues_datatimer[i] is approximately 120, it is data 1. 
//
// Parameters: None
// Returns: None

void decode_dht_data(void){
    int i;
    for(i=0; i<44; ++i) {
        g_diff_count_values[i] = g_countvalues_datatimer[i-1];
        g_diff_count_values[i] -= g_countvalues_datatimer[i];
    }
    
    int j;
    for(j=0; j<8; ++j) {
        if(g_diff_count_values[j+3]>100) {
            g_humidity_values[7-j]=1;
        }else{
            g_humidity_values[7-j]=0;
        }
        
        if(g_diff_count_values[j+19]>100) {
            g_temperature_values[7-j] = 1;
        }else{
            g_temperature_values[7-j] = 0;
        }
    }
    g_decoded_temperature_data = (uint8_t)((g_temperature_values[7]<<7) + (g_temperature_values[6]<<6) + (g_temperature_values[5]<<5) + (g_temperature_values[4]<<4) + (g_temperature_values[3] <<3) + (g_temperature_values[2] <<2) + (g_temperature_values[1]<<1) + g_temperature_values[0]);
    g_decoded_humidity_data = (uint8_t)((g_humidity_values[7]<<7) + (g_humidity_values[6]<<6) + (g_humidity_values[5]<<5) + (g_humidity_values[4]<<4) + (g_humidity_values[3] <<3) + (g_humidity_values[2] <<2) + (g_humidity_values[1]<<1) + g_humidity_values[0]);
    
    // Now the data is decoded
    g_decode_flag = 1;
    // From here we will have the acctual values. We can call functions from
    // here or send it out depending on what we decide to go with 
}    

// Name: Delay_Timer_ISR_Handler
// Summary:
//    - Interrupt Service Routine. Check the Delay_Timer status
//      and clear the interrupt
//    - change the Count and Executed status

_CY_ISR(Delay_Timer_ISR_Handler){
    
    if(Delay_Timer_ReadPeriod() == DELAY_ACQUISITION) {
        g_count = 2;                  
        g_executed=0;             
    }else if(Delay_Timer_ReadPeriod() == DELAY_PROCESSING) { 
        g_decode_flag = 1;
    }
    
    // Write 1 to the Contro_Reg_Delay_Timer to disable the Timer function 
    Control_Reg_Delay_Timer_Write(1);
    // Read the status register of Delay_Timer to clear interrupt
    Delay_Timer_ReadStatusRegister();
    // Clear the Delay_Timer_ISR interrupt
    Delay_Timer_ISR_ClearPending();
}    

_CY_ISR(DHT_Pin_ISR_Handler){
    // Clear the interrupt request of the ISR DHT_Pin_ISR 
    DHT_Pin_ISR_ClearPending();
    // Clear the interrupt request of the pin DHT_Pin
    DHT_Pin_ClearInterrupt();
    // Read the counter values of Data_Timer for processing
    g_countvalues_datatimer[g_risingedge_counts]=Data_Timer_ReadCounter();
    g_risingedge_counts++;
}

// What dht_init does:
//    - Initilizes all variables that need to be zeroed out and
//      otherwise. 
//    - Writes 1 to the pin as a starting condition
//    - Start various functions neccessary to read the conditions
//
// Paramers: None
// Returns: None

void dht_init(){
    g_check = 0;
    g_decode_flag = 0;
    g_risingedge_counts = 0;
    
    // Starts the data timer and delay timer components
    Data_Timer_Start();
    Delay_Timer_Start();
    
    // Write Controlregdatatimer and controlregdealytimer value
    // to 1 to keep them reset
    Control_Reg_Data_Timer_Write(1);
    Control_Reg_Delay_Timer_Write(1);
    
    // The pin value will be written as 1 as the starting condition
    DHT_Pin_Write(1);
    
    // Initilize dhtpinisr and delaytimeriser
    DHT_Pin_ISR_StartEx(DHT_Pin_ISR_Handler);
    Delay_Timer_ISR_StartEx(Delay_Timer_ISR_Handler);
    
    // Disable the ISR compondents
    DHT_Pin_ISR_Disable();
    Delay_Timer_ISR_Disable();
    
    // Initilize g_count to 0 and g_executed to 1
    g_count = 0;
    g_executed = 1;
    
    g_has_been_executed = 0;
}   


// What dht_start does:
//    Starts the dht components
//    Get output from dht11
//    Send out results
//
// Paramers: None
// Returns: None


void dht_start(){
    
    // Enable Global Interrupts
    CyGlobalIntEnable;
    
    // This is going to run until decode dht data is called
    // After this is done, the loop will end, and the data will
    // be in the respective variables
    
    switch (g_has_been_executed) {
        case 0:
            do {
                
                if(g_executed == 1 && g_count == 0) {
                    g_executed = 0;
                    g_risingedge_counts = 0;
                    CyDelayUs(50);
                    DHT_Pin_Write(0);
                    Delay_Timer_WritePeriod(DELAY_ACQUISITION);
                    // Call the delay function to set the DHT_Pin as low for 20ms 
                    delay_funct();
                }    
                
                if(g_count >= 2 && g_executed ==0) {
                    Control_Reg_Data_Timer_Write(0);
                    // Write 1 to DHT_Pin 
                    DHT_Pin_Write(1);
                    // Enable DHT_Pin_ISR to get data from the DHT11 sensor
                    DHT_Pin_ISR_Enable();
                    // To keep the DHT_Pin as High for 30us, the below function is called 
                    CyDelayUs(30);
                    Delay_Timer_WritePeriod(DELAY_PROCESSING);
                    Control_Reg_Delay_Timer_Write(0);
                    // Change the Executed and Count status to decode the DHT11 values
                    g_executed = 2;
                    g_count = 0;
                }
                
                if(g_decode_flag == 1) {
                    Control_Reg_Data_Timer_Write(1);
                    DHT_Pin_ISR_Disable(); 
                    DHT_Pin_Write(1);   
                    g_decode_flag = 0;
                    decode_dht_data();
                    g_executed = 1;
                    g_count = 0;
                }    
            
            } while (g_decode_flag == 1);
            g_has_been_executed = 1;
            break; 
            
        case 1:
            break;
    }    
    
    // When exited we will have the data in the two "decoded" variables
}    