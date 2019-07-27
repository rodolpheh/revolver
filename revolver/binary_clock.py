from revolver import Revolver
from collections import namedtuple

Minutes = namedtuple('Minutes', ['tens', 'units'])

def to_binary(revolver_datetime):
    # Weird way to split tens and units in a decimal number but fine for now
    minutes = Minutes(*list('{:02d}'.format(revolver_datetime.minute)))
    print('{:04b}°{:04b}:{:04b}\''
          .format(
              revolver_datetime.hour,
              int(minutes.tens),
              int(minutes.units)
          )
    )

to_binary(Revolver.now())
