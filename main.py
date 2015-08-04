import argparse
from guest import Guest

import libvirt

import sys


def getParser():
    usage = "--name NAME --ram RAM --ncpu nCPU --cpuarch CPUARCH --boot BOOTIMAGE --cdrom IMAGE"
    desc = "Create a new virtual machine from the command line arguments given"
    parser = argparse.ArgumentParser(usage=usage, description=desc)

    parser.add_argument('--version', action='version',
                        help='Shows you the current version',
                        version='0.0.1')

    parser.add_argument("-c", "--connect", help="Connect to hypervisor using libvirt",
                        default='qemu:///system')

    parser.add_argument("--desc", help="Description of the VM that is being created")

    parser.add_argument("--name", help="Name of this VM", required=True)
    parser.add_argument("--mem", help="Memory of this VM", required=True)
    parser.add_argument("--vcpu", help="Number of CPUs for the VM", required=True)
    parser.add_argument("--cpuarch", help="Architecture of the CPU", required=True)
    parser.add_argument("--boot", help="Specify the boot image", required=True)
    parser.add_argument("--cdrom", help="Specify the CDROM image to boot from",
                        required=True)
    return parser

def main(conn=None):
    parser = getParser()
    options = parser.parse_args()
    
    conn = libvirt.open(options.connect)
    if conn is None:
        print "There is some error opening connection to libvirt"
        sys.exit(1);

    guest = Guest(conn, options)
    guest.guestGetXML()
    
    return 0

if __name__ == "__main__":
    main()

