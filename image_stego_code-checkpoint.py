import cv2
import hashlib
import os
d = {chr(i): i for i in range(255)}
c = {i: chr(i) for i in range(255)}

# Reading the image
x = cv2.imread(r"C:\Users\divya\Downloads\cover_image.jpg")
i, j, k = x.shape
print(i, j, k)

# Input security key and text to hide
key = input("\nEnter Security Key: ")
text = input("\nEnter text to hide:")

# Initialize variables
k1 = 0
n, m, z = 0, 0, 0
l = len(text)

# Encode text into the image
for i in range(l):
    x[n, m, z] = d[text[i]] ^ d[key[k1]]
    z = (z + 1) % 3
    if z == 0:
        m = (m + 1) % j
        if m == 0:
            n = (n + 1) % i
    k1 = (k1 + 1) % len(key)

# Save the encrypted image
cv2.imwrite("encrypted_img.jpg", x)
os.startfile("encrypted_img.jpg")
print("Data encrypted successfully.")

# Initialize variables for decoding
k1 = 0
n, m, z = 0, 0, 0

# Prompt to unhide text
ch = int(input("\nEnter 0 To Unhide The Text: "))
if ch == 0:
    key_input = input("\nEnter Secret key To Unhide The Text: ")
    decrypt = ""
    if key == key_input:
        for i in range(l):
            decrypt += c[x[n, m, z] ^ d[key[k1]]]
            z = (z + 1) % 3
            if z == 0:
                m = (m + 1) % j
                if m == 0:
                    n = (n + 1) % i
            k1 = (k1 + 1) % len(key)
        print("Hidden Message is:", decrypt)
    else:
        print("KEY MISMATCH!!!")
else:
    print("EXITING!!!")