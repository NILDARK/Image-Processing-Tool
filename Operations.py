import numpy as np
import cv2


#Adjust Brightness

def color_brightness(image, brightness_factor):
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
    b, g, r = cv2.split(image)      # Split the image into RGB channels

    # Apply contrast adjustment to each channel
    b = np.clip(b * amount, 0, 255).astype(np.uint8)
    g = np.clip(g * amount, 0, 255).astype(np.uint8)
    r = np.clip(r * amount, 0, 255).astype(np.uint8)

    contrast_image = cv2.merge((b, g, r))       # Merge the RGB channels back into an image

    return np.asarray(contrast_image, np.uint8)


# Adjust Sharpening

def color_sharpening(image, amount):
    b, g, r = cv2.split(image)

    blurred_b = cv2.GaussianBlur(b, (0, 0), 3)
    sharp_b = cv2.addWeighted(b, 1 + amount, blurred_b, -amount, 0)

    blurred_g = cv2.GaussianBlur(g, (0, 0), 3)
    sharp_g = cv2.addWeighted(g, 1 + amount, blurred_g, -amount, 0)

    blurred_r = cv2.GaussianBlur(r, (0, 0), 3)
    sharp_r = cv2.addWeighted(r, 1 + amount, blurred_r, -amount, 0)

    lab_sharp = cv2.merge((sharp_b, sharp_g, sharp_r))

    return lab_sharp


#Adjust Blurring

def colour_blurring(image,kernel_size):
    # Split the image into RGB channels
    b, g, r = cv2.split(image)

    b_blur = cv2.GaussianBlur(b, (kernel_size,kernel_size), 0)
    g_blur = cv2.GaussianBlur(g, (kernel_size,kernel_size), 0)
    r_blur = cv2.GaussianBlur(r, (kernel_size,kernel_size), 0)

    # Merge the blurred channels back into an RGB image
    blurred_image = cv2.merge((b_blur, g_blur, r_blur))

    return blurred_image