echo meu programa!
echo olá

echo  Abertura Pino "16"

echo 16 >> "/sys/class/gpio/export"
sleep 1
echo "out" >> "/sys/class/gpio/gpio16/direction"

echo 1 >> "/sys/class/gpio/gpio16/value"
sleep 1
echo 0 >> "/sys/class/gpio/gpio16/value"
sleep 1

echo 1 >> "/sys/class/gpio/gpio16/value"
sleep 1
echo 0 >> "/sys/class/gpio/gpio16/value"
sleep 1

echo 1 >> "/sys/class/gpio/gpio16/value"
sleep 1
echo 0 >> "/sys/class/gpio/gpio16/value"
sleep 1

echo 1 >> "/sys/class/gpio/gpio16/value"
sleep 1
echo 0 >> "/sys/class/gpio/gpio16/value"
sleep 1

echo 1 >> "/sys/class/gpio/gpio16/value"
sleep 1
echo 0 >> "/sys/class/gpio/gpio16/value"
sleep 1


echo 16 >> "/sys/class/gpio/unexport"

echo  Abertura Pino "20"

echo 20 >> "/sys/class/gpio/export"
sleep 1
echo "out" >> "/sys/class/gpio/gpio20/direction"

echo 1 >> "/sys/class/gpio/gpio20/value"
sleep 2
echo 0 >> "/sys/class/gpio/gpio20/value"
sleep 2

echo 1 >> "/sys/class/gpio/gpio20/value"
sleep 2
echo 0 >> "/sys/class/gpio/gpio20/value"
sleep 2

echo 1 >> "/sys/class/gpio/gpio20/value"
sleep 2
echo 0 >> "/sys/class/gpio/gpio20/value"
sleep 2

echo 1 >> "/sys/class/gpio/gpio20/value"
sleep 2
echo 0 >> "/sys/class/gpio/gpio20/value"
sleep 2

echo 1 >> "/sys/class/gpio/gpio20/value"
sleep 2
echo 0 >> "/sys/class/gpio/gpio20/value"
sleep 2

echo 20 >> "/sys/class/gpio/unexport"


echo  Abertura Pino "21"

echo 21 >> "/sys/class/gpio/export"
sleep 1
echo "out" >> "/sys/class/gpio/gpio21/direction"

echo 1 >> "/sys/class/gpio/gpio21/value"
sleep 1
echo 0 >> "/sys/class/gpio/gpio21/value"
sleep 1

echo 1 >> "/sys/class/gpio/gpio21/value"
sleep 1
echo 0 >> "/sys/class/gpio/gpio21/value"
sleep 1

echo 1 >> "/sys/class/gpio/gpio21/value"
sleep 1
echo 0 >> "/sys/class/gpio/gpio21/value"
sleep 1

echo 1 >> "/sys/class/gpio/gpio21/value"
sleep 1
echo 0 >> "/sys/class/gpio/gpio21/value"
sleep 1

echo 1 >> "/sys/class/gpio/gpio21/value"
sleep 1
echo 0 >> "/sys/class/gpio/gpio21/value"
sleep 1


echo 21 >> "/sys/class/gpio/unexport"
