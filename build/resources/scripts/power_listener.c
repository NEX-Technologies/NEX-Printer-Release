#include <wiringPi.h>
#include <stdlib.h>
#include <stdio.h>

int main (void)
{

    printf("Program started.");

    int board_pin = 26;
    int hold_delay = 3000;
    int curr_delay = 0;
    
    wiringPiSetupPhys();
    pinMode(board_pin, INPUT);
    pullUpDnControl(board_pin, PUD_DOWN) ;

    while(1)
    {
        if(digitalRead(board_pin == 1))
        {
           curr_delay += 1000;

           if(curr_delay == hold_delay)
           {
               break;
           }

           printf("Holding...");
        }
        else
        {
            curr_delay = 0;

            printf("Not holding...");
        }

        delay(1000);
    }

    system("sudo shutdown now");

    return 0;
}
