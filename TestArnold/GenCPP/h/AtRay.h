#ifndef __KL2EDK_AUTOGEN_AtRay__
#define __KL2EDK_AUTOGEN_AtRay__

#ifdef KL2EDK_INCLUDE_MESSAGES
  #pragma message ( "Including 'AtRay.h'" )
#endif

////////////////////////////////////////////////////////////////
// THIS FILE IS AUTOMATICALLY GENERATED -- DO NOT MODIFY!!
////////////////////////////////////////////////////////////////
// Generated by kl2edk version 2.1.0-alpha
////////////////////////////////////////////////////////////////

#include <FabricEDK.h>
#if FABRIC_EDK_VERSION_MAJ != 2 || FABRIC_EDK_VERSION_MIN != 1
# error "This file needs to be rebuilt for the current EDK version!"
#endif

#include "global.h"
#include "Vec3.h"
#include "AtShaderGlobals.h"
#include "AtBucket.h"

namespace Fabric { namespace EDK { namespace KL {

// KL struct 'AtRay'
// Defined at E:\dev\OpusTech\Cpp2KL\TestArnold\GenKL/\ai_ray.kl:10:1

struct AtRay
{
  typedef AtRay &Result;
  typedef AtRay const &INParam;
  typedef AtRay &IOParam;
  typedef AtRay &OUTParam;
  
