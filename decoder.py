def vampy_decoder(dct):
    if '__realtime__' in dct:
        print('__realtime__')
        print(dct['__realtime__'])
        x = dct['__realtime__'][0]
        y = dct['__realtime__'][1]
        return vampyhost.RealTime(x, y)
    if '__float32__' in dct:
        print('__float32__')
        print(type(dct['__float32__']))
        return numpy.float32(dct['__float32__'])
    if '__ndarray__' in dct:
        print('__ndarray__')
        print(dct['__ndarray__'])
        x = numpy.array(dct['__ndarray__'])
        print(x)
        print(type(x))
        #return numpy.ndarray((dct['__ndarray__']))
        return x
