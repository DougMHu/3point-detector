from i2clibraries import i2c_hmc5883l
import sys, time, argparse
import statistics as stats

def parseCSV(infile):
    
    # Read input csv file
    csv_output = infile.read()

    # Create a list of samples for each x, y, z
    x = []
    y = []
    z = []
    output_lines = csv_output.split('\n')
    for line in output_lines:
        if line:
            sample = line.split(',')
            x.append(float(sample[0]))
            y.append(float(sample[1]))
            z.append(float(sample[2]))

    # Return the lists of samples
    return x, y, z

def calculateCalibration(infile):

    # Parse input csv file
    xs, ys, zs = parseCSV(infile)

    # Find median of each axis
    x_calib = stats.median(xs)
    y_calib = stats.median(ys)
    z_calib = stats.median(zs)

    # Return calibration values
    return x_calib, y_calib, z_calib 

def writeCalibratedSamples(num, freq, infile, outfile):

    # Calculate calibration constants
    xc, yc, zc = calculateCalibration(infile)

    # Instantiate I2C communication and set HMC5883L to continuous mode
    hmc5883l = i2c_hmc5883l.i2c_hmc5883l(1)
    hmc5883l.setContinuousMode()

    # Store and return sample lists
    xs = []
    ys = []
    zs = []

    sleep_time = 1/freq
    # Take num samples of x, y, and z magnitudes
    for i in list(range(num)):
        x, y, z = hmc5883l.getAxes()
        x -= xc
        y -= yc
        z -= zc
        outfile.write('%.2f,%.2f,%.2f\n' % (x, y, z))
        xs.append(x)
        ys.append(y)
        zs.append(z)
        time.sleep(sleep_time)

    return xs, ys, zs

if __name__ == '__main__':
    # Parse arguments
    parser = argparse.ArgumentParser(description='Take magnetometer samples.')
    parser.add_argument('--num', default=100, type=int)
    parser.add_argument('--dur', type=int)
    parser.add_argument('--freq', default=10, type=int)
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'),
                    default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'),
                    default=sys.stdout)
    args = parser.parse_args()
    if args.dur:
        args.num = args.dur * args.freq
    
    # Take samples and write them to outfile
    xs, ys, zs = writeCalibratedSamples(args.num, args.freq, args.infile, args.outfile)

    # Print median calibrated measurements
    print(stats.median(xs))
    print(stats.median(ys))
    print(stats.median(zs))
