# large-xml-file-parser

Use this script to search for a specific element tag in a very large XML file.  Some XML viewers are very slow loading when it comes to XML files that are > 500mb so I create this script to extract out just the element you want.

Example: `$python largeXMLFileParser.py '<Listing id="1130"' listings.xml out.xml`
