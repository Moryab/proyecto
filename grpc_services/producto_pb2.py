# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: producto.proto
# Protobuf Python Version: 6.31.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    6,
    31,
    0,
    '',
    'producto.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0eproducto.proto\x12\tproductos\"e\n\x0fProductoRequest\x12\x0e\n\x06nombre\x18\x01 \x01(\t\x12\x13\n\x0bsucursal_id\x18\x02 \x01(\x05\x12\x0e\n\x06precio\x18\x03 \x01(\x01\x12\r\n\x05stock\x18\x04 \x01(\x05\x12\x0e\n\x06imagen\x18\x05 \x01(\x0c\"2\n\x10ProductoResponse\x12\r\n\x05\x65xito\x18\x01 \x01(\x08\x12\x0f\n\x07mensaje\x18\x02 \x01(\t2[\n\x0fProductoService\x12H\n\rCrearProducto\x12\x1a.productos.ProductoRequest\x1a\x1b.productos.ProductoResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'producto_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_PRODUCTOREQUEST']._serialized_start=29
  _globals['_PRODUCTOREQUEST']._serialized_end=130
  _globals['_PRODUCTORESPONSE']._serialized_start=132
  _globals['_PRODUCTORESPONSE']._serialized_end=182
  _globals['_PRODUCTOSERVICE']._serialized_start=184
  _globals['_PRODUCTOSERVICE']._serialized_end=275
# @@protoc_insertion_point(module_scope)
