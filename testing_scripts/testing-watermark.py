from PIL import Image

size_w = 231
size_h = 92

# load watermark
img_watermark = Image.open('Logo_MMFCB.png')
img_orig = Image.open('MeMyselfAndI.jpg')

# Calculations
img_w, img_h = img_orig.size

def_w = (img_w - 35) - size_w
def_h = (img_h - 35) - size_h

img_orig.paste(img_watermark, (def_w,def_h),img_watermark)


#out = Image.alpha_composite(img_orig)
img_orig.save('NewWater.jpg')
img_orig.show()
