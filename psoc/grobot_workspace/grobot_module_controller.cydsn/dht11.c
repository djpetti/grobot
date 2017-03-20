#include <project.h>

#include "dht11.h"

void delay(void);
void unpack_dht_data(void);

uint8_t check = 0;
uint8_t decode_flag=0;
uint8_t decoded_temperature_data;
uint8_t decoded_humidity_data;

int temperature_values[8], humidity_values[8];
int diff_count_values[44]={0};
int countvalues_datatimer[44]={0};
int executed;
int count;
int risingedge_counts=0;

_CY_ISR_PROTO(Delay_Timer_ISR_Handler);
_CY_ISR_PROTO(DHT_Pin_ISR_Handler);


//What dhtmain does:
//    Starts the dht components
//    Get output from dht11
//    Send out results
//
//Paramers: None
//Returns: None


void dhtmain(){
    decoded_temperature_data = -255;
    decoded_humidity_data = -255;
    
    //Starts the data timer and delay timer components
    Data_Timer_Start();
    Delay_Timer_Start();
    
    //Write Controlregdatatimer and controlregdealytimer value to 1 to keep them reset
    Control_Reg_Data_Timer_Write(1);
    Control_Reg_Delay_Timer_Write(1);
    
    //The pin value will be written as 1 as the starting condition
    DHT_Pin_Write(1);
    
    //Initilize dhtpinisr and delaytimeriser
    DHT_Pin_ISR_StartEx(DHT_Pin_ISR_Handler);
    Delay_Timer_ISR_StartEx(Delay_Timer_ISR_Handler);
    
    //Disable the ISR compondents
    DHT_Pin_ISR_Disable();
    Delay_Timer_ISR_Disable();
    
    //Initilize count to 0 and executed to 1
    count = 0;
    executed = 1;
    
    // Enable Global Interrupts
    CyGlobalIntEnable;
    
    //This is going to run until decode dht data is called
    //After this is done, the loop will end, and the data will
    //be in the respective variables
    int x;
    for(x=0;x<1;){
        
        if(executed == 1 && count == 0){
            executed = 0;
            risingedge_counts = 0;
            CyDelayUs(50);
            DHT_Pin_Write(0);
            Delay_Timer_WritePeriod(DELAY_ACQUISITION);
            //Call the delay function to stay the DHT_Pin as low for 20ms 
            delay_funct();
        }    
        
        if(count >= 2 && executed ==0){
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
            executed=2;
            cnt=0;
        }
        
        if(decode_flag==1){
            Control_Reg_Data_Timer_Write(1);
            DHT_Pin_ISR_Disable(); 
            DHT_Pin_Write(1);   
            decode_flag=0;
            Decode_DHT_Data();
            executed=1;
            count=0;
            x=1;
        }    
        
    }   
    
    //When exited we will have the data in the two "decoded" variables
    
}    


//What Return_Decoded_Temperature does:
//    -Returns the data in decoded_temperature_data
// 
//Parameters: None
//Returns: uint8_t decoded_temperature_data

uint8_t Return_Decoded_Temperature(){
    
    if(decoded_temperature_data == -255){
        return -1;
    }
    else{
        return decoded_temperature_data; 
    }    
}    

//What Return_Decoded_Humidity does:
//    -Returns the data in decoded_humidity_data
// 
//Parameters: None
//Returns: uint8_t decoded_humidity_data

uint8_t Return_Decoded_Temperature(){
    
    if(decoded_humidity_data == -255){
        return -1;
    }else{
        return decoded_humidity_data;
    }    
}   


//What delay_funct does:
//    - Enable Delay_Timer_ISR to detect Delay_Tiemr Terminal Count interrupt
//    - Start the Delay_Timer component.
//    - This function does not use the CPU delay API, CyDelay(), but uses Delay_Timer to generate delay. 
//
//Parameters: None
//Return: None

void delay_funct(void){
    count = 1;
    executed = 0;
    // Enable Delay_timer_ISR
    Delay_Timer_ISR_Enable();
    //Write 0 to Control_Reg_Delay_Timer to starting Delay_Timer component 
    Control_Reg_Delay_Timer_Write(0);
}    


//What decode dht data does:
//    - The value stored in countvalues_datatimer[] array, is used to decode the data of DHT output
//    - The time difference between countvalues_datatimer[i] and countvalues_datatimer[i-1] is calculated
//    - If the countvalues_datatimer[i] is approximately 70 counts, it is data 0, and if countvalues_datatimer[i] is approximately 120, it is data 1. 
//
//Parameters: None
//Returns: None

void Decode_DHT_Data(void){
    int i;
    for(i=0; i<44; i++){
        diff_count_values[i]=countvalues_datatimer[i-1]-countvalues_datatimer[i];
    }
    
    int j;
    for(j=0; j<8; j++){
        if(diff_count_values[j+3]>100){
            Humidity_Values[7-j]=1;
        }else{
            Humidity_Values[7-j]=0;
        }
        
        if(diff_count_values[j+19]>100){
            Temperature_Values[7-j]=1;
        }else{
            Temperature_Values[7-j]=0;
        }
    }
    decoded_temperature_data = (uint8_t)((Temperature_Values[7]<<7) + (Temperature_Values[6]<<6) + (Temperature_Values[5]<<5) + (Temperature_Values[4]<<4) + (Temperature_Values[3] <<3) + (Temperature_Values[2] <<2) + (Temperature_Values[1]<<1) + Temperature_Values[0]);
    decoded_humidity_data=(uint8_t)((Humidity_Values[7]<<7) + (Humidity_Values[6]<<6) + (Humidity_Values[5]<<5) + (Humidity_Values[4]<<4) + (Humidity_Values[3] <<3) + (Humidity_Values[2] <<2) + (Humidity_Values[1]<<1) + Humidity_Values[0]);
    
    //Now the data is decoded
    decode_flag = 1;
    //From here we will have the acctual values. We can call functions from
    //here or send it out depending on what we decide to go with 
}    

//Name: Delay_Timer_ISR_Handler
//Summary:
//    Interrupt Service Routine. Check the Delay_Timer status and clear the interrupt
//    change the Count and Executed status


_CY_ISR(Delay_Timer_ISR_Handler){
    
    if(Delay_Timer_ReadPeriod() == DELAY_ACQUISITION){
        count=2;                  
        executed=0;             
    }else if(Delay_Timer_ReadPeriod() == DELAY_PROCESSING){ 
        decode_flag=1;
    }
    
    //Write 1 to the Contro_Reg_Delay_Timer to disable the Timer function 
    Control_Reg_Delay_Timer_Write(1);
    //Read the status register of Delay_Timer to clear interrupt
    Delay_Timer_ReadStatusRegister();
    //Clear the Delay_Timer_ISR interrupt
    Delay_Timer_ISR_ClearPending();
}    


_CY_ISR(DHT_Pin_ISR_Handler){
    //Clear the interrupt request of the ISR DHT_Pin_ISR 
    DHT_Pin_ISR_ClearPending();
    //Clear the interrupt request of the pin DHT_Pin
    DHT_Pin_ClearInterrupt();
    //Read the counter values of Data_Timer for processing
    countvalues_datatimer[risingedge_counts]=Data_Timer_ReadCounter();
    risingedge_counts++;
}
