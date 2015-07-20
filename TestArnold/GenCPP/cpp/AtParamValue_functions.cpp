////////////////////////////////////////////////////////////////
// THIS FILE IS AUTOMATICALLY GENERATED -- DO NOT MODIFY!!
// USE COPY & PASTE TO MAKE USE OF THE FUNCTION IMPLEMENTATIONS!!
////////////////////////////////////////////////////////////////
// Generated by kl2edk version 2.1.0-alpha
////////////////////////////////////////////////////////////////

#include "AtParamValue_functions.h"

#include "ai.h"
#include "_defines.h"

using namespace Fabric::EDK;


// Defined at GenKL\\ai_params.kl:12:1
FABRIC_EXT_EXPORT Fabric::EDK::KL::UInt8 _fe_AtParamValueAsUInt8(
  Fabric::EDK::KL::Traits< Fabric::EDK::KL::AtParamValue >::INParam this_
)
{
  F2A_TRY_STATEMENT("_fe_AtParamValueAsUInt8")

  AtParamValue f2aThis_;
  if(!KlParamValue_to_AtParamValue(this_, f2aThis_)){
    setError("Error in _fe_AtParamValueAsUInt8. unable to convert: this_");
    return ;
  }
 f2aThis_.BYTE;
  F2A_CATCH_STATEMENT_RETURN("_fe_AtParamValueAsUInt8", )
}

// Defined at GenKL\\ai_params.kl:13:1
FABRIC_EXT_EXPORT Fabric::EDK::KL::UInt32 _fe_AtParamValueAsUInt32(
  Fabric::EDK::KL::Traits< Fabric::EDK::KL::AtParamValue >::INParam this_
)
{
  F2A_TRY_STATEMENT("_fe_AtParamValueAsUInt32")

  AtParamValue f2aThis_;
  if(!KlParamValue_to_AtParamValue(this_, f2aThis_)){
    setError("Error in _fe_AtParamValueAsUInt32. unable to convert: this_");
    return ;
  }
unsigned int f2a_result = f2aThis_.UINT;
  F2A_CATCH_STATEMENT_RETURN("_fe_AtParamValueAsUInt32", )
}

// Defined at GenKL\\ai_params.kl:14:1
FABRIC_EXT_EXPORT Fabric::EDK::KL::Float32 _fe_AtParamValueAsFloat32(
  Fabric::EDK::KL::Traits< Fabric::EDK::KL::AtParamValue >::INParam this_
)
{
  F2A_TRY_STATEMENT("_fe_AtParamValueAsFloat32")

  AtParamValue f2aThis_;
  if(!KlParamValue_to_AtParamValue(this_, f2aThis_)){
    setError("Error in _fe_AtParamValueAsFloat32. unable to convert: this_");
    return ;
  }
  float f2a_result = f2aThis_.fe();
  KL::Float32 _result;
  float_to_Float32(f2a_result, _result);
  return _result;

  F2A_CATCH_STATEMENT_RETURN("_fe_AtParamValueAsFloat32", )
}

// Defined at GenKL\\ai_params.kl:15:1
FABRIC_EXT_EXPORT void _fe_AtParamValueAsVec3(
  Fabric::EDK::KL::Traits< Fabric::EDK::KL::Vec3 >::Result _result,
  Fabric::EDK::KL::Traits< Fabric::EDK::KL::AtParamValue >::INParam this_
)
{
  F2A_TRY_STATEMENT("_fe_AtParamValueAsVec3")

  AtParamValue f2aThis_;
  if(!KlParamValue_to_AtParamValue(this_, f2aThis_)){
    setError("Error in _fe_AtParamValueAsVec3. unable to convert: this_");
    return;
  }
AtVector f2a_result = f2aThis_.VEC;
  F2A_CATCH_STATEMENT("_fe_AtParamValueAsVec3")
}

// Defined at GenKL\\ai_params.kl:16:1
FABRIC_EXT_EXPORT void _fe_AtParamValueAsMat44(
  Fabric::EDK::KL::Traits< Fabric::EDK::KL::Mat44 >::Result _result,
  Fabric::EDK::KL::Traits< Fabric::EDK::KL::AtParamValue >::INParam this_
)
{
  F2A_TRY_STATEMENT("_fe_AtParamValueAsMat44")

  AtParamValue f2aThis_;
  if(!KlParamValue_to_AtParamValue(this_, f2aThis_)){
    setError("Error in _fe_AtParamValueAsMat44. unable to convert: this_");
    return;
  }
AtMatrix f2a_result = *f2aThis_.pMTX;
  F2A_CATCH_STATEMENT("_fe_AtParamValueAsMat44")
}

// Defined at GenKL\\ai_params.kl:17:1
FABRIC_EXT_EXPORT void _fe_AtParamValueAsString(
  Fabric::EDK::KL::Traits< Fabric::EDK::KL::String >::Result _result,
  Fabric::EDK::KL::Traits< Fabric::EDK::KL::AtParamValue >::INParam this_
)
{
  F2A_TRY_STATEMENT("_fe_AtParamValueAsString")

  AtParamValue f2aThis_;
  if(!KlParamValue_to_AtParamValue(this_, f2aThis_)){
    setError("Error in _fe_AtParamValueAsString. unable to convert: this_");
    return;
  }
const char* f2a_result = f2aThis_.STR;
  F2A_CATCH_STATEMENT("_fe_AtParamValueAsString")
}
