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

    def guestGetXML(self, boot, cdrom):
        # Generate the XML out of class variables
        opt = self.options
        domain = Element('domain', attrib={'type':'kvm'})

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

        vcpu = Element('vcpu', attrib={'placement': 'static'})
        vcpu.text = self.options.vcpu

        devices = self.devices(boot, cdrom)

        domain.append(name)
        domain.append(uuid)
        domain.append(description)
        domain.append(memory)
        domain.append(currentMemory)
        domain.append(vcpu)
        domain.append(domain_os)
        domain.append(devices)

        return (ET.tostring(domain))

    def devices(self, boot, cdrom):
        text = """
        <devices>
        <emulator>/usr/bin/qemu-kvm</emulator>
        <disk device="disk" type="file">
        <driver name="qemu" type="raw" />
        <source file="%s" />
        <target bus="ide" dev="hda" />
        <address bus="0" controller="0" target="0" type="drive" unit="0" />
        </disk>
        <disk device="cdrom" type="file">
        <driver name="qemu" type="raw" />
        <source file="%s" />
        <target bus="ide" dev="hdb" />
        <readonly />
        <address bus="0" controller="0" target="0" type="drive" unit="1" />
        </disk>
        <controller index="0" model="ich9-ehci1" type="usb">
        <address bus="0x00" domain="0x0000" function="0x7" slot="0x06" type="pci" />
        </controller>
        <controller index="0" model="ich9-uhci1" type="usb">
        <master startport="0" />
        <address bus="0x00" domain="0x0000" function="0x0" multifunction="on" slot="0x06" type="pci" />
        </controller>
        <controller index="0" model="ich9-uhci2" type="usb">
        <master startport="2" />
        <address bus="0x00" domain="0x0000" function="0x1" slot="0x06" type="pci" />
        </controller>
        <controller index="0" model="ich9-uhci3" type="usb">
        <master startport="4" />
        <address bus="0x00" domain="0x0000" function="0x2" slot="0x06" type="pci" />
        </controller>
        <controller index="0" model="pci-root" type="pci" />
        <controller index="0" type="ide">
        <address bus="0x00" domain="0x0000" function="0x1" slot="0x01" type="pci" />
        </controller>
        <controller index="0" type="virtio-serial">
        <address bus="0x00" domain="0x0000" function="0x0" slot="0x05" type="pci" />
        </controller>
        <interface type="network">
        <mac address="52:54:00:e1:fb:d5" />
        <source network="default" />
        <model type="rtl8139" />
        <address bus="0x00" domain="0x0000" function="0x0" slot="0x03" type="pci" />
        </interface>
        <serial type="pty">
        <target port="0" />
        </serial>
        <console type="pty">
        <target port="0" type="serial" />
        </console>
        <channel type="spicevmc">
        <target name="com.redhat.spice.0" type="virtio" />
        <address bus="0" controller="0" port="1" type="virtio-serial" />
        </channel>
        <input bus="ps2" type="mouse" />
        <input bus="ps2" type="keyboard" />
        <graphics autoport="yes" type="spice">
        <image compression="off" />
        </graphics>
        <sound model="ich6">
        <address bus="0x00" domain="0x0000" function="0x0" slot="0x04" type="pci" />
        </sound>
        <video>
        <model heads="1" ram="65536" type="qxl" vgamem="16384" vram="65536" />
        <address bus="0x00" domain="0x0000" function="0x0" slot="0x02" type="pci" />
        </video>
        <redirdev bus="usb" type="spicevmc"></redirdev>
        <redirdev bus="usb" type="spicevmc"></redirdev>
        <memballoon model="virtio">
        <address bus="0x00" domain="0x0000" function="0x0" slot="0x07" type="pci" />
        </memballoon>
        </devices>
        """ % (boot, cdrom)

        return ET.XML(text)
