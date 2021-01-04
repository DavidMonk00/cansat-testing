import struct
import temporenc


class Packet:
    def __init__(self, schema, **kwargs):
        self.schema = schema
        for k, v in kwargs.items():
            assert(k in schema['fields'])
            setattr(self, k, v)
        for field in schema['fields']:
            assert hasattr(self, field), "{} data field is missing".format(field)

    def __str__(self):
        strings = []
        for key, value in self.schema['fields'].items():
            if type(getattr(self, key)) == tuple:
                strings.append(value['representation'].format(*getattr(self, key)))
            else:
                strings.append(value['representation'].format(getattr(self, key)))
        return " | ".join(strings)

    def encode(self):
        b = []
        for key, value in self.schema['fields'].items():
            if not value['custom']:
                if type(getattr(self, key)) == int or type(getattr(self, key)) == float:
                    b.append(bytearray(struct.pack(value["type"], getattr(self, key))))
                elif type(getattr(self, key)) == tuple:
                    b.append(bytearray(struct.pack(value["type"], *getattr(self, key))))
            else:
                if key == 'time':
                    b.append(temporenc.packb(getattr(self, key)))
        return b''.join(b)

    @staticmethod
    def decode(schema, packet_bytes):
        fields = {}
        cursor = 0
        for i, key in enumerate(schema['fields'].keys()):
            if not schema['fields'][key]['custom']:
                data = struct.unpack(schema['fields'][key]["type"], packet_bytes[cursor:cursor+schema['fields'][key]["length"]])
                fields[key] = data[0] if len(data) == 1 else data
            else:
                if key == 'time':
                    fields[key] = temporenc.unpackb(packet_bytes[cursor:cursor+schema['fields'][key]["length"]]).datetime()
            cursor += schema['fields'][key]["length"]
        return Packet(schema, **fields)
