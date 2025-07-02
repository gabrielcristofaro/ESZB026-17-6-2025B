void setup() {
  Serial.begin(115200);
}

void loop() {
  int valor = analogRead(A0);   // Potenciômetro no pino A0
  Serial.println(valor);        // Envia valor por serial
  delay(100);                   // Aguarda 100 ms
}
