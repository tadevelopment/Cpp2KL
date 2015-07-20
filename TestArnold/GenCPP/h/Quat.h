#ifndef __KL2EDK_AUTOGEN_Quat__
#define __KL2EDK_AUTOGEN_Quat__

#ifdef KL2EDK_INCLUDE_MESSAGES
  #pragma message ( "Including 'Quat.h'" )
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

namespace Fabric { namespace EDK { namespace KL {

// KL struct 'Quat'
// Defined at Quat.kl:24:1

struct Quat
{
  typedef Quat &Result;
  typedef Quat const &INParam;
  typedef Quat &IOParam;
  typedef Quat &OUTParam;
  
  Vec3 v;
  Float32 w;
};

inline void Traits<Quat>::ConstructEmpty( Quat &val )
{
  Traits< Vec3 >::ConstructEmpty( val.v );
  Traits< Float32 >::ConstructEmpty( val.w );
}
inline void Traits<Quat>::ConstructCopy( Quat &lhs, Quat const &rhs )
{
  Traits< Vec3 >::ConstructCopy( lhs.v, rhs.v );
  Traits< Float32 >::ConstructCopy( lhs.w, rhs.w );
}
inline void Traits<Quat>::AssignCopy( Quat &lhs, Quat const &rhs )
{
  Traits< Vec3 >::AssignCopy( lhs.v, rhs.v );
  Traits< Float32 >::AssignCopy( lhs.w, rhs.w );
}
inline void Traits<Quat>::Destruct( Quat &val )
{
  Traits< Float32 >::Destruct( val.w );
  Traits< Vec3 >::Destruct( val.v );
}
}}}

#endif // __KL2EDK_AUTOGEN_Quat__