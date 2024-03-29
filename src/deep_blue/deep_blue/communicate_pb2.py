# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: communicate.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)




DESCRIPTOR = _descriptor.FileDescriptor(
  name='communicate.proto',
  package='teamstyle16.communicate',
  serialized_pb='\n\x11\x63ommunicate.proto\x12\x17teamstyle16.communicate\"+\n\x08Position\x12\t\n\x01x\x18\x01 \x02(\x05\x12\t\n\x01y\x18\x02 \x02(\x05\x12\t\n\x01z\x18\x03 \x02(\x05\"\xb7\x02\n\x07\x45lement\x12\r\n\x05index\x18\x01 \x02(\x05\x12\x0c\n\x04type\x18\x02 \x02(\x05\x12.\n\x03pos\x18\x03 \x02(\x0b\x32!.teamstyle16.communicate.Position\x12\x33\n\x04size\x18\x04 \x01(\x0b\x32%.teamstyle16.communicate.Element.Size\x12\x0f\n\x07visible\x18\x05 \x02(\x08\x12\x0f\n\x04team\x18\x06 \x01(\x05:\x01\x32\x12\x0e\n\x06health\x18\x07 \x01(\x05\x12\x0c\n\x04\x66uel\x18\x08 \x01(\x05\x12\x0c\n\x04\x61mmo\x18\t \x01(\x05\x12\r\n\x05metal\x18\n \x01(\x05\x12/\n\x04\x64\x65st\x18\x0b \x01(\x0b\x32!.teamstyle16.communicate.Position\x1a\x1c\n\x04Size\x12\t\n\x01x\x18\x01 \x02(\x05\x12\t\n\x01y\x18\x02 \x02(\x05\"4\n\x03Map\x12\r\n\x05x_max\x18\x01 \x02(\x05\x12\r\n\x05y_max\x18\x02 \x02(\x05\x12\x0f\n\x07terrain\x18\x03 \x03(\x05\"\xa1\x01\n\nStableInfo\x12)\n\x03map\x18\x01 \x02(\x0b\x32\x1c.teamstyle16.communicate.Map\x12\x10\n\x08team_num\x18\x02 \x02(\x05\x12\x0f\n\x07weather\x18\x03 \x01(\x05\x12\x18\n\x10population_limit\x18\x04 \x01(\x05\x12\x13\n\x0bround_limit\x18\x05 \x01(\x05\x12\x16\n\x0etime_per_round\x18\x06 \x01(\x02\"\xf2\x01\n\tRoundInfo\x12\r\n\x05round\x18\x01 \x02(\x05\x12\r\n\x05score\x18\x02 \x03(\x05\x12\x12\n\npopulation\x18\x03 \x01(\x05\x12\x31\n\x07\x65lement\x18\x04 \x03(\x0b\x32 .teamstyle16.communicate.Element\x12K\n\x0fproduction_list\x18\x05 \x03(\x0b\x32\x32.teamstyle16.communicate.RoundInfo.ProductionEntry\x1a\x33\n\x0fProductionEntry\x12\x0c\n\x04type\x18\x01 \x02(\x05\x12\x12\n\nround_left\x18\x02 \x02(\x05')




_POSITION = _descriptor.Descriptor(
  name='Position',
  full_name='teamstyle16.communicate.Position',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='x', full_name='teamstyle16.communicate.Position.x', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='y', full_name='teamstyle16.communicate.Position.y', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='z', full_name='teamstyle16.communicate.Position.z', index=2,
      number=3, type=5, cpp_type=1, label=2,
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
  serialized_start=46,
  serialized_end=89,
)


_ELEMENT_SIZE = _descriptor.Descriptor(
  name='Size',
  full_name='teamstyle16.communicate.Element.Size',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='x', full_name='teamstyle16.communicate.Element.Size.x', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='y', full_name='teamstyle16.communicate.Element.Size.y', index=1,
      number=2, type=5, cpp_type=1, label=2,
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
  serialized_start=375,
  serialized_end=403,
)

_ELEMENT = _descriptor.Descriptor(
  name='Element',
  full_name='teamstyle16.communicate.Element',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='index', full_name='teamstyle16.communicate.Element.index', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='type', full_name='teamstyle16.communicate.Element.type', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='pos', full_name='teamstyle16.communicate.Element.pos', index=2,
      number=3, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='size', full_name='teamstyle16.communicate.Element.size', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='visible', full_name='teamstyle16.communicate.Element.visible', index=4,
      number=5, type=8, cpp_type=7, label=2,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='team', full_name='teamstyle16.communicate.Element.team', index=5,
      number=6, type=5, cpp_type=1, label=1,
      has_default_value=True, default_value=2,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='health', full_name='teamstyle16.communicate.Element.health', index=6,
      number=7, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='fuel', full_name='teamstyle16.communicate.Element.fuel', index=7,
      number=8, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ammo', full_name='teamstyle16.communicate.Element.ammo', index=8,
      number=9, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='metal', full_name='teamstyle16.communicate.Element.metal', index=9,
      number=10, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='dest', full_name='teamstyle16.communicate.Element.dest', index=10,
      number=11, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_ELEMENT_SIZE, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=92,
  serialized_end=403,
)


