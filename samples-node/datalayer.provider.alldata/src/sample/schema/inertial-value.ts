// automatically generated by the FlatBuffers compiler, do not modify

import * as flatbuffers from 'flatbuffers';



export class InertialValue {
  bb: flatbuffers.ByteBuffer|null = null;
  bb_pos = 0;
__init(i:number, bb:flatbuffers.ByteBuffer):InertialValue {
  this.bb_pos = i;
  this.bb = bb;
  return this;
}

static getRootAsInertialValue(bb:flatbuffers.ByteBuffer, obj?:InertialValue):InertialValue {
  return (obj || new InertialValue()).__init(bb.readInt32(bb.position()) + bb.position(), bb);
}

static getSizePrefixedRootAsInertialValue(bb:flatbuffers.ByteBuffer, obj?:InertialValue):InertialValue {
  bb.setPosition(bb.position() + flatbuffers.SIZE_PREFIX_LENGTH);
  return (obj || new InertialValue()).__init(bb.readInt32(bb.position()) + bb.position(), bb);
}

x():number {
  const offset = this.bb!.__offset(this.bb_pos, 4);
  return offset ? this.bb!.readInt16(this.bb_pos + offset) : 0;
}

y():number {
  const offset = this.bb!.__offset(this.bb_pos, 6);
  return offset ? this.bb!.readInt16(this.bb_pos + offset) : 0;
}

z():number {
  const offset = this.bb!.__offset(this.bb_pos, 8);
  return offset ? this.bb!.readInt16(this.bb_pos + offset) : 0;
}

static startInertialValue(builder:flatbuffers.Builder) {
  builder.startObject(3);
}

static addX(builder:flatbuffers.Builder, x:number) {
  builder.addFieldInt16(0, x, 0);
}

static addY(builder:flatbuffers.Builder, y:number) {
  builder.addFieldInt16(1, y, 0);
}

static addZ(builder:flatbuffers.Builder, z:number) {
  builder.addFieldInt16(2, z, 0);
}

static endInertialValue(builder:flatbuffers.Builder):flatbuffers.Offset {
  const offset = builder.endObject();
  return offset;
}

static finishInertialValueBuffer(builder:flatbuffers.Builder, offset:flatbuffers.Offset) {
  builder.finish(offset);
}

static finishSizePrefixedInertialValueBuffer(builder:flatbuffers.Builder, offset:flatbuffers.Offset) {
  builder.finish(offset, undefined, true);
}

static createInertialValue(builder:flatbuffers.Builder, x:number, y:number, z:number):flatbuffers.Offset {
  InertialValue.startInertialValue(builder);
  InertialValue.addX(builder, x);
  InertialValue.addY(builder, y);
  InertialValue.addZ(builder, z);
  return InertialValue.endInertialValue(builder);
}

unpack(): InertialValueT {
  return new InertialValueT(
    this.x(),
    this.y(),
    this.z()
  );
}


unpackTo(_o: InertialValueT): void {
  _o.x = this.x();
  _o.y = this.y();
  _o.z = this.z();
}
}

export class InertialValueT {
constructor(
  public x: number = 0,
  public y: number = 0,
  public z: number = 0
){}


pack(builder:flatbuffers.Builder): flatbuffers.Offset {
  return InertialValue.createInertialValue(builder,
    this.x,
    this.y,
    this.z
  );
}
}
