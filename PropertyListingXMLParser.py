import re
import sys

#This program will take as input a properyt ID and
#a xml file to look through. The output is either
#nothing if the property ID is not found or an XML
#file holding the contents of the property ID.

#python xmlparse.py 2082996 hotpads_rentlinx.xml

if len(sys.argv) < 3:
    print('Usage: ' + sys.argv[0] + ' propertyId fileName')
    sys.exit()

propertyId = sys.argv[1]
filename = sys.argv[2]

start = re.compile('<Listing id="' + propertyId + '".*')
end = re.compile('.*Listing>')

propertyListingfound = False
propertyListingXML = ''

with open(filename, 'r') as f:
    for line in f:
        regex = end if propertyListingfound else start
        result = regex.search(line)
        if result:
            if propertyListingfound:
                propertyListingXML += result.group(0)
                break
            propertyListingfound = True
            propertyListingXML += result.group(0);
            #check if end is in same line
            result = end.search(propertyListingXML)
            if result:
                propertyListingXML = result.group(0)
                break
        elif propertyListingfound:
            propertyListingXML += line

if propertyListingXML:
    with open(propertyId + '.xml', 'w') as f:
        f.write(propertyListingXML)
    print("Output file: " + propertyId + ".xml")
else:
    print("Could not find property")