_MAP = _descriptor.Descriptor(
  name='Map',
  full_name='teamstyle16.communicate.Map',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='x_max', full_name='teamstyle16.communicate.Map.x_max', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='y_max', full_name='teamstyle16.communicate.Map.y_max', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='terrain', full_name='teamstyle16.communicate.Map.terrain', index=2,
      number=3, type=5, cpp_type=1, label=3,
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
  serialized_start=405,
  serialized_end=457,
)


_STABLEINFO = _descriptor.Descriptor(
  name='StableInfo',
  full_name='teamstyle16.communicate.StableInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='map', full_name='teamstyle16.communicate.StableInfo.map', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='team_num', full_name='teamstyle16.communicate.StableInfo.team_num', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='weather', full_name='teamstyle16.communicate.StableInfo.weather', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='population_limit', full_name='teamstyle16.communicate.StableInfo.population_limit', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='round_limit', full_name='teamstyle16.communicate.StableInfo.round_limit', index=4,
      number=5, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='time_per_round', full_name='teamstyle16.communicate.StableInfo.time_per_round', index=5,
      number=6, type=2, cpp_type=6, label=1,
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
  serialized_start=460,
  serialized_end=621,
)


_ROUNDINFO_PRODUCTIONENTRY = _descriptor.Descriptor(
  name='ProductionEntry',
  full_name='teamstyle16.communicate.RoundInfo.ProductionEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='type', full_name='teamstyle16.communicate.RoundInfo.ProductionEntry.type', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='round_left', full_name='teamstyle16.communicate.RoundInfo.ProductionEntry.round_left', index=1,
      number=2, type=5, cpp_type=1, label=2,
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
  serialized_start=815,
  serialized_end=866,
)

_ROUNDINFO = _descriptor.Descriptor(
  name='RoundInfo',
  full_name='teamstyle16.communicate.RoundInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='round', full_name='teamstyle16.communicate.RoundInfo.round', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='score', full_name='teamstyle16.communicate.RoundInfo.score', index=1,
      number=2, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='population', full_name='teamstyle16.communicate.RoundInfo.population', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='element', full_name='teamstyle16.communicate.RoundInfo.element', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='production_list', full_name='teamstyle16.communicate.RoundInfo.production_list', index=4,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_ROUNDINFO_PRODUCTIONENTRY, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=624,
  serialized_end=866,
)

_ELEMENT_SIZE.containing_type = _ELEMENT;
_ELEMENT.fields_by_name['pos'].message_type = _POSITION
_ELEMENT.fields_by_name['size'].message_type = _ELEMENT_SIZE
_ELEMENT.fields_by_name['dest'].message_type = _POSITION
_STABLEINFO.fields_by_name['map'].message_type = _MAP
_ROUNDINFO_PRODUCTIONENTRY.containing_type = _ROUNDINFO;
_ROUNDINFO.fields_by_name['element'].message_type = _ELEMENT
_ROUNDINFO.fields_by_name['production_list'].message_type = _ROUNDINFO_PRODUCTIONENTRY
DESCRIPTOR.message_types_by_name['Position'] = _POSITION
DESCRIPTOR.message_types_by_name['Element'] = _ELEMENT
DESCRIPTOR.message_types_by_name['Map'] = _MAP
DESCRIPTOR.message_types_by_name['StableInfo'] = _STABLEINFO
DESCRIPTOR.message_types_by_name['RoundInfo'] = _ROUNDINFO

class Position(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _POSITION

  # @@protoc_insertion_point(class_scope:teamstyle16.communicate.Position)

class Element(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType

  class Size(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _ELEMENT_SIZE

    # @@protoc_insertion_point(class_scope:teamstyle16.communicate.Element.Size)
  DESCRIPTOR = _ELEMENT

  # @@protoc_insertion_point(class_scope:teamstyle16.communicate.Element)

class Map(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _MAP

  # @@protoc_insertion_point(class_scope:teamstyle16.communicate.Map)

class StableInfo(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _STABLEINFO

  # @@protoc_insertion_point(class_scope:teamstyle16.communicate.StableInfo)

class RoundInfo(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType

  class ProductionEntry(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _ROUNDINFO_PRODUCTIONENTRY

    # @@protoc_insertion_point(class_scope:teamstyle16.communicate.RoundInfo.ProductionEntry)
  DESCRIPTOR = _ROUNDINFO

  # @@protoc_insertion_point(class_scope:teamstyle16.communicate.RoundInfo)


# @@protoc_insertion_point(module_scope)
