def bright(image, brightnessFactor):
#     im = Image.open(image)   
#     out = Image.new('RGB', im.size, 0xffffff)
#     def boundedPixelValue(color, brightnessFactor):
#         scaledValue = float(color * (1 + brightnessFactor))
#         if scaledValue < 0:
#             return 0
#         elif scaledValue > 255:
#             return 255
#         return int(scaledValue)
    
#     width, height = im.size
#     for x in range(width):
#         for y in range(height):
#             r,g,b = im.getpixel((x,y))
#             updatedR = boundedPixelValue(r, brightnessFactor)
#             updatedG = boundedPixelValue(g, brightnessFactor)
#             updatedB = boundedPixelValue(b, brightnessFactor)
#             out.putpixel((x,y), (updatedR, updatedG, updatedB))
#     return np.asarray(out,np.uint8)
