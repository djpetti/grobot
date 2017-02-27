/* ========================================
 *
 * Copyright YOUR COMPANY, THE YEAR
 * All Rights Reserved
 * UNPUBLISHED, LICENSED SOFTWARE.
 *
 * CONFIDENTIAL AND PROPRIETARY INFORMATION
 * WHICH IS THE PROPERTY OF your company.
 *
 * ========================================
*/

#include <project.h>

void delay(void);
void unpackdhtdata(void);

uint8 check = 0;
uint8 decodeFlag=0;
int temperature_values[8], humidity_values[8];

int DiffCountValues[44]={0};
int CountValues_DataTimer[44]={0};

CY_ISR_PROTO(Delay_Timer_ISR_Handler);
CY_ISR_PROTO(DHT_Pin_ISR_Handler);

int executed;
int count;
int RisingEdge_Counts=0;

int i,j,k;
/*
What dhtmain does:
    Starts the dht components
    Get output from dht11
    Send out results

Paramers: None
Returns: None

*/

void dhtmain(){
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
    
    //Initilize count to zero and executed to 1
    
    count = 0;
    executed = 1;
    
    // Enable Global Interrupts
    
    CyGlobalIntEnable;
    
    //This is going to run forever, gonna need to put this somewhere else.
    //Probably in the main.c, but thatis for later 
    //But this will read in the input from the dht11
    
    for(;;)
    {
        
        if(executed == 1 && count == 0)
        {
            executed = 0;
            
            RisingEdge_Counts = 0;
            
            CyDelayUs(50);
            
            DHT_Pin_Write(0);
            
            Delay_Timer_WritePeriod(DELAY_ACQUISITION);
            //Call the delay function to stay the DHT_Pin as low for 20ms 
            delay_funct();
        }    
        
        if(count >= 2 && executed ==0)
        {
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
        
        if(decodeFlag==1)
        {
            Control_Reg_Data_Timer_Write(1);
            DHT_Pin_ISR_Disable(); 
            DHT_Pin_Write(1);   
            decodeFlag=0;
            Decode_DHT_Data();
            executed=1;
            count=0;
        }    
        
        
    }    
    
}    


/*
What delay_funct does:
    - Enable Delay_Timer_ISR to detect Delay_Tiemr Terminal Count interrupt
    - Start the Delay_Timer component.
    - This function does not use the CPU delay API, CyDelay(), but uses Delay_Timer to generate delay. 

Parameters: None
Return: None
*/
void delay_funct(void)
{
    count = 1;
    executed = 0;
    // Enable Delay_timer_ISR
    Delay_Timer_ISR_Enable();
    //Write 0 to Control_Reg_Delay_Timer to starting Delay_Timer component 
    Control_Reg_Delay_Timer_Write(0);
}    

/*
What decode dht data does:
    - The value stored in CountValues_DataTimer[] array, is used to decode the data of DHT output
    - The time difference between CountValues_DataTimer[i] and CountValues_DataTimer[i-1] is calculated
    - If the CountValues_DataTimer[i] is approximately 70 counts, it is data 0, and if CountValues_DataTimer[i] is approximately 120, it is data 1. 

Parameters: None
Returns: None

*/

void Decode_DHT_Data(void)
{
    for(i=0; i<44; i++)
    {
        DiffCountValues[i]=CountValues_DataTimer[i-1]-CountValues_DataTimer[i];
    }    
    for(j=0; j<8; j++)
    {
        if(DiffCountValues[j+3]>100)
        {
            Humidity_Values[7-j]=1;
        }
        else
        {
            Humidity_Values[7-j]=0;
        }
        if(DiffCountValues[j+19]>100)
        {
            Temperature_Values[7-j]=1;
        }
        else
        {
            Temperature_Values[7-j]=0;
        }
    }
    Decoded_Temperature_Data= (uint8)((Temperature_Values[7]<<7) + (Temperature_Values[6]<<6) + (Temperature_Values[5]<<5) + (Temperature_Values[4]<<4) + (Temperature_Values[3] <<3) + (Temperature_Values[2] <<2) + (Temperature_Values[1]<<1) + Temperature_Values[0]);
    Decoded_Humidity_Data=(uint8)((Humidity_Values[7]<<7) + (Humidity_Values[6]<<6) + (Humidity_Values[5]<<5) + (Humidity_Values[4]<<4) + (Humidity_Values[3] <<3) + (Humidity_Values[2] <<2) + (Humidity_Values[1]<<1) + Humidity_Values[0]);
}    

/*
Name: Delay_Timer_ISR_Handler
Summary:
    Interrupt Service Routine. Check the Delay_Timer status and clear the interrupt
    change the Count and Executed status

*/

CY_ISR(Delay_Timer_ISR_Handler)
{
    if(Delay_Timer_ReadPeriod() == DELAY_ACQUISITION)
    {
        cnt=2;                  
        executed=0;             
    }
    else if(Delay_Timer_ReadPeriod() == DELAY_PROCESSING)
    { 
        decodeFlag=1;
    }
    
    //Write 1 to the Contro_Reg_Delay_Timer to disable the Timer function 
    Control_Reg_Delay_Timer_Write(1);
    //Read the status register of Delay_Timer to clear interrupt
    Delay_Timer_ReadStatusRegister();
    //Clear the Delay_Timer_ISR interrupt
    Delay_Timer_ISR_ClearPending();
}    


CY_ISR(DHT_Pin_ISR_Handler)
{
    //Clear the interrupt request of the ISR DHT_Pin_ISR 
    DHT_Pin_ISR_ClearPending();
    //Clear the interrupt request of the pin DHT_Pin
    DHT_Pin_ClearInterrupt();
    //Read the counter values of Data_Timer for processing
    CountValues_DataTimer[RisingEdge_Counts]=Data_Timer_ReadCounter();
    RisingEdge_Counts++;
}    
/* [] END OF FILE */
