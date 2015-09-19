#!/usr/bin/python

import pyaudio
import numpy
import audioop
import sys
import math
import struct
import time
import curses
import sys
from socket import *

p = pyaudio.PyAudio()

# algorithm parameters
bins        = 20
chunk       = 4096
scale       = 300
exponent    = .5
sample_rate = 44100 
    
# filenames to be used
save_file_data =   'recorded_keystrokes_data.txt'
save_file_target = 'recorded_keystrokes_target.txt'

def find_input_device():
    device_index = None            
    for i in range( p.get_device_count() ):     
        devinfo = p.get_device_info_by_index(i)   
        print( "Device %d: %s"%(i,devinfo["name"]) )

        for keyword in ["mic","input"]:
            if keyword in devinfo["name"].lower():
                print( "Found an input: device %d - %s"%(i,devinfo["name"]) )
                device_index = i
                return device_index

    if device_index == None:
        print( "No preferred input found; using default input device." )

    return device_index
 
def get_coeffs(data, width, sample_rate, bins):
    fmt = "%dH"%(len(data)/2)
    data = struct.unpack(fmt, data)
    data = numpy.array(data, dtype='h')
    fourier = numpy.fft.fft(data)
    ffty = numpy.abs(fourier[0:len(fourier)/2])/1000
    ffty1 = ffty[:len(ffty)/2]
    ffty2 = ffty[len(ffty)/2::]+2
    ffty2 = ffty2[::-1]
    ffty = ffty1+ffty2
    ffty = numpy.log(ffty)-2
    fourier = list(ffty)[4:-4]
    fourier = fourier[:len(fourier)/2]
    size = len(fourier)
    levels = [sum(fourier[i:(i+size/bins)]) for i in xrange(0, size, size/bins)][:bins]
    
    return levels

def visualize(device):
    global bins, chunk, sample_rate, exponent
    scale    = 300
    
    p = pyaudio.PyAudio()
    stream = p.open(format = pyaudio.paInt16,
                    channels = 1,
                    rate = sample_rate,
                    input = True,
                    frames_per_buffer = chunk,
                    input_device_index = device)
    
    screen = curses.initscr()
    curses.start_color()
    curses.use_default_colors()
    curses.curs_set(0)
    curses.init_pair(1, -1, curses.COLOR_BLUE)
    curses.init_pair(2, -1, -1)
    
    term_height = screen.getmaxyx()[0]
    term_width = screen.getmaxyx()[1]

    min_bar_height = 1
    bar_width = 4
    bar_spacing = 2
    vertical_offset = 2

    bars = []
    for i in range(bins):
        xcoord = bar_spacing + i*(bar_width + bar_spacing) 
        bars.append(curses.newwin(min_bar_height, bar_width, term_height - vertical_offset , xcoord)) 
    screen.nodelay(1)
    height = 0
    
    try:
        while True:
            catch_data = False
            c = screen.getch()
            if c != -1:
                screen.addstr(0, 0, str(c) + ' ')
                f_d = open(save_file_data, 'a')
                f_t = open(save_file_target, 'a')
                catch_data = True
            
            if curses.is_term_resized(term_height, term_width): 
                screen.clear()
                screen.refresh()

                term_height = screen.getmaxyx()[0]
                term_width = screen.getmaxyx()[1]

                bars = []
                
                for i in range(bins):
                    xcoord = bar_spacing + i*(bar_width + bar_spacing) 
                    bars.append(curses.newwin(min_bar_height, bar_width, term_height - vertical_offset, xcoord)) 

            data = stream.read(chunk)
            levels = get_coeffs(data, chunk, sample_rate, bins)
            
            if catch_data:
                data = ', '.join([x.astype('str') for x in levels])
                f_d.write(data + '\n')
                f_t.write(str(c) + '\n')
 
            for i in range(bins):
                height = max(min((levels[i]*1.0)/scale, 1.0), 0.0)
                height = height**exponent
                height = int(height*term_height*1.5)
                
                prev_coords = bars[i].getbegyx()
                prev_bar_height = bars[i].getmaxyx()[0]

                bars[i].bkgd(' ', curses.color_pair(2))
                bars[i].erase()
                bars[i].refresh()
        
                new_bar_height = max(height, min_bar_height)
                bars[i] = curses.newwin(new_bar_height, bar_width, prev_coords[0] - (new_bar_height - prev_bar_height) , prev_coords[1]) 
                bars[i].bkgd(' ', curses.color_pair(1))     
                bars[i].refresh()
    
    except KeyboardInterrupt:
        pass
        
    finally:
        print "\nStopping to record"
        stream.close()
        p.terminate()
        curses.endwin()


def main():
    global save_file_data, save_file_target
    if len(sys.argv) > 1 and str(sys.argv[1]) == '-train':
        save_file_data = 'train_' + save_file_data
        save_file_target = 'train_' + save_file_target

    visualize(find_input_device())

if __name__ == '__main__':
    main()    