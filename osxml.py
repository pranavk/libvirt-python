from xml.etree.ElementTree import Element

class OSXML():
    def __init__(self, conn, arch=None):
        if arch is None:
            self.arch = 'x86_64'
        self.arch = arch

    def getXML(self):
        os = Element('os')

        type = Element('type', attrib={'arch': self.arch})
        type.text = 'hvm'

        boot1 = Element('boot', attrib={'dev':'cdrom'})
        boot2 = Element('boot', attrib={'dev':'hd'})

        os.append(type)
        os.append(boot1)
        os.append(boot2)

        return os
