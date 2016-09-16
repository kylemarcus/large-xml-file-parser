import re
import sys
import argparse

#This program will take as input a properyt ID and
#a xml file to look through. The output is either
#nothing if the property ID is not found or an XML
#file holding the contents of the property ID.

#python xmlparse.py 2082996 hotpads_rentlinx.xml

def main():

    listingID, fileName = parseArgs()

    start = re.compile('<Listing id="' + str(listingID) + '".*')
    end = re.compile('.*Listing>')

    propertyListingfound = False
    propertyListingXML = ''

    with open(fileName, 'r') as f:
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
        with open(str(listingID) + '.xml', 'w') as f:
            f.write(propertyListingXML)
        print("Output file: " + str(listingID) + ".xml")
    else:
        print("Could not find property")

def parseArgs():
    parser = argparse.ArgumentParser()
    addParserArguments(parser)
    args = parser.parse_args()
    return args.listingID, args.fileName

def addParserArguments(parser):
    parser.add_argument("listingID", help="the listing ID you want to search for", type=int)
    parser.add_argument("fileName", help="XML file you want to search")

if __name__ == "__main__":
    main()