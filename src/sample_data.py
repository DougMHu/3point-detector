from i2clibraries import i2c_hmc5883l
import sys, time, argparse

def writeSamples(num, freq, outfile):

    # Instantiate I2C communication and set HMC5883L to continuous mode
    hmc5883l = i2c_hmc5883l.i2c_hmc5883l(1)
    hmc5883l.setContinuousMode()

    sleep_time = 1/freq
    # Take num samples of x, y, and z magnitudes
    for i in list(range(num)):
        x, y, z = hmc5883l.getAxes()
        outfile.write('%.2f,%.2f,%.2f\n' % (x, y, z))
        time.sleep(sleep_time)

if __name__ == '__main__':
    # Parse arguments
    parser = argparse.ArgumentParser(description='Take magnetometer samples.')
    parser.add_argument('--num', default=100, type=int)
    parser.add_argument('--dur', type=int)
    parser.add_argument('--freq', default=10, type=int)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'),
                    default=sys.stdout)
    args = parser.parse_args()
    if args.dur:
        args.num = args.dur * args.freq
    
    # Take samples and write them to outfile
    writeSamples(args.num, args.freq, args.outfile)
