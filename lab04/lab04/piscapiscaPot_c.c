#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <termios.h>
#include <string.h>
#include <stdlib.h>
#include <wiringPi.h>
#include <softPwm.h>

int main() {
    int file, count;
    char receive[100];
    int valor_AD, brilho;
    int pino_PWM = 23;
    int range = 100;

    // Inicializa WiringPi e PWM por software
    wiringPiSetupGpio();                   
    pinMode(pino_PWM, OUTPUT);
    softPwmCreate(pino_PWM, 0, range);     

    // Abre a porta serial
    if ((file = open("/dev/ttyACM0", O_RDWR | O_NOCTTY | O_NDELAY)) < 0) {
        perror("UART: Falha ao abrir o arquivo.\n");
        return -1;
    }

    // Configura a serial
    struct termios options;
    tcgetattr(file, &options);
    options.c_cflag = B115200 | CS8 | CREAD | CLOCAL;
    options.c_iflag = IGNPAR | ICRNL;
    tcflush(file, TCIFLUSH);
    tcsetattr(file, TCSANOW, &options);

    // Loop infinito para ler valor e aplicar brilho
    while (1) {
        memset(receive, 0, sizeof(receive)); // limpa o buffer de recepção

        // Leitura da serial
        count = read(file, (void*)receive, sizeof(receive));
        if (count > 0) {
            valor_AD = atoi(receive);  // converte string para inteiro

            // Converte de 0–1023 para 0–100 (porcentagem do brilho)
            if (valor_AD > 1023) valor_AD = 1023;
            if (valor_AD < 0) valor_AD = 0;
            brilho = (valor_AD * 100) / 1023;

            // Aplica valor PWM
            softPwmWrite(pino_PWM, brilho);

            // Imprime valor para debug
            printf("AD: %d | Brilho: %d%%\n", valor_AD, brilho);
        } else {
            printf("Sem leitura da serial...\n");
        }

        usleep(100000); // espera 100 ms antes da próxima leitura
    }

    close(file);
    return 0;
}
