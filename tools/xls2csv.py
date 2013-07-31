# -*- coding:utf-8 -*-

# Author : JEANNENOT Stephane
# Mail : stephane.jeannenot@gmail.com

# Modified by : Rich Alesi
# rich.alesi@gmail.com
#
# History
# + 10 january 2008
#        --> Version : 0.1 : first try of creating a program that feets my objectives : convert
#              easily xls sheets into csv with my favorite language ;)
# + 24 may 2009
#        --> Version : 0.2
#        --> changed license from LGPL3 to simplified BSD
#        --> parsing arguments with optparse module
#        --> options added : remove lines or columns in the destination file
# + 16 september 2009
#        --> Version : 0.3
#        --> added remove option for lines and colums with negative indexes
# + 26 september 2009
#        --> Version : 0.4
#        --> added double-quoted cellvalue option
#            (contribution submitted by Mintaka : mintaka@email.cz)
# + 20 april 2011
#        --> Version : 0.5
#        --> allow output to stdout
## Copyright (c) 2008-2009, JEANNENOT Stephane
## All rights reserved.
##
## Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are met:
##
##    1 Redistributions of source code must retain the above copyright notice,
##      this list of conditions and the following disclaimer.
##    2 Redistributions in binary form must reproduce the above copyright
##      notice, this list of conditions and the following disclaimer in the
##      documentation and/or other materials provided with the distribution.
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
## AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
## IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
## ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
## LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
## CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
## SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
## INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
## CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
## ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
## THE POSSIBILITY OF SUCH DAMAGE.


import os
import sys
import warnings
import datetime
import codecs

from optparse import OptionParser

try:
    import xlrd
except ImportError:
    print("\n-----------------------------------------------------------")
    print("   The module xlrd is necessary to run this script.")
    print("   It is available here : http://pypi.python.org/pypi/xlrd")
    print("-----------------------------------------------------------\n")
    sys.exit(1)

def convertFactory(options, wSheet):
    widths = [i for i in rowWidths(options, wSheet)]
    #print widths
    for numRow in xrange(wSheet.nrows):
        if(numRow not in options.remrows):
            liste = []
            column_order = 0
            for numCol in xrange(wSheet.ncols):
                if(numCol not in options.remcols):
                    cellType = wSheet.cell_type(numRow,numCol)
                    cellValue = wSheet.cell_value(numRow,numCol)
                    if((options.colasint == "all") or (cellType == xlrd.XL_CELL_BOOLEAN) or (cellType == xlrd.XL_CELL_NUMBER and numCol in options.colasint )):
                        try:
                            liste.append(str(int(cellValue)))
                        except ValueError, error:
                            liste.append(cellValue)
                            #~ warnings.warn("Bad cell format : gets string, expects number", stacklevel=2)
                    elif(cellType == xlrd.XL_CELL_NUMBER ):
                        liste.append(str(cellValue))
                    elif(cellType == xlrd.XL_CELL_DATE ):
                        # trying to handle dates - maybe buggy at this time !
                        # by default, datemode is 1900-based
                        datemode = 0 # 1900-based
                        # datemode = 1 # 1904-based
                        tp = xlrd.xldate_as_tuple(cellValue,0)
                        mydate = datetime.datetime( tp[0], tp[1], tp[2], tp[3], tp[4], tp[5] )
                        # return isoformat (may be improved in the future)
                        liste.append(mydate.isoformat())
                    else:
                        # conversion for latin-1 : really needed ??
                        if(options.encloseText):
                            liste.append("\"%s\""%(cellValue))
                        else:
                            liste.append(cellValue)
                    if options.delimit == True:
                        liste[-1] = str.rjust(str(liste[-1]),
                                    widths[column_order]+1 )
                        column_order += 1

            yield liste

def rowWidths(options, wSheet):
    widths = []
    for numCol in xrange(wSheet.ncols):
        if(numCol not in options.remcols):
            for numRow in xrange(wSheet.nrows):
                if(numRow not in options.remrows):
                    cellType = wSheet.cell_type(numRow,numCol)
                    cellValue = wSheet.cell_value(numRow,numCol)
                    if((options.colasint == "all") or (cellType == xlrd.XL_CELL_BOOLEAN) or (cellType == xlrd.XL_CELL_NUMBER and numCol in options.colasint )):
                        try:
                            widths.append(str(int(cellValue)))
                        except ValueError, error:
                            widths.append(cellValue)
                            #~ warnings.warn("Bad cell format : gets string, expects number", stacklevel=2)
                    elif(cellType == xlrd.XL_CELL_NUMBER ):
                        widths.append(str(cellValue))
                    elif(cellType == xlrd.XL_CELL_DATE ):
                        # trying to handle dates - maybe buggy at this time !
                        # by default, datemode is 1900-based
                        datemode = 0 # 1900-based
                        # datemode = 1 # 1904-based
                        tp = xlrd.xldate_as_tuple(cellValue,0)
                        mydate = datetime.datetime( tp[0], tp[1], tp[2], tp[3], tp[4], tp[5] )
                        # return isoformat (may be improved in the future)
                        widths.append(mydate.isoformat())
                    else:
                        # conversion for latin-1 : really needed ??
                        if(options.encloseText):
                            widths.append("\"%s\""%(cellValue))
                        else:
                            widths.append(cellValue)
            yield max([len(i) for i in widths])


