//Used to get the temperature and humidity    
#ifndef TEMPERATURE_AND_HUMIDITY_SENSOR_H_
#define TEMPERATURE_AND_HUMIDITY_SENSOR_H_

#include <stdint.h>
    
    
//Initilize everything needed
void dht_init();

//Takes in a new sample of the humidity/temp.
//Will have temp and humidity ready to be returned.
void dht_start();

//Function that will return the temperature after it
//is loaded up
uint8_t dht_get_temperature();

//Function that will return the humidity after it
//is loaded up
uint8_t dht_get_humidity();
    
#endif //TEMPERATURE_AND_HUMIDITY_SENSOR_H_