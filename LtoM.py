#!/usr/bin/env python3

from __future__ import print_function

__author__ = 'Roman Ammann'
__version__= 0.1

EXIT_OK = 0
EXIT_ERROR = 1

SHEET_E = 0.297   # A4 29.7x21 cm, landscape
SHEET_N = 0.21

SHEET_BORDER = 0.01 # leave a 1cm border around each A4
SHEET_OVERLAP = 0.01 # overlap sheets at least by 1cm

MAP_RESOLUTION = 50000  # 1:50000

COORDINATE_STEP = 1000
COORDINATE_LABEL_OFFSET = 10 # offset from the coordiante line to the label

DPI = 300 # resolution of the map 300 dots/inch
M_PER_INCH = 0.0254 # 0.0254 m = 1 inch
DPM_MAP = (DPI / M_PER_INCH) # dots in the map per  m
DPM_REAL = (DPI / M_PER_INCH) / MAP_RESOLUTION # dots in the map per real m

DECLINATION_POINT_X = 0.25 # 24cm from the left
DECLINATION_POINT_Y = 0.04 # 4cm from the top

import argparse
import sys
import os.path
import logging
import math

def format_coordinate(c):
    """Formats a coordinate (int, eg. 1501000) into a string like 15,00,000"""
    c = str(c)
    return c[0:2]+','+c[2:4]+','+c[4:]


class Annotation(object):
    def __init__(self, x, y, text):
        self.x = x
        self.y = y
        self.text = text
    
    def __repr__(self):
        return "Annotation()"
    
    def __str__(self):
        return "Annotation({}, {}, {})".format(self.y, self.x, self.text)
    
    def plot(self):
        return "-annotate {0:+d}{1:+d} '{2}'".format(self.y, self.x, self.text)

