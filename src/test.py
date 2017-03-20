# Import HMC55883L library that wraps I2C communication
from i2clibraries import i2c_hmc5883l
import sys, time, argparse

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

# Instantiate I2C communication and set HMC5883L to continuous mode
hmc5883l = i2c_hmc5883l.i2c_hmc5883l(1)
hmc5883l.setContinuousMode()

# Set declination to correct for heading (adds declination to heading)
# hmc5883l.setDeclination(12,4)

# Print magnetometer x, y, z, and heading
# Heading is angle away from North in clockwise direction, i.e. arcTan(y,x)
# print(hmc5883l)

# Prepare output file
args.outfile.write('x,y,z\n')

sleep_time = 1/args.freq
# Take num samples of x, y, and z magnitudes
for i in list(range(args.num)):
    x, y, z = hmc5883l.getAxes()
    args.outfile.write('%.2f,%.2f,%.2f\n' % (x, y, z))
    time.sleep(sleep_time)
