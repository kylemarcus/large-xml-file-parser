import re
import sys
import argparse

# This program will take as input a listing ID and
# a xml file to look through. The output is either
# nothing if the listing ID is not found or an XML
# file holding the contents of the listing ID.

# The parsing of the XML was done this way because
# regular XML parsing was too slow for very large
# files (>500mb). By parsing just the specific text
# it is much faster.

# python xmlparse.py 123 listings.xml

def main():

    listingID, fileName = parseArgs()

    specificListingXML = parseFileForListingId(listingID, fileName)

    if specificListingXML:
        writeOutputToFile(listingID, specificListingXML)
    else:
        print("Could not find listing " + str(listingID) + " in " + fileName)

def parseArgs():
    parser = argparse.ArgumentParser()
    addParserArguments(parser)
    args = parser.parse_args()
    return args.listingID, args.fileName

def addParserArguments(parser):
    parser.add_argument("listingID", help="the listing ID you want to search for", type=int)
    parser.add_argument("fileName", help="XML file you want to search")

def parseFileForListingId(listingID, fileName):
    beginListingRegEx, endListingRegEx = compileBeginAndEndListingRegEx(listingID)
    currentRegEx = beginListingRegEx
    specificListingXML = ''

    with open(fileName, 'r') as fileToParse:
        for line in fileToParse:
            regExResult = currentRegEx.search(line)
            if regExResult:
                if specificListingXML:
                    specificListingXML += regExResult.group(0)
                    break
                currentRegEx = endListingRegEx
                specificListingXML += regExResult.group(0);
                regExResult = endListingRegEx.search(specificListingXML)
                if regExResult: # check if end is in same line
                    specificListingXML = regExResult.group(0)
                    break
            elif specificListingXML:
                specificListingXML += line

    return specificListingXML

def compileBeginAndEndListingRegEx(id):
    beginListingRegEx = re.compile('<Listing id="' + str(id) + '".*')
    endListingRegEx = re.compile('.*Listing>')
    return beginListingRegEx, endListingRegEx

def writeOutputToFile(listingID, specificListingXML):
    outputFileName = str(listingID) + '.xml'
    with open(outputFileName, 'w') as outputFile:
        outputFile.write(specificListingXML)
    print("Found listing " + str(listingID) + ", output file: " + outputFileName)

if __name__ == "__main__":
    main()