  UInt16 type;
  UInt8 tid;
  UInt8 level;
  UInt8 diff_bounces;
  UInt8 gloss_bounces;
  UInt8 refl_bounces;
  UInt8 refr_bounces;
  SInt32 x;
  SInt32 y;
  Float32 sx;
  Float32 sy;
  Float32 px;
  Float32 py;
  Vec3 origin;
  Vec3 dir;
  Float64 mindist;
  Float64 maxdist;
  AtShaderGlobals psg;
  Data light_source;
  AtBucket bucket;
  Float32 weight;
  Float32 time;
  Vec3 dOdx;
  Vec3 dOdy;
  Vec3 dDdx;
  Vec3 dDdy;
  String traceset;
  Boolean inclusive_traceset;
  UInt16 sindex;
};

inline void Traits<AtRay>::ConstructEmpty( AtRay &val )
{
  Traits< UInt16 >::ConstructEmpty( val.type );
  Traits< UInt8 >::ConstructEmpty( val.tid );
  Traits< UInt8 >::ConstructEmpty( val.level );
  Traits< UInt8 >::ConstructEmpty( val.diff_bounces );
  Traits< UInt8 >::ConstructEmpty( val.gloss_bounces );
  Traits< UInt8 >::ConstructEmpty( val.refl_bounces );
  Traits< UInt8 >::ConstructEmpty( val.refr_bounces );
  Traits< SInt32 >::ConstructEmpty( val.x );
  Traits< SInt32 >::ConstructEmpty( val.y );
  Traits< Float32 >::ConstructEmpty( val.sx );
  Traits< Float32 >::ConstructEmpty( val.sy );
  Traits< Float32 >::ConstructEmpty( val.px );
  Traits< Float32 >::ConstructEmpty( val.py );
  Traits< Vec3 >::ConstructEmpty( val.origin );
  Traits< Vec3 >::ConstructEmpty( val.dir );
  Traits< Float64 >::ConstructEmpty( val.mindist );
  Traits< Float64 >::ConstructEmpty( val.maxdist );
  Traits< AtShaderGlobals >::ConstructEmpty( val.psg );
  Traits< Data >::ConstructEmpty( val.light_source );
  Traits< AtBucket >::ConstructEmpty( val.bucket );
  Traits< Float32 >::ConstructEmpty( val.weight );
  Traits< Float32 >::ConstructEmpty( val.time );
  Traits< Vec3 >::ConstructEmpty( val.dOdx );
  Traits< Vec3 >::ConstructEmpty( val.dOdy );
  Traits< Vec3 >::ConstructEmpty( val.dDdx );
  Traits< Vec3 >::ConstructEmpty( val.dDdy );
  Traits< String >::ConstructEmpty( val.traceset );
  Traits< Boolean >::ConstructEmpty( val.inclusive_traceset );
  Traits< UInt16 >::ConstructEmpty( val.sindex );
}
inline void Traits<AtRay>::ConstructCopy( AtRay &lhs, AtRay const &rhs )
{
  Traits< UInt16 >::ConstructCopy( lhs.type, rhs.type );
  Traits< UInt8 >::ConstructCopy( lhs.tid, rhs.tid );
  Traits< UInt8 >::ConstructCopy( lhs.level, rhs.level );
  Traits< UInt8 >::ConstructCopy( lhs.diff_bounces, rhs.diff_bounces );
  Traits< UInt8 >::ConstructCopy( lhs.gloss_bounces, rhs.gloss_bounces );
  Traits< UInt8 >::ConstructCopy( lhs.refl_bounces, rhs.refl_bounces );
  Traits< UInt8 >::ConstructCopy( lhs.refr_bounces, rhs.refr_bounces );
  Traits< SInt32 >::ConstructCopy( lhs.x, rhs.x );
  Traits< SInt32 >::ConstructCopy( lhs.y, rhs.y );
  Traits< Float32 >::ConstructCopy( lhs.sx, rhs.sx );
  Traits< Float32 >::ConstructCopy( lhs.sy, rhs.sy );
  Traits< Float32 >::ConstructCopy( lhs.px, rhs.px );
  Traits< Float32 >::ConstructCopy( lhs.py, rhs.py );
  Traits< Vec3 >::ConstructCopy( lhs.origin, rhs.origin );
  Traits< Vec3 >::ConstructCopy( lhs.dir, rhs.dir );
  Traits< Float64 >::ConstructCopy( lhs.mindist, rhs.mindist );
  Traits< Float64 >::ConstructCopy( lhs.maxdist, rhs.maxdist );
  Traits< AtShaderGlobals >::ConstructCopy( lhs.psg, rhs.psg );
  Traits< Data >::ConstructCopy( lhs.light_source, rhs.light_source );
  Traits< AtBucket >::ConstructCopy( lhs.bucket, rhs.bucket );
  Traits< Float32 >::ConstructCopy( lhs.weight, rhs.weight );
  Traits< Float32 >::ConstructCopy( lhs.time, rhs.time );
  Traits< Vec3 >::ConstructCopy( lhs.dOdx, rhs.dOdx );
  Traits< Vec3 >::ConstructCopy( lhs.dOdy, rhs.dOdy );
  Traits< Vec3 >::ConstructCopy( lhs.dDdx, rhs.dDdx );
  Traits< Vec3 >::ConstructCopy( lhs.dDdy, rhs.dDdy );
  Traits< String >::ConstructCopy( lhs.traceset, rhs.traceset );
  Traits< Boolean >::ConstructCopy( lhs.inclusive_traceset, rhs.inclusive_traceset );
  Traits< UInt16 >::ConstructCopy( lhs.sindex, rhs.sindex );
}
inline void Traits<AtRay>::AssignCopy( AtRay &lhs, AtRay const &rhs )
{
  Traits< UInt16 >::AssignCopy( lhs.type, rhs.type );
  Traits< UInt8 >::AssignCopy( lhs.tid, rhs.tid );
  Traits< UInt8 >::AssignCopy( lhs.level, rhs.level );
  Traits< UInt8 >::AssignCopy( lhs.diff_bounces, rhs.diff_bounces );
  Traits< UInt8 >::AssignCopy( lhs.gloss_bounces, rhs.gloss_bounces );
  Traits< UInt8 >::AssignCopy( lhs.refl_bounces, rhs.refl_bounces );
  Traits< UInt8 >::AssignCopy( lhs.refr_bounces, rhs.refr_bounces );
  Traits< SInt32 >::AssignCopy( lhs.x, rhs.x );
  Traits< SInt32 >::AssignCopy( lhs.y, rhs.y );
  Traits< Float32 >::AssignCopy( lhs.sx, rhs.sx );
  Traits< Float32 >::AssignCopy( lhs.sy, rhs.sy );
  Traits< Float32 >::AssignCopy( lhs.px, rhs.px );
  Traits< Float32 >::AssignCopy( lhs.py, rhs.py );
  Traits< Vec3 >::AssignCopy( lhs.origin, rhs.origin );
  Traits< Vec3 >::AssignCopy( lhs.dir, rhs.dir );
  Traits< Float64 >::AssignCopy( lhs.mindist, rhs.mindist );
  Traits< Float64 >::AssignCopy( lhs.maxdist, rhs.maxdist );
  Traits< AtShaderGlobals >::AssignCopy( lhs.psg, rhs.psg );
  Traits< Data >::AssignCopy( lhs.light_source, rhs.light_source );
  Traits< AtBucket >::AssignCopy( lhs.bucket, rhs.bucket );
  Traits< Float32 >::AssignCopy( lhs.weight, rhs.weight );
  Traits< Float32 >::AssignCopy( lhs.time, rhs.time );
  Traits< Vec3 >::AssignCopy( lhs.dOdx, rhs.dOdx );
  Traits< Vec3 >::AssignCopy( lhs.dOdy, rhs.dOdy );
  Traits< Vec3 >::AssignCopy( lhs.dDdx, rhs.dDdx );
  Traits< Vec3 >::AssignCopy( lhs.dDdy, rhs.dDdy );
  Traits< String >::AssignCopy( lhs.traceset, rhs.traceset );
  Traits< Boolean >::AssignCopy( lhs.inclusive_traceset, rhs.inclusive_traceset );
  Traits< UInt16 >::AssignCopy( lhs.sindex, rhs.sindex );
}
inline void Traits<AtRay>::Destruct( AtRay &val )
{
  Traits< UInt16 >::Destruct( val.sindex );
  Traits< Boolean >::Destruct( val.inclusive_traceset );
  Traits< String >::Destruct( val.traceset );
  Traits< Vec3 >::Destruct( val.dDdy );
  Traits< Vec3 >::Destruct( val.dDdx );
  Traits< Vec3 >::Destruct( val.dOdy );
  Traits< Vec3 >::Destruct( val.dOdx );
  Traits< Float32 >::Destruct( val.time );
  Traits< Float32 >::Destruct( val.weight );
  Traits< AtBucket >::Destruct( val.bucket );
  Traits< Data >::Destruct( val.light_source );
  Traits< AtShaderGlobals >::Destruct( val.psg );
  Traits< Float64 >::Destruct( val.maxdist );
  Traits< Float64 >::Destruct( val.mindist );
  Traits< Vec3 >::Destruct( val.dir );
  Traits< Vec3 >::Destruct( val.origin );
  Traits< Float32 >::Destruct( val.py );
  Traits< Float32 >::Destruct( val.px );
  Traits< Float32 >::Destruct( val.sy );
  Traits< Float32 >::Destruct( val.sx );
  Traits< SInt32 >::Destruct( val.y );
  Traits< SInt32 >::Destruct( val.x );
  Traits< UInt8 >::Destruct( val.refr_bounces );
  Traits< UInt8 >::Destruct( val.refl_bounces );
  Traits< UInt8 >::Destruct( val.gloss_bounces );
  Traits< UInt8 >::Destruct( val.diff_bounces );
  Traits< UInt8 >::Destruct( val.level );
  Traits< UInt8 >::Destruct( val.tid );
  Traits< UInt16 >::Destruct( val.type );
}
}}}

#endif // __KL2EDK_AUTOGEN_AtRay__
