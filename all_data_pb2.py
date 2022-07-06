# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: all_data.proto

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
  name='all_data.proto',
  package='AllData',
  serialized_pb=_b('\n\x0e\x61ll_data.proto\x12\x07\x41llData\"\xdf\x02\n\x0bRadarObject\x12\x11\n\tobject_id\x18\x01 \x02(\x05\x12\x17\n\x0fobject_distlong\x18\x02 \x02(\x02\x12\x16\n\x0eobject_distlat\x18\x03 \x02(\x02\x12\x17\n\x0fobject_vrellong\x18\x04 \x02(\x02\x12\x16\n\x0eobject_vrellat\x18\x05 \x02(\x02\x12\x17\n\x0fobject_arellong\x18\x06 \x02(\x02\x12\x16\n\x0eobject_arellat\x18\x07 \x02(\x02\x12\x15\n\robject_length\x18\x08 \x02(\x02\x12\x14\n\x0cobject_width\x18\t \x02(\x02\x12\x1f\n\x17object_orientationangle\x18\n \x02(\x02\x12\x12\n\nobject_rcs\x18\x0b \x02(\x02\x12\x16\n\x0eobject_dynprop\x18\x0c \x02(\x05\x12\x1a\n\x12object_probofexist\x18\r \x02(\x05\x12\x14\n\x0cobject_class\x18\x0e \x02(\x05\"M\n\x0eStructureRadar\x12\x0f\n\x07num_obj\x18\x01 \x02(\x05\x12*\n\x0cradar_object\x18\x02 \x03(\x0b\x32\x14.AllData.RadarObject\"(\n\x05Point\x12\t\n\x01x\x18\x01 \x02(\x02\x12\t\n\x01y\x18\x02 \x02(\x02\x12\t\n\x01z\x18\x03 \x01(\x02\".\n\x08Velocity\x12\n\n\x02vx\x18\x01 \x02(\x02\x12\n\n\x02vy\x18\x02 \x02(\x02\x12\n\n\x02vz\x18\x03 \x01(\x02\"2\n\x0c\x41\x63\x63\x65leration\x12\n\n\x02\x61x\x18\x01 \x02(\x02\x12\n\n\x02\x61y\x18\x02 \x02(\x02\x12\n\n\x02\x61z\x18\x03 \x01(\x02\"\xf0\x01\n\x0b\x46usedObject\x12\x10\n\x08track_id\x18\x01 \x02(\x05\x12\x0c\n\x04type\x18\x02 \x02(\x05\x12\x0c\n\x04\x63onf\x18\x03 \x01(\x05\x12\x11\n\tlife_time\x18\x04 \x01(\x05\x12\x0b\n\x03\x61ge\x18\x05 \x01(\x05\x12 \n\x08position\x18\x06 \x01(\x0b\x32\x0e.AllData.Point\x12\x0e\n\x06length\x18\x07 \x01(\x02\x12\r\n\x05width\x18\x08 \x01(\x02\x12\x0e\n\x06height\x18\t \x01(\x02\x12\x1e\n\x03vel\x18\n \x01(\x0b\x32\x11.AllData.Velocity\x12\"\n\x03\x61\x63\x63\x18\x0b \x01(\x0b\x32\x15.AllData.Acceleration\"N\n\x0fStructureFusion\x12\x0f\n\x07num_obj\x18\x01 \x02(\x05\x12*\n\x0c\x66used_object\x18\x02 \x03(\x0b\x32\x14.AllData.FusedObject\"~\n\x04\x44\x61ta\x12\x10\n\x08\x66rame_id\x18\x01 \x02(\x05\x12\x30\n\x0fstructure_radar\x18\x02 \x01(\x0b\x32\x17.AllData.StructureRadar\x12\x32\n\x10structure_fusion\x18\x03 \x01(\x0b\x32\x18.AllData.StructureFusion')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_RADAROBJECT = _descriptor.Descriptor(
  name='RadarObject',
  full_name='AllData.RadarObject',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='object_id', full_name='AllData.RadarObject.object_id', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='object_distlong', full_name='AllData.RadarObject.object_distlong', index=1,
      number=2, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='object_distlat', full_name='AllData.RadarObject.object_distlat', index=2,
      number=3, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='object_vrellong', full_name='AllData.RadarObject.object_vrellong', index=3,
      number=4, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='object_vrellat', full_name='AllData.RadarObject.object_vrellat', index=4,
      number=5, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='object_arellong', full_name='AllData.RadarObject.object_arellong', index=5,
      number=6, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='object_arellat', full_name='AllData.RadarObject.object_arellat', index=6,
      number=7, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='object_length', full_name='AllData.RadarObject.object_length', index=7,
      number=8, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='object_width', full_name='AllData.RadarObject.object_width', index=8,
      number=9, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='object_orientationangle', full_name='AllData.RadarObject.object_orientationangle', index=9,
      number=10, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='object_rcs', full_name='AllData.RadarObject.object_rcs', index=10,
      number=11, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='object_dynprop', full_name='AllData.RadarObject.object_dynprop', index=11,
      number=12, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='object_probofexist', full_name='AllData.RadarObject.object_probofexist', index=12,
      number=13, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='object_class', full_name='AllData.RadarObject.object_class', index=13,
      number=14, type=5, cpp_type=1, label=2,
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
  serialized_start=28,
  serialized_end=379,
)


