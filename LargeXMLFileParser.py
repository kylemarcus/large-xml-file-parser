import re
import sys
import argparse
import xml.dom.minidom

'''
This program will take as input a starting XML element
to search for and a xml file to look through along with
a output filename. The output is either nothing if the 
element is not found or an XML file holding the contents 
of the found element.

The parsing of the XML was done this way because regular 
XML parsing was too slow for very large files (>500mb). 
By parsing just the specific text it is much faster.

The search element is pretty specific to the below example
but could easily be modified to look for something else.

python PropertyListingXMLParser.py '<Listing id="1130"' listings.xml out.xml
'''

def main():

    searchElement, inputFilename, outputFilename = parseArgs()

    extractedElement = parseFileForElement(searchElement, inputFilename)

    if extractedElement:
        writeExtractedElementToFile(extractedElement, outputFilename)
    else:
        print("Could not element '" + searchElement + "' in " + inputFilename)
        exit(1)

def parseArgs():
    parser = argparse.ArgumentParser()
    addParserArguments(parser)
    args = parser.parse_args()
    return args.searchElement, args.inputFilename, args.outputFilename

def addParserArguments(parser):
    parser.add_argument("searchElement", help="The starting xml tag to search for")
    parser.add_argument("inputFilename", help="XML file you want to search")
    parser.add_argument("outputFilename", help="output filename")

def parseFileForElement(searchElement, fileName):
    extractedElement = ""
    startSearchStr = searchElement
    endSearchStr = "</" + searchElement.split(" ")[0][1:] + ">"

    with open(fileName, 'r') as fileToParse:
        for line in fileToParse:
            startIndex = line.find(startSearchStr)
            endIndex = line.find(endSearchStr)
            if (startIndex >= 0 and endIndex >= 0): # same line
                extractedElement = line[startIndex:endIndex]
                break
            elif (startIndex >= 0): # start of listing
                extractedElement = line[startIndex:]
            elif (endIndex >= 0 and extractedElement): # end of listing
                extractedElement += line[:endIndex] + endSearchStr
                break;
            elif (extractedElement): # continuation of found line
                extractedElement += line

    return extractedElement

def writeExtractedElementToFile(extractedElement, outputFilename):
    with open(outputFilename, 'w') as outputFile:
        parsedXML = xml.dom.minidom.parseString(extractedElement)
        outputFile.write(parsedXML.toprettyxml())
    print("Found element, output file: " + outputFilename)

if __name__ == "__main__":
    main()