def manageOptions(options):
    if(options.verbose):
        print("\nOptions given to the conversion function :")
        print("... input filename = %s" % options.ifname)
        print("... output filename = %s" % options.ofname)
        print("... sheet to convert = %d" % options.numsheet)
        print("... separator = %s" % options.separator)
        print("... override input encoding = %s" % options.inputEncoding)
        print("... columns containing integers = %s" % options.colasint)
        print("... removing rows = %s" % options.remrows)
        print("... removing columns = %s" % options.remcols)
        print("... print statistics = %s" % options.stats)
        print("... set output encoding = %s" % options.outputEncoding)
        print("... set output lineend = %s" % options.lineend)

    if(options.colasint):
        if(not options.colasint == "all"):
            options.colasint = set([int(x) for x in options.colasint.split(':')])
    else:
        options.colasint = set()

    if(options.remrows):
        options.remrows = set([int(x) for x in options.remrows.split(':')])
    else:
        options.remrows = set()

    if(options.remcols):
        options.remcols = set([int(x) for x in options.remcols.split(':')])
    else:
        options.remcols = set()

    if(options.lineend not in ["CRLF","LF"]):
        options.lineend = "LF"

    return options

def convert2csv(options):
    options = manageOptions(options)
    WIN32 = True if (sys.platform == 'win32') else False
    if(options.lineend == "LF"):
        NIX = True
    else:
        NIX = False

    # Open input file
    if(options.inputEncoding):
        book = xlrd.open_workbook(filename=options.ifname, encoding_override=options.inputEncoding)
    else:
        book = xlrd.open_workbook(filename=options.ifname)


    # Statistics
    nSheets = book.nsheets
    if(options.stats):
        print("\nStatistics of input Excel file :")
        print("... sheets found = %d" % nSheets)
        print("... encoding = %s" % book.encoding)

    if(options.numsheet >= nSheets or options.numsheet < 0):
        raise ValueError

    # Select working sheet
    wSheet = book.sheet_by_index(options.numsheet)
    if(options.stats):
        print("\nStatistics of sheet #%d" % options.numsheet)
        print("... sheet name = %s" % wSheet.name)
        print("... number of rows = %d" % wSheet.nrows)
        print("... number of columns = %d" % wSheet.ncols)

    # Handle negative indexes for removing rows and colums
    for item in options.remrows:
        if(item<0):
            options.remrows.remove(item)
            options.remrows.add(wSheet.nrows+item)
    for item in options.remcols:
        if(item<0):
            options.remcols.remove(item)
            options.remcols.add(wSheet.ncols+item)

    # Open output file
    if options.ofname == '-':
        print_out = '' 
        for data in convertFactory(options,wSheet):
            print_out += (options.separator).join(data)
            if(NIX):
                print_out += "\n"
            else:
                print_out += "\r\n"
        print print_out

    else:
        outfile = codecs.open(options.ofname, 'w', encoding=options.outputEncoding)

        for data in convertFactory(options,wSheet):
            outfile.write((options.separator).join(data))
            if(NIX):
                outfile.write("\n")
            else:
                outfile.write("\r\n")

        outfile.close()



def main():
    if(sys.version_info[0] > 2):
        print("Found Python interpreter : %s\n"%sys.version)
        print("This script works only with Python version up to 2.x *but* not with an above version (xlrd module limitation)")
        sys.exit(1)
    else:
        parser = OptionParser(usage="%prog -i <IFNAME> -o <OFNAME>", version="%prog 0.3")
        parser.add_option("-i", "--input", dest="ifname",
                            help="input Excel filename")
        parser.add_option("-o", "--output", dest="ofname",
                            help="output CSV filename")
        parser.add_option("-s", "--sheet", dest="numsheet", type="int", default=0,
                            help="sheet number to convert (1st sheet is numbered '0', so it's 0 by default)")
        parser.add_option("-d", "--delim", action="store_true", dest="delimit", default=False,
                            help="use spaces to delimit columns")
        parser.add_option("-p", "--sep", dest="separator", default=";",
                            help="separator used in the csv file (';' as Excel default conversion character)")
        parser.add_option("-e", "--enclose-text", action="store_true", dest="encloseText", default=False,
                            help="enclose text values into double-quote characters")
        parser.add_option("--input-encoding", dest="inputEncoding",
                            help="override the input file encoding (useful for excel 95 and earlier versions)")
        parser.add_option("--output-encoding", dest="outputEncoding", default="utf-8",
                            help="set the output file encoding (utf-8 by default)")
        parser.add_option("--col-as-int", dest="colasint",
                            help="give column numbers as a list with ':' as separator, like 1:25:41 or 'all' for converting all colums \
                            For these columns, if the cell contains a number, it will be considered as an integer")
        parser.add_option("--remove-rows", dest="remrows",
                            help="give row numbers to remove as a list with ':' as separator, like 2:3:56")
        parser.add_option("--remove-cols", dest="remcols",
                            help="give column numbers to remove as a list with ':' as separator, like 6:89:7")
        parser.add_option("--lineend", dest="lineend", default="LF",
                            help="character for line ending : CRLF (windows) or LF (unix) default")
        parser.add_option("--stats", action="store_true", dest="stats", default=False,
                            help="print statistics about the Excel file")
        parser.add_option("-v", "--verbose",
                          action="store_true", dest="verbose", default=False,
                          help="don't print status messages to stdout")

        (options, args) = parser.parse_args()

        if( (not options.ifname) or (not options.ofname) ):
            parser.error("options -i and -o are mandatory")

        convert2csv(options)

if __name__ == "__main__":
    main()
