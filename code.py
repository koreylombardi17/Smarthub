import board
import audiomp3
import audiobusio
import busio
import time
import neopixel

# Used for recieving data
uart = busio.UART(board.GP0, board.GP1, baudrate=9600)

# Audio playback variables
audio = audiobusio.I2SOut(board.GP27, board.GP28, board.GP26)
mp3 = audiomp3.MP3Decoder(open("2.mp3", "rb"))

# RGB LED variables
RED = (255, 0, 0)
BLUE = (0, 0, 255)
pixel_pin = board.GP16
num_pixels = 60
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.5, auto_write=False)

def play_audio():
    audio.play(mp3)
    while audio.playing:
        pass
    print("Done playing!")

def leds_on(color):
    pixels.fill(color)
    pixels.show()

# Initial state is Blue LED's on 
leds_on(BLUE)

while True:
    data = uart.read(1)  # read up to 32 bytes
    if data is not None:
        # convert bytearray to string
        status = ''.join([chr(b) for b in data])
        print(status)
        if status == '1':
            print("Audio Playback")
            play_audio()
            status = 0
        elif status == '2':
            print("Red LED's on")
            leds_on(RED)
            time.sleep(10)
            leds_on(BLUE)
            status = 0
        elif status == '3':
            print("Red LED's on")
            leds_on(RED)
            print("Audio Playback")
            play_audio()
            leds_on(BLUE)
            status = 0
