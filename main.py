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

    # check if existing machine of same name exists
    vm = None
    try:
        vm = conn.lookupByName(options.name)
    except libvirt.libvirtError:
        pass

    if vm is not None:
        print "VM of same name exists already, destroying and recreating it again"
        if vm.ID() != -1:
            vm.destroy()
        vm.undefine()

    guest = Guest(conn, options)
    xml = guest.guestGetXML(options.boot, options.cdrom).replace('\n','')
    dom = conn.createXML(xml, 0)
    dom = conn.defineXML(xml)

    if not dom:
        print "Cannot create/define domain"
        sys.exit(1)

    return 0

if __name__ == "__main__":
    main()
