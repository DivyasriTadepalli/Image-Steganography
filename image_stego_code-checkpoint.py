from PIL import Image

def text_to_bin(text):
    bin_str=""
    for char in text:
        ascii_value=ord(char)
        bin_char=format(ascii_value,'08b')
        bin_str+=bin_char
    return bin_str
    
def bin_to_text(binary):
    text=""
    for i in range(0,len(binary),8):
        byte=binary[i:i+8]
        decimal_value=int(byte,2)
        character=chr(decimal_value)
        text+=character
    return text
    
    
def encoding(img_path,msg,key,output_path):
    img=Image.open(img_path)
    if img.mode!='RGB':
        img=img.convert('RGB')
    
    pixels=img.load()   #loading the pixels of an image 
    
    main_msg=key+":"+msg+"||END||"  #combining secret key & message
    
    bin_msg=text_to_bin(main_msg)  #coverting message to binary
    
    index=0   #index to show position in bin_msg
    
    #to iterate over each pixel of the image
    for y in range(img.height):      
        for x in range(img.width):
            r,g,b=pixels[x,y]
            #red channel
            if index<len(bin_msg):
                bit=int(bin_msg[index])
                #setting LSB of r to 0 using bitwise AND operation & the LSB of r to the value of bit using bitwise OR
                r=(r&~1)|bit 
                index+=1
                
            #green channel
            if index<len(bin_msg):
                bit=int(bin_msg[index])
                g=(g&~1)|bit 
                index+=1
                
            #blue channel
            if index<len(bin_msg):
                bit=int(bin_msg[index])
                b=(b&~1)|bit 
                index+=1
                
            pixels[x,y]=(r,g,b)   #updating pixels with new rgb values
            
    img.save(output_path)
    print("Message encoded and saved at",output_path)
    
    
def decoding(img_path,key):
    img=Image.open(img_path)
    pixels=img.load()   #loading the pixels of an image
    bin_data=""
     
    #extracting LSB bits from each channel
    for y in range(img.height):
        for x in range(img.width):
            r,g,b=pixels[x,y]
            r1=str(r&1)  #extracting LSB of red channel
            g1=str(g&1)  #extracting LSB of red channel
            b1=str(b&1)  #extracting LSB of red channel
            bin_data+=r1+g1+b1
             
    out_msg=bin_to_text(bin_data)
    if "||END||" in out_msg:
        extracted=out_msg.split("||END||")[0]
        if ":" not in extracted:
            return "Message format corruted."
        decoded_key,secret_msg=extracted.split(":",1)

        if decoded_key==key:
            return (secret_msg)
        else:
            return "Invalid secret key!"
    else:
        return "No valid message found."
        
#taking input from user       
def main():
    mode=input("Mode(encode/decode):").strip()
    mode=mode.lower()
     
    if mode=="encode":
        img_path=input("Enter input image path in .png format:").strip()
        msg=input("Enter secret message:").strip()
        key=input("Enter secret key:").strip()
        output_path=input("Enter output file name:").strip()
        encoding(img_path,msg,key,output_path)
         
    elif mode=="decode":
        img_path=input("Enter encoded image path in .png format:").strip()
        key=input("Enter secret key:").strip()
        print(decoding(img_path,key))
         
main()   
     