class Sheet(object):
    
    def factory(e1, n1, e2, n2):
        """Creates sheet objects based on a line defined by two coordinates"""
        
        # calculate room on a sheet real m (real_e contains the number of m of landscape that fit onto one sheet)
        # using round to avoid floating point errors
        real_e = round((SHEET_E - 2*SHEET_BORDER)*MAP_RESOLUTION)
        real_n = round((SHEET_N - 2*SHEET_BORDER)*MAP_RESOLUTION)
        logging.debug("real_e:{} real_n:{}".format(real_e, real_n))
        
        # step max is the number of real m one map can shift in each direction to still include the required overlap
        # using round to avoid floating point errors
        step_max_e = round((SHEET_E - 2*SHEET_BORDER -2*SHEET_OVERLAP)*MAP_RESOLUTION)
        step_max_n = round((SHEET_N - 2*SHEET_BORDER -2*SHEET_OVERLAP)*MAP_RESOLUTION)
        logging.debug("step_max_e:{} step_max_n:{}".format(step_max_e, step_max_n))
        
        # distance to cover between the two coordinates
        distance_e = e2 - e1
        distance_n = n2 - n1
        logging.debug("distance_e:{} distance_n:{}".format(distance_e, distance_n))
        
        # number of sheets required to cover that distance
        number_e = math.ceil(abs(distance_e) / step_max_e) + 1
        number_n = math.ceil(abs(distance_n) / step_max_n) + 1
        # number is the number of sheets required (the larger of the e or n number of sheets required)
        number = max(number_e, number_n)
        logging.debug("number_e:{} number_n:{} number:{}".format(number_e, number_n, number))
        
        # acutal step (the number of required sheets spread across the distance)
        if number > 1:
            step_e = distance_e / (number - 1)
            step_n = distance_n / (number - 1)
        else:
            step_e = 0
            step_n = 0
        logging.debug("step_e:{} step_n:{}".format(step_e, step_n))
        
        sheets = []
        for i in range(0, number):
            centre_e = e1+step_e*i
            centre_n = n1+step_n*i
            logging.debug("centre_e:{} centre_n:{}".format(centre_e, centre_n))
            
            sheet_e1 = centre_e - (real_e/2)
            sheet_n1 = centre_n - (real_n/2)
            sheet_e2 = centre_e + (real_e/2)
            sheet_n2 = centre_n + (real_n/2)
            sheets.append(Sheet(i, sheet_e1, sheet_n1, sheet_e2, sheet_n2))
        
        return sheets
    factory = staticmethod(factory)
    
    def __init__(self, id, e1, n1, e2, n2):
        self.id = id
        self.e1 = e1
        self.n1 = n1
        self.e2 = e2
        self.n2 = n2
    
    def __repr__(self):
        return "Sheet()"
    
    def __str__(self):
        return "Sheet({},{} {},{})".format(self.e1, self.n1, self.e2, self.n2)
    
    def crop(self, tiff):
        """Prints the command to crop a square defined by two coordinates from a GeoTIFF and converts it into a PDF"""
        print("gdalwarp -te {} {} {} {} {} {:02d}.tif".format(self.e1, self.n1, self.e2, self.n2, tiff, self.id))
        print("tiff2pdf {0:02d}.tif -o {0:02d}.pdf".format(self.id))
    
    def plot_coordinates(self):
        
        #Annotation = namedtuple('Annotation', 'x y text')
        
        # find first easting coordinate
        e = int(round(self.e1/COORDINATE_STEP,0)*COORDINATE_STEP+COORDINATE_STEP)
        x_annotations = []
        
        while e < self.e2:
            
            # x is the x coordinate in the map where the coordinate text should be placed
            # x is the distance to the left
            x = round((e-self.e1) * DPM_REAL - COORDINATE_LABEL_OFFSET)
            logging.debug("e:{} offet_e:{}".format(e, x))
            x_annotations.append(Annotation(x, COORDINATE_LABEL_OFFSET, format_coordinate(e)))
            
            e += COORDINATE_STEP
        
        cmd = "convert -font helvetica -fill '#0085be' -pointsize 8 -density 300 -undercolor '#ffffff80' -rotate 90 "
        for x_annotation in x_annotations:
            cmd += x_annotation.plot() + " "
        cmd += "-rotate -90 {0:02d}.pdf {0:02d}.pdf".format(self.id)
        print(cmd)
        
        
        n = int(round(self.n1/COORDINATE_STEP,0)*COORDINATE_STEP+COORDINATE_STEP)
        y_annotations = []
        
        while n < self.n2:
            # y is the y coordinate in the map where the coordinate text should be placed, 0 is in the top-left corner 
            # y is the distance to the top
            y = round((self.n2-n) * DPM_REAL - COORDINATE_LABEL_OFFSET)
            logging.debug("n:{} offet_e:{}".format(n, y))
            y_annotations.append(Annotation(y, COORDINATE_LABEL_OFFSET, format_coordinate(n)))
            
            n += COORDINATE_STEP
        
        cmd = "convert -font helvetica -fill '#0085be' -pointsize 8 -density 300 -undercolor '#ffffff80' "
        for y_annotation in y_annotations:
            cmd += y_annotation.plot() + " "
        cmd += "{0:02d}.pdf {0:02d}.pdf".format(self.id)
        print(cmd)
    
    def plot_declination(self, angle):
        args = []
        
        gn_l = 0.03
        label_offset_x = 0.002
        label_offset_y = 0.002
        declination_y = 0.025
        
        # GN line
        x1 = DECLINATION_POINT_X*DPM_MAP
        y1 = DECLINATION_POINT_Y*DPM_MAP
        x2 = (DECLINATION_POINT_X)*DPM_MAP
        y2 = (DECLINATION_POINT_Y-gn_l)*DPM_MAP
        args.append("-draw 'line {:.0f},{:.0f} {:.0f},{:.0f}'".format(x1, y1, x2, y2))
        
        # MN line
        x1 = DECLINATION_POINT_X*DPM_MAP
        y1 = DECLINATION_POINT_Y*DPM_MAP
        x_offset = math.sin(math.radians(angle))*gn_l
        logging.debug("x_offset:{}".format(x_offset))
        x2 = (DECLINATION_POINT_X+x_offset)*DPM_MAP
        y2 = (DECLINATION_POINT_Y-0.03)*DPM_MAP
        args.append("-draw 'line {:.0f},{:.0f} {:.0f},{:.0f}'".format(x1, y1, x2, y2))
        
        args.append("-strokewidth 1")
        
        # GN label
        x = (DECLINATION_POINT_X-label_offset_x)*DPM_MAP
        y = (DECLINATION_POINT_Y-gn_l-label_offset_y)*DPM_MAP
        args.append("-annotate {:+.0f}{:+.0f} 'GN'".format(x, y))
        
        # MN label
        x = (DECLINATION_POINT_X+x_offset-label_offset_x)*DPM_MAP
        y = (DECLINATION_POINT_Y-gn_l-label_offset_y)*DPM_MAP
        args.append("-annotate {:+.0f}{:+.0f} 'MN'".format(x, y))
        
        # declination label
        x = (DECLINATION_POINT_X+x_offset/2-label_offset_x)*DPM_MAP
        y = (DECLINATION_POINT_Y-declination_y)*DPM_MAP
        args.append("-annotate {:+.0f}{:+.0f} '{}°'".format(x, y, angle))
        
        cmd = "convert -density 300 -stroke '#0085be' -strokewidth 3 -font helvetica -fill '#0085be' -pointsize 8 -undercolor '#ffffff80' "
        cmd+= " ".join(args)
        cmd+= " {0:02d}.pdf {0:02d}.pdf".format(self.id)
        print(cmd)
    
    def plot_filename(self):
        return "{0:02d}.pdf".format(self.id)


def str2bool(v):
    """Converts various string representations of booleans into boolean values"""
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def read_parameter(argv):
    """Parses the command line parameters"""
    
    parser = argparse.ArgumentParser(description='Uses a line (defined by two coordinates) and generate A4 maps that cover the defined line.')
    
    parser.add_argument('e1', type=int)
    parser.add_argument('n1', type=int)
    parser.add_argument('e2', type=int)
    parser.add_argument('n2', type=int)
    parser.add_argument('tiff')
    parser.add_argument('-v', '--verbose', type=str2bool, nargs='?', const=True, default=False, help="Activate nice mode.")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    else:
        logging.basicConfig(stream=sys.stderr, level=logging.INFO)
        
    logging.debug(args)
    
    if not os.path.isfile(args.tiff):
        print("TIFF file: '{}' does not exist!".format(args.tiff), file=sys.stderr)
        sys.exit(EXIT_ERROR)
    
    return args


def main(argv):
    args = read_parameter(argv)
    #print(args)
    
    print("#!/bin/bash")
    
    # get sheets
    merge = "convert -density 300 "
    tidyup = "rm "
    sheets = Sheet.factory(args.e1, args.n1, args.e2, args.n2)
    for sheet in sheets:
        sheet.crop(args.tiff)
        sheet.plot_coordinates()
        sheet.plot_declination(22)
        merge += sheet.plot_filename() + " "
        tidyup += sheet.plot_filename() + " "
    # generate sheets
    merge += "map.pdf"
    
    print(merge)
    print(tidyup)
    print("")


if __name__ == "__main__":
    main(sys.argv)
    