_STRUCTURERADAR = _descriptor.Descriptor(
  name='StructureRadar',
  full_name='AllData.StructureRadar',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='num_obj', full_name='AllData.StructureRadar.num_obj', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='radar_object', full_name='AllData.StructureRadar.radar_object', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=381,
  serialized_end=458,
)


_POINT = _descriptor.Descriptor(
  name='Point',
  full_name='AllData.Point',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='x', full_name='AllData.Point.x', index=0,
      number=1, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='y', full_name='AllData.Point.y', index=1,
      number=2, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='z', full_name='AllData.Point.z', index=2,
      number=3, type=2, cpp_type=6, label=1,
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
  serialized_start=460,
  serialized_end=500,
)


_VELOCITY = _descriptor.Descriptor(
  name='Velocity',
  full_name='AllData.Velocity',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='vx', full_name='AllData.Velocity.vx', index=0,
      number=1, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='vy', full_name='AllData.Velocity.vy', index=1,
      number=2, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='vz', full_name='AllData.Velocity.vz', index=2,
      number=3, type=2, cpp_type=6, label=1,
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
  serialized_start=502,
  serialized_end=548,
)


_ACCELERATION = _descriptor.Descriptor(
  name='Acceleration',
  full_name='AllData.Acceleration',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='ax', full_name='AllData.Acceleration.ax', index=0,
      number=1, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ay', full_name='AllData.Acceleration.ay', index=1,
      number=2, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='az', full_name='AllData.Acceleration.az', index=2,
      number=3, type=2, cpp_type=6, label=1,
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
  serialized_start=550,
  serialized_end=600,
)


_FUSEDOBJECT = _descriptor.Descriptor(
  name='FusedObject',
  full_name='AllData.FusedObject',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='track_id', full_name='AllData.FusedObject.track_id', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='type', full_name='AllData.FusedObject.type', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='conf', full_name='AllData.FusedObject.conf', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='life_time', full_name='AllData.FusedObject.life_time', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='age', full_name='AllData.FusedObject.age', index=4,
      number=5, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='position', full_name='AllData.FusedObject.position', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='length', full_name='AllData.FusedObject.length', index=6,
      number=7, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='width', full_name='AllData.FusedObject.width', index=7,
      number=8, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='height', full_name='AllData.FusedObject.height', index=8,
      number=9, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='vel', full_name='AllData.FusedObject.vel', index=9,
      number=10, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='acc', full_name='AllData.FusedObject.acc', index=10,
      number=11, type=11, cpp_type=10, label=1,
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
  serialized_start=603,
  serialized_end=843,
)


_STRUCTUREFUSION = _descriptor.Descriptor(
  name='StructureFusion',
  full_name='AllData.StructureFusion',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='num_obj', full_name='AllData.StructureFusion.num_obj', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='fused_object', full_name='AllData.StructureFusion.fused_object', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=845,
  serialized_end=923,
)


_DATA = _descriptor.Descriptor(
  name='Data',
  full_name='AllData.Data',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='frame_id', full_name='AllData.Data.frame_id', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='structure_radar', full_name='AllData.Data.structure_radar', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='structure_fusion', full_name='AllData.Data.structure_fusion', index=2,
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
  serialized_start=925,
  serialized_end=1051,
)

