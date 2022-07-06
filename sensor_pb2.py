# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: sensor.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='sensor.proto',
  package='SensorProto',
  serialized_pb=_b('\n\x0csensor.proto\x12\x0bSensorProto\"\x90\x01\n\x08IMUFrame\x12\r\n\x05\x61\x63\x63_x\x18\x01 \x01(\x02\x12\r\n\x05\x61\x63\x63_y\x18\x02 \x01(\x02\x12\r\n\x05\x61\x63\x63_z\x18\x03 \x01(\x02\x12\x0e\n\x06gyro_x\x18\x04 \x01(\x02\x12\x0e\n\x06gyro_y\x18\x05 \x01(\x02\x12\x0e\n\x06gyro_z\x18\x06 \x01(\x02\x12\x13\n\x0btemperature\x18\x07 \x01(\x02\x12\x12\n\ntime_stamp\x18\x08 \x02(\x03\"\x82\x02\n\x08GPSFrame\x12\x11\n\tlongitude\x18\x01 \x02(\x02\x12\x10\n\x08latitude\x18\x02 \x02(\x02\x12\x12\n\ntime_stamp\x18\x03 \x02(\x03\x12\x16\n\x0elongitude_cent\x18\x04 \x01(\x02\x12\x15\n\rlongitude_dir\x18\x05 \x01(\t\x12\x15\n\rlatitude_cent\x18\x06 \x01(\x02\x12\x14\n\x0clatitude_dir\x18\x07 \x01(\t\x12\x14\n\x0cground_speed\x18\x08 \x01(\x02\x12\x15\n\rground_course\x18\t \x01(\x02\x12\x10\n\x08gps_time\x18\n \x01(\x03\x12\x10\n\x08\x61ltitude\x18\x0b \x01(\x02\x12\x10\n\x08\x61\x63\x63uracy\x18\x0c \x01(\x02\"V\n\x0bGPSFrameRaw\x12\x0c\n\x04info\x18\x01 \x01(\t\x12\x12\n\ntime_stamp\x18\x02 \x02(\x03\x12%\n\x06parsed\x18\x03 \x01(\x0b\x32\x15.SensorProto.GPSFrame')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_IMUFRAME = _descriptor.Descriptor(
  name='IMUFrame',
  full_name='SensorProto.IMUFrame',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='acc_x', full_name='SensorProto.IMUFrame.acc_x', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='acc_y', full_name='SensorProto.IMUFrame.acc_y', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='acc_z', full_name='SensorProto.IMUFrame.acc_z', index=2,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='gyro_x', full_name='SensorProto.IMUFrame.gyro_x', index=3,
      number=4, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='gyro_y', full_name='SensorProto.IMUFrame.gyro_y', index=4,
      number=5, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='gyro_z', full_name='SensorProto.IMUFrame.gyro_z', index=5,
      number=6, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='temperature', full_name='SensorProto.IMUFrame.temperature', index=6,
      number=7, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='time_stamp', full_name='SensorProto.IMUFrame.time_stamp', index=7,
      number=8, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=30,
  serialized_end=174,
)


_GPSFRAME = _descriptor.Descriptor(
  name='GPSFrame',
  full_name='SensorProto.GPSFrame',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='longitude', full_name='SensorProto.GPSFrame.longitude', index=0,
      number=1, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='latitude', full_name='SensorProto.GPSFrame.latitude', index=1,
      number=2, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='time_stamp', full_name='SensorProto.GPSFrame.time_stamp', index=2,
      number=3, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='longitude_cent', full_name='SensorProto.GPSFrame.longitude_cent', index=3,
      number=4, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='longitude_dir', full_name='SensorProto.GPSFrame.longitude_dir', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='latitude_cent', full_name='SensorProto.GPSFrame.latitude_cent', index=5,
      number=6, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='latitude_dir', full_name='SensorProto.GPSFrame.latitude_dir', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ground_speed', full_name='SensorProto.GPSFrame.ground_speed', index=7,
      number=8, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ground_course', full_name='SensorProto.GPSFrame.ground_course', index=8,
      number=9, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='gps_time', full_name='SensorProto.GPSFrame.gps_time', index=9,
      number=10, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='altitude', full_name='SensorProto.GPSFrame.altitude', index=10,
      number=11, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='accuracy', full_name='SensorProto.GPSFrame.accuracy', index=11,
      number=12, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=177,
  serialized_end=435,
)


_GPSFRAMERAW = _descriptor.Descriptor(
  name='GPSFrameRaw',
  full_name='SensorProto.GPSFrameRaw',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='info', full_name='SensorProto.GPSFrameRaw.info', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='time_stamp', full_name='SensorProto.GPSFrameRaw.time_stamp', index=1,
      number=2, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='parsed', full_name='SensorProto.GPSFrameRaw.parsed', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=437,
  serialized_end=523,
)

_GPSFRAMERAW.fields_by_name['parsed'].message_type = _GPSFRAME
DESCRIPTOR.message_types_by_name['IMUFrame'] = _IMUFRAME
DESCRIPTOR.message_types_by_name['GPSFrame'] = _GPSFRAME
DESCRIPTOR.message_types_by_name['GPSFrameRaw'] = _GPSFRAMERAW

IMUFrame = _reflection.GeneratedProtocolMessageType('IMUFrame', (_message.Message,), dict(
  DESCRIPTOR = _IMUFRAME,
  __module__ = 'sensor_pb2'
  # @@protoc_insertion_point(class_scope:SensorProto.IMUFrame)
  ))
_sym_db.RegisterMessage(IMUFrame)

GPSFrame = _reflection.GeneratedProtocolMessageType('GPSFrame', (_message.Message,), dict(
  DESCRIPTOR = _GPSFRAME,
  __module__ = 'sensor_pb2'
  # @@protoc_insertion_point(class_scope:SensorProto.GPSFrame)
  ))
_sym_db.RegisterMessage(GPSFrame)

GPSFrameRaw = _reflection.GeneratedProtocolMessageType('GPSFrameRaw', (_message.Message,), dict(
  DESCRIPTOR = _GPSFRAMERAW,
  __module__ = 'sensor_pb2'
  # @@protoc_insertion_point(class_scope:SensorProto.GPSFrameRaw)
  ))
_sym_db.RegisterMessage(GPSFrameRaw)


# @@protoc_insertion_point(module_scope)