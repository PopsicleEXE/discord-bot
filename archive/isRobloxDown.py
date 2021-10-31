from pygame import mixer 
from requests import get
from time import sleep as wait

while True:
    response = get('https://api.roblox.com/docs')
    if response.content.decode().find("https://images.rbxcdn.com/6ef6e892aea640c3b1f79f0f820caca5") == -1:
        mixer.init()
        mixer.music.load('sound.mp3')
        mixer.music.play()
    wait(5)
