from xml.etree.ElementTree import Element, SubElement
import xml.etree.ElementTree as ET
import pprint

import utils
from osxml import OSXML

class Guest():
    def __init__(self, conn, options):
        self.conn = conn
        self.options = options

        self.setDefaultValues()

    def setDefaultValues(self):
        self.options.description = "test description"
        self.options.memunit = 'KiB'

        self.os = OSXML(self.conn, arch=self.options.cpuarch)

    def guestGetXML(self):
        # Generate the XML out of class variables
        opt = self.options
        domain = Element('domain', attrib={'key':'kvm'})

        name = Element('name')
        name.text = opt.name

        uuid = Element('uuid')
        uuid.text = utils.randomUUID()

        description = Element('description')
        description.text = opt.description

        memory = Element('memory', attrib={'unit': opt.memunit})
        memory.text = opt.mem

        currentMemory = Element('currentMemory', attrib={'unit': opt.memunit})
        currentMemory.text = opt.mem

        domain_os = self.os.getXML()

        devices = self.devices()

        domain.append(name)
        domain.append(uuid)
        domain.append(description)
        domain.append(memory)
        domain.append(currentMemory)
        domain.append(domain_os)
        domain.append(devices)

        pprint.pprint(ET.tostring(domain))

    def devices(self):
        text = """
        <devices>
        <emulator>/usr/bin/qemu-kvm</emulator>
        <disk type='file' device='disk'>
        <driver name='qemu' type='raw'/>
        <source file='/home/pranavk/disk2.img'/>
        <target dev='hda' bus='ide'/>
        <address type='drive' controller='0' bus='0' target='0' unit='0'/>
        </disk>
        <disk type='block' device='cdrom'>
        <driver name='qemu' type='raw'/>
        <target dev='hdb' bus='ide'/>
        <readonly/>
        <address type='drive' controller='0' bus='0' target='0' unit='1'/>
        </disk>
        <controller type='usb' index='0' model='ich9-ehci1'>
        <address type='pci' domain='0x0000' bus='0x00' slot='0x06' function='0x7'/>
        </controller>
        <controller type='usb' index='0' model='ich9-uhci1'>
        <master startport='0'/>
        <address type='pci' domain='0x0000' bus='0x00' slot='0x06' function='0x0' multifunction='on'/>
        </controller>
        <controller type='usb' index='0' model='ich9-uhci2'>
        <master startport='2'/>
        <address type='pci' domain='0x0000' bus='0x00' slot='0x06' function='0x1'/>
        </controller>
        <controller type='usb' index='0' model='ich9-uhci3'>
        <master startport='4'/>
        <address type='pci' domain='0x0000' bus='0x00' slot='0x06' function='0x2'/>
        </controller>
        <controller type='pci' index='0' model='pci-root'/>
        <controller type='ide' index='0'>
        <address type='pci' domain='0x0000' bus='0x00' slot='0x01' function='0x1'/>
        </controller>
        <controller type='virtio-serial' index='0'>
        <address type='pci' domain='0x0000' bus='0x00' slot='0x05' function='0x0'/>
        </controller>
        <interface type='network'>
        <mac address='52:54:00:e1:fb:d5'/>
        <source network='default'/>
        <model type='rtl8139'/>
        <address type='pci' domain='0x0000' bus='0x00' slot='0x03' function='0x0'/>
        </interface>
        <serial type='pty'>
        <target port='0'/>
        </serial>
        <console type='pty'>
        <target type='serial' port='0'/>
        </console>
        <channel type='spicevmc'>
        <target type='virtio' name='com.redhat.spice.0'/>
        <address type='virtio-serial' controller='0' bus='0' port='1'/>
        </channel>
        <input type='mouse' bus='ps2'/>
        <input type='keyboard' bus='ps2'/>
        <graphics type='spice' autoport='yes'>
        <image compression='off'/>
        </graphics>
        <sound model='ich6'>
        <address type='pci' domain='0x0000' bus='0x00' slot='0x04' function='0x0'/>
        </sound>
        <video>
        <model type='qxl' ram='65536' vram='65536' vgamem='16384' heads='1'/>
        <address type='pci' domain='0x0000' bus='0x00' slot='0x02' function='0x0'/>
        </video>
        <redirdev bus='usb' type='spicevmc'>
        </redirdev>
        <redirdev bus='usb' type='spicevmc'>
        </redirdev>
        <memballoon model='virtio'>
        <address type='pci' domain='0x0000' bus='0x00' slot='0x07' function='0x0'/>
        </memballoon>
        </devices>
        """
        
        return ET.XML(text)
