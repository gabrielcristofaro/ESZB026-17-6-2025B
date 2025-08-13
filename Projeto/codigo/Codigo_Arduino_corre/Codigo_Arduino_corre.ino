// Frequencia de amostragem desejada, em Hz:
long frequencia = 120;

// Constantes necessárias para o filtro notch
#define N_PONTOS 2
#define N 1
#define a 0.05

unsigned long atraso_us = (1000000.0 / frequencia);
int X[N_PONTOS];   // vetor com as medidas atuais
int Y[N_PONTOS];   // vetor com as medidas filtradas
unsigned long tempo_atual, tempo_anterior;
int contador;

/////////////////////////////////////////////////////////////////
// Esta função só roda uma vez, no início
void setup() {
  Serial.begin(115200);
  pinMode(4, INPUT); 
  pinMode(5, INPUT);
  pinMode(LED_BUILTIN, OUTPUT);
  tempo_anterior = micros();
  contador = 0;
}

/////////////////////////////////////////////////////////////////
// Esta função se repete indefinidamente
void loop() {
  // ==== TRATA COMANDOS VINDOS DO PYTHON ====
  if (Serial.available()) {
    char cmd = Serial.read();

    if (cmd == 'I') {
      // Envia intervalo em milissegundos
      Serial.println((float)atraso_us / 1000.0, 2);
    }
    else if (cmd == 'A') {
      // Aumenta taxa → diminui atraso
      if (atraso_us > 1000) atraso_us -= 1000;
    }
    else if (cmd == 'D') {
      // Diminui taxa → aumenta atraso
      atraso_us += 1000;
    }
  }

  // ==== AQUISIÇÃO DO SINAL ====
  tempo_atual = micros();

  if ((digitalRead(4) == 1) || (digitalRead(5) == 1)) {
    digitalWrite(LED_BUILTIN, HIGH);
  }
  else {
    if (digitalRead(LED_BUILTIN) == 1) { // se está aceso, apaga
      digitalWrite(LED_BUILTIN, LOW);
    }

    // o abs() evita problemas com overflow da função micros()
    if (abs((long)(tempo_atual - tempo_anterior)) > (long)atraso_us) {
      tempo_anterior = tempo_atual;

      X[contador] = analogRead(A0); // realiza medida atual
      int ponto_anterior = (contador + N_PONTOS - N) % N_PONTOS;

      Y[contador] = ((X[contador] + X[ponto_anterior]) / 2) +
                    a * (((X[contador] + X[ponto_anterior]) / 2) - Y[ponto_anterior]);

      Serial.println(Y[contador]);

      contador++;
      if (contador >= N_PONTOS) {
        contador = 0;
      }
    }
  }
}
