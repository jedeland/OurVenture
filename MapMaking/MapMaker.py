# -*- coding: utf-8 -*-
"""
Created on Sun Jan 16 14:55:40 2022

@author: User
"""

from PIL import Image

mapSize = 2048

image = Image.new("RGB", (mapSize,mapSize))

for x in range(0, mapSize//2):
    for y in range(0, mapSize//2):
        image.putpixel((x,y), 150);

image.save("Generated.png");
image.show();