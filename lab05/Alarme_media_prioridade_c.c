/** Programa baseado no codigo disponibilizado em:
* Derek Molloy, Exploring Raspberry Pi: Interfacing to the Real World with Embedded Linux,
* Wiley 2016, ISBN 978-1-119-1868-1, http://www.exploringrpi.com/
*/

// Ajustando o PWM por HARDWARE na Raspberry Pi

#include <stdio.h>
#include <wiringPi.h>

#define pino_PWM0 18                    // o PWM sera acionado na GPIO18

int main() {                            // este programa deve ser rodado com 'sudo'
   int dc, ciclos;
   wiringPiSetupGpio();                 // usa a numeracao da GPIO
   pinMode(pino_PWM0, PWM_OUTPUT);      // configura a GPIO18 com o PWM por hardware

   // Ajustando a frequencia do PWM em 10kHz com 128 passos de duty cycle
   // frequencia PWM = 19,2 MHz / (divisor * range)
   // 10000 = 19200000 / (divisor * 128) => divisor = 15
   pwmSetMode(PWM_MODE_MS);             // usando frequencia fixa
   pwmSetRange(2048);                    // passos do duty cycle (max=4096)
   pwmSetClock(36);                     // fornece uma frequencia de 10kHz (max=4096)
   printf("Alarme média prioridade\n");
   
   for(ciclos = 0; ciclos < 3; ciclos++){  
      
         pwmWrite(pino_PWM0, 1024);
         usleep(500000);
         pwmWrite(pino_PWM0, 0);
         usleep(500000);
      
   }
   return 0;                            // a saida PWM permanece ligada apos o termino do programa
}
