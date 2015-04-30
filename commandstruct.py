from ctypes import Structure,c_uint16,c_double,c_ubyte,c_uint32,c_int16,c_uint8

class ROBOT_JOINT_REF(Structure):
      _pack_ = 1
      _fields_ = [("position", c_double),
		              ("velocity", c_double),
		              ("acc", c_double),
		              ("mode", c_uint8),
		              ("ID", c_uint8),
		              ("lambda", c_double),
		              ("cmd", c_double)]
