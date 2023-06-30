from machine import Pin, SoftSPI, I2C
from sx127x import SX127x
from time import sleep
import ssd1306

rst = Pin(16, Pin.OUT)
rst.value(1)
scl = Pin(15, Pin.OUT, Pin.PULL_UP)
sda = Pin(4, Pin.OUT, Pin.PULL_UP)
i2c = I2C(scl=scl, sda=sda, freq=450000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3c)

oled.fill(0)
oled.text('Display ok', 0, 0, 1)
oled.show()
sleep(5)
oled.show()
#oled.poweroff()

lora_parameters = {
    'frequency': 433E6, 
    'tx_power_level': 2, 
    'signal_bandwidth': 250E3,    
    'spreading_factor': 12, 
    'coding_rate': 4, 
    'preamble_length': 6,
    'implicit_header': False, 
    'sync_word': 0x12, 
    'enable_CRC': False,
    'invert_IQ': False,
}

device_config = {
    'miso':19,
    'mosi':27,
    'ss':18,
    'sck':5,
    'dio_0':26,
    'reset':14,     
}

device_spi = SoftSPI(baudrate = 10000000, 
        polarity = 0, phase = 0, bits = 8, firstbit = SoftSPI.MSB,
        sck = Pin(device_config['sck'], Pin.OUT, Pin.PULL_DOWN),
        mosi = Pin(device_config['mosi'], Pin.OUT, Pin.PULL_UP),
        miso = Pin(device_config['miso'], Pin.IN, Pin.PULL_UP))

lora = SX127x(device_spi, pins=device_config, parameters=lora_parameters)


counter = 0
print("LoRa Sender")

while True:
    payload = 'Hello ({0})'.format(counter)
    print("Sending packet: \n{}\n".format(payload))
    lora.println(payload)
       
    oled.fill(0)
    oled.text("Sending packet: ", 0, 0, 1)
    oled.text("{}".format(payload), 0, 30, 1)
    oled.show()
        

    counter += 1
    sleep(5)
