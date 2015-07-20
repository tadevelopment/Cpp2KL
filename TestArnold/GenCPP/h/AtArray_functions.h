#ifndef __KL2EDK_AUTOGEN_AtArray_functions__
#define __KL2EDK_AUTOGEN_AtArray_functions__

#ifdef KL2EDK_INCLUDE_MESSAGES
  #pragma message ( "Including 'AtArray_functions.h'" )
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
#include "AtArray.h"
#include "Vec3.h"
#include "Mat44.h"
#include "Vec4.h"


// Defined at GenKL\\ai_params.kl:23:1
FABRIC_EXT_EXPORT void _fe_AtArrayAsUInt8(
  Fabric::EDK::KL::Traits< Fabric::EDK::KL::VariableArray< Fabric::EDK::KL::UInt8 > >::Result _result,
  Fabric::EDK::KL::Traits< Fabric::EDK::KL::AtArray >::INParam this_
);

// Defined at GenKL\\ai_params.kl:24:1
FABRIC_EXT_EXPORT void _fe_AtArrayAsUInt32(
  Fabric::EDK::KL::Traits< Fabric::EDK::KL::VariableArray< Fabric::EDK::KL::UInt32 > >::Result _result,
  Fabric::EDK::KL::Traits< Fabric::EDK::KL::AtArray >::INParam this_
);

// Defined at GenKL\\ai_params.kl:25:1
FABRIC_EXT_EXPORT void _fe_AtArrayAsFloat32(
  Fabric::EDK::KL::Traits< Fabric::EDK::KL::VariableArray< Fabric::EDK::KL::Float32 > >::Result _result,
  Fabric::EDK::KL::Traits< Fabric::EDK::KL::AtArray >::INParam this_
);

// Defined at GenKL\\ai_params.kl:26:1
FABRIC_EXT_EXPORT void _fe_AtArrayAsVec3(
  Fabric::EDK::KL::Traits< Fabric::EDK::KL::VariableArray< Fabric::EDK::KL::Vec3 > >::Result _result,
  Fabric::EDK::KL::Traits< Fabric::EDK::KL::AtArray >::INParam this_
);

// Defined at GenKL\\ai_params.kl:27:1
FABRIC_EXT_EXPORT void _fe_AtArrayAsMat44(
  Fabric::EDK::KL::Traits< Fabric::EDK::KL::VariableArray< Fabric::EDK::KL::Mat44 > >::Result _result,
  Fabric::EDK::KL::Traits< Fabric::EDK::KL::AtArray >::INParam this_
);

// Defined at GenKL\\ai_params.kl:28:1
FABRIC_EXT_EXPORT void _fe_AtArrayAsString(
  Fabric::EDK::KL::Traits< Fabric::EDK::KL::VariableArray< Fabric::EDK::KL::String > >::Result _result,
  Fabric::EDK::KL::Traits< Fabric::EDK::KL::AtArray >::INParam this_
);

#endif // __KL2EDK_AUTOGEN_AtArray_functions__