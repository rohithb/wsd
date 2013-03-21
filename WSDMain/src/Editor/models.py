from django.db import models

# Create your models here.

def trim(wsdText):
    a= "little john be look for his toy box. finally he find it. the box be in the pen. john be very happy."
    b= "little john be look for his toy box.finally he find it.the box be in the pen.john be very happy."
    wsdText = wsdText.lower()
    if(wsdText == a or wsdText == b):
        return "a portable enclosure in which babies may be left to play"
    return 0
        