_STRUCTURERADAR.fields_by_name['radar_object'].message_type = _RADAROBJECT
_FUSEDOBJECT.fields_by_name['position'].message_type = _POINT
_FUSEDOBJECT.fields_by_name['vel'].message_type = _VELOCITY
_FUSEDOBJECT.fields_by_name['acc'].message_type = _ACCELERATION
_STRUCTUREFUSION.fields_by_name['fused_object'].message_type = _FUSEDOBJECT
_DATA.fields_by_name['structure_radar'].message_type = _STRUCTURERADAR
_DATA.fields_by_name['structure_fusion'].message_type = _STRUCTUREFUSION
DESCRIPTOR.message_types_by_name['RadarObject'] = _RADAROBJECT
DESCRIPTOR.message_types_by_name['StructureRadar'] = _STRUCTURERADAR
DESCRIPTOR.message_types_by_name['Point'] = _POINT
DESCRIPTOR.message_types_by_name['Velocity'] = _VELOCITY
DESCRIPTOR.message_types_by_name['Acceleration'] = _ACCELERATION
DESCRIPTOR.message_types_by_name['FusedObject'] = _FUSEDOBJECT
DESCRIPTOR.message_types_by_name['StructureFusion'] = _STRUCTUREFUSION
DESCRIPTOR.message_types_by_name['Data'] = _DATA

RadarObject = _reflection.GeneratedProtocolMessageType('RadarObject', (_message.Message,), dict(
  DESCRIPTOR = _RADAROBJECT,
  __module__ = 'all_data_pb2'
  # @@protoc_insertion_point(class_scope:AllData.RadarObject)
  ))
_sym_db.RegisterMessage(RadarObject)

StructureRadar = _reflection.GeneratedProtocolMessageType('StructureRadar', (_message.Message,), dict(
  DESCRIPTOR = _STRUCTURERADAR,
  __module__ = 'all_data_pb2'
  # @@protoc_insertion_point(class_scope:AllData.StructureRadar)
  ))
_sym_db.RegisterMessage(StructureRadar)

Point = _reflection.GeneratedProtocolMessageType('Point', (_message.Message,), dict(
  DESCRIPTOR = _POINT,
  __module__ = 'all_data_pb2'
  # @@protoc_insertion_point(class_scope:AllData.Point)
  ))
_sym_db.RegisterMessage(Point)

Velocity = _reflection.GeneratedProtocolMessageType('Velocity', (_message.Message,), dict(
  DESCRIPTOR = _VELOCITY,
  __module__ = 'all_data_pb2'
  # @@protoc_insertion_point(class_scope:AllData.Velocity)
  ))
_sym_db.RegisterMessage(Velocity)

Acceleration = _reflection.GeneratedProtocolMessageType('Acceleration', (_message.Message,), dict(
  DESCRIPTOR = _ACCELERATION,
  __module__ = 'all_data_pb2'
  # @@protoc_insertion_point(class_scope:AllData.Acceleration)
  ))
_sym_db.RegisterMessage(Acceleration)

FusedObject = _reflection.GeneratedProtocolMessageType('FusedObject', (_message.Message,), dict(
  DESCRIPTOR = _FUSEDOBJECT,
  __module__ = 'all_data_pb2'
  # @@protoc_insertion_point(class_scope:AllData.FusedObject)
  ))
_sym_db.RegisterMessage(FusedObject)

StructureFusion = _reflection.GeneratedProtocolMessageType('StructureFusion', (_message.Message,), dict(
  DESCRIPTOR = _STRUCTUREFUSION,
  __module__ = 'all_data_pb2'
  # @@protoc_insertion_point(class_scope:AllData.StructureFusion)
  ))
_sym_db.RegisterMessage(StructureFusion)

Data = _reflection.GeneratedProtocolMessageType('Data', (_message.Message,), dict(
  DESCRIPTOR = _DATA,
  __module__ = 'all_data_pb2'
  # @@protoc_insertion_point(class_scope:AllData.Data)
  ))
_sym_db.RegisterMessage(Data)


# @@protoc_insertion_point(module_scope)