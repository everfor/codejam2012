import strategies as stra

sma = stra.SMA(5)
lwma = stra.LWMA(5)
ema = stra.EMA(5)
tma = stra.TMA(5)

sma.update(61.590, 1)
lwma.update(61.590, 1)
ema.update(61.590, 1)
tma.update(61.590, 1)

print 'sma = %.3f' % sma.showValue()
print 'lwma = %.3f' % lwma.showValue()
print 'ema = %.3f' % ema.showValue()
print 'tma = %.3f' % tma.showValue()
print '-------------------------------------'

sma.update(61.440, 2)
lwma.update(61.440, 2)
ema.update(61.440, 2)
tma.update(61.440, 2)
print 'sma = %.3f' % sma.showValue()
print 'lwma = %.3f' % lwma.showValue()
print 'ema = %.3f' % ema.showValue()
print 'tma = %.3f' % tma.showValue()
print '-------------------------------------'

sma.update(61.320, 3)
lwma.update(61.320, 3)
ema.update(61.320, 3)
tma.update(61.320, 3)

sma.update(61.670, 4)
lwma.update(61.670, 4)
ema.update(61.670, 4)
tma.update(61.670, 4)

sma.update(61.920, 5)
lwma.update(61.920, 5)
ema.update(61.920, 5)
tma.update(61.920, 5)

sma.update(62.610, 6)
lwma.update(62.610, 6)
ema.update(62.610, 6)
tma.update(62.610, 6)

print 'sma = %.3f' % sma.showValue()
print 'lwma = %.3f' % lwma.showValue()
print 'ema = %.3f' % ema.showValue()
print 'tma = %.3f' % tma.showValue()





