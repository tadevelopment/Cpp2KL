#ifndef __KL2EDK_AUTOGEN_AtNodeMethods__
#define __KL2EDK_AUTOGEN_AtNodeMethods__

#ifdef KL2EDK_INCLUDE_MESSAGES
  #pragma message ( "Including 'AtNodeMethods.h'" )
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

namespace Fabric { namespace EDK { namespace KL {

// KL struct 'AtNodeMethods'
// Defined at GenKL\\_opaque_types.kl:24:1

struct AtNodeMethods
{
  typedef AtNodeMethods &Result;
  typedef AtNodeMethods const &INParam;
  typedef AtNodeMethods &IOParam;
  typedef AtNodeMethods &OUTParam;
  
  Data _handle;
};

inline void Traits<AtNodeMethods>::ConstructEmpty( AtNodeMethods &val )
{
  Traits< Data >::ConstructEmpty( val._handle );
}
inline void Traits<AtNodeMethods>::ConstructCopy( AtNodeMethods &lhs, AtNodeMethods const &rhs )
{
  Traits< Data >::ConstructCopy( lhs._handle, rhs._handle );
}
inline void Traits<AtNodeMethods>::AssignCopy( AtNodeMethods &lhs, AtNodeMethods const &rhs )
{
  Traits< Data >::AssignCopy( lhs._handle, rhs._handle );
}
inline void Traits<AtNodeMethods>::Destruct( AtNodeMethods &val )
{
  Traits< Data >::Destruct( val._handle );
}
}}}

#endif // __KL2EDK_AUTOGEN_AtNodeMethods__
