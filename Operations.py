from PIL import Image
import numpy as np
import cv2


#Adjust Brightness

def brightness(image, brightness_factor):
    b, g, r = cv2.split(image)

    b = cv2.add(b, 255 * brightness_factor)
    g = cv2.add(g, 255 * brightness_factor)
    r = cv2.add(r, 255 * brightness_factor)

    b = np.clip(b, 0, 255)
    g = np.clip(g, 0, 255)
    r = np.clip(r, 0, 255)

    adjusted_image = cv2.merge((b, g, r))
    return np.asarray(adjusted_image, np.uint8)


# Adjust Contrast

def color_contrast(image, amount):
    # Split the image into RGB channels
    b, g, r = cv2.split(image)

    # Apply contrast adjustment to each channel
    b = np.clip(b * amount, 0, 255).astype(np.uint8)
    g = np.clip(g * amount, 0, 255).astype(np.uint8)
    r = np.clip(r * amount, 0, 255).astype(np.uint8)

    # Merge the RGB channels back into an image
    contrast_image = cv2.merge((b, g, r))
    return np.asarray(contrast_image, np.uint8)


# Sharpening

def color_sharpening(image, amount):
    # Convert image to LAB color space
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    # Split LAB channels
    l, a, b = cv2.split(lab)
    # Apply unsharp masking to the L channel
    blurred_l = cv2.GaussianBlur(l, (0, 0), 3)
    sharp_l = cv2.addWeighted(l, 1 + amount, blurred_l, -amount, 0)
    # Merge LAB channels back to LAB image
    lab_sharp = cv2.merge((sharp_l, a, b))
    # Convert LAB image back to BGR
    sharp_image = cv2.cvtColor(lab_sharp, cv2.COLOR_LAB2BGR)
    # Clip pixel values to 0-255
    sharp_image = np.clip(sharp_image, 0, 255).astype(np.uint8)
    return np.asarray(sharp_image, np.uint8)

