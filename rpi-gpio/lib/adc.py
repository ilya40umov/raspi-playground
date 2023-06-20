import smbus

ADS7830_ADDRESS = 0x4B


def detect_module():
    bus = smbus.SMBus(1)

    def check_i2c_address(address):
        try:
            bus.write_byte(address, 0)
            print("Found device in address 0x%x" % (address))
            return True
        except:
            print("Not found device in address 0x%x" % (address))
            return False

    if check_i2c_address(ADS7830_ADDRESS):
        return ADS7830(bus)
    else:
        bus.close()
        print("No ADC module detected, try checking with 'i2cdetect -y 1'")
        return None


class AdcModule(object):
    def __init__(self, cmd, address, bus):
        self.cmd = cmd
        self.address = address
        self.bus = bus

    def read(self, channel):
        pass

    def close(self):
        self.bus.close()


class ADS7830(AdcModule):
    def __init__(self, bus):
        super().__init__(cmd=0x84, address=ADS7830_ADDRESS, bus=bus)

    def read(self, channel):
        if channel < 0 or channel > 7:
            raise Exception(f"Incorrect channel {channel}")
        return self.bus.read_byte_data(
            self.address, self.cmd | (((channel << 2 | channel >> 1) & 0x07) << 4)
        )
