from datetime import datetime

import json
import numpy
import vampyhost


class VampCustomEncoder(json.JSONEncoder):

    def default(self, o):
        # print(o)
        if isinstance(o, vampyhost.RealTime):
            b = o.values()
            return {'__realtime__': list(b)}
        if isinstance(o, numpy.ndarray):
            return {'__ndarray__': tuple(o)}
        if isinstance(o, numpy.float32):
            return {'__float32__': o.tolist()}

        return json.JSONEncoder.default(self, o)

def vampy_decoder(dct):
    if '__realtime__' in dct:
            x = dct['__realtime__'][0]
            y = dct['__realtime__'][1]
            return vampyhost.RealTime(x, y)
    if '__float32__' in dct:
            # print('__float32__')
            # print(type(dct['__float32__']))
            return numpy.float32(dct['__float32__'])
    if '__ndarray__' in dct:
            # print('__ndarray__')
            # print(dct['__ndarray__'])
            x = numpy.array(dct['__ndarray__'])
            return x

    print(type(dct))
    print(dct)
    return dct
