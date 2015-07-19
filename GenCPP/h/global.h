#ifndef __KL2EDK_AUTOGEN_global__
#define __KL2EDK_AUTOGEN_global__

#ifdef KL2EDK_INCLUDE_MESSAGES
  #pragma message ( "Including 'global.h'" )
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

// Dependencies on other extensions
#define FABRIC_EDK_EXT_Fabric2Arnold_DEPENDENT_EXTS \
  { \
    { "Math", 1, 0, 1, 0 }, \
    { 0, 0, 0, 0, 0 } \
  }

// forward declarations
namespace Fabric { namespace EDK { namespace KL {
  class Object;
  struct ARGB;
  struct AtAOVEntry;
  struct AtAOVIterator;
  struct AtArray;
  struct AtCameraInput;
  struct AtCameraOutput;
  struct AtLicenseInfo;
  struct AtMetaDataEntry;
  struct AtMetaDataIterator;
  struct AtMetaDataStore;
  struct AtNode;
  struct AtNodeEntry;
  struct AtNodeEntryIterator;
  struct AtNodeIterator;
  struct AtNodeLib;
  struct AtNodeMethods;
  struct AtParamEntry;
  struct AtParamIterator;
  struct AtParamValue;
  struct AtRay;
  struct AtScrSample;
  struct AtShaderGlobals;
  struct AtTextureHandle;
  struct AtTextureParams;
  struct AtUserParamEntry;
  struct AtUserParamIterator;
  struct Box2;
  struct Box3;
  struct Color;
  struct Euler;
  struct Mat22;
  struct Mat33;
  struct Mat44;
  struct Quat;
  struct RGB;
  struct RGBA;
  struct Ray;
  struct RotationOrder;
  struct Vec2;
  struct Vec3;
  struct Vec3_d;
  struct Vec4;
  struct Xfo;
}}}

#include "aliases.h"

namespace Fabric { namespace EDK { namespace KL {

// KL interface 'Object'
// Defined at (internal)

class Object
{
public:
  
  struct VTable
  {
  };
  
  struct Bits
  {
    ObjectCore *objectCorePtr;
    SwapPtr<VTable const> const *vTableSwapPtrPtr;
  } *m_bits;
  
protected:
  
  friend struct Traits< Object >;
  
  static void ConstructEmpty( Object *self )
  {
    self->m_bits = 0;
  }
  
  static void ConstructCopy( Object *self, Object const *other )
  {
    if ( (self->m_bits = other->m_bits) )
      AtomicUInt32Increment( &self->m_bits->objectCorePtr->refCount );
  }
  
  static void AssignCopy( Object *self, Object const *other )
  {
    if ( self->m_bits != other->m_bits )
    {
      Destruct( self );
      ConstructCopy( self, other );
    }
  }
  
  static void Destruct( Object *self )
  {
    if ( self->m_bits
      && AtomicUInt32DecrementAndGetValue( &self->m_bits->objectCorePtr->refCount ) == 0 )
    {
      self->m_bits->objectCorePtr->lTableSwapPtrPtr->get()->lifecycleDestroy(
        &self->m_bits->objectCorePtr
        );
    }
  }
  
public: 
  
  typedef Object &Result;
  typedef Object const &INParam;
  typedef Object &IOParam;
  typedef Object &OUTParam;
  
  Object()
  {
    ConstructEmpty( this );
  }
  
  Object( Object const &that )
  {
    ConstructCopy( this, &that );
  }
  
  Object &operator =( Object const &that )
  {
    AssignCopy( this, &that );
    return *this;
  }
  
  ~Object()
  {
    Destruct( this );
  }
  
  void appendDesc( String::IOParam string ) const
  {
    if ( m_bits )
      m_bits->objectCorePtr->lTableSwapPtrPtr->get()->appendDesc( &m_bits->objectCorePtr, string );
    else string.append( "null", 4 );
  }
  
  bool isValid() const
  {
    return !!m_bits;
  }
  
  operator bool() const
  {
    return isValid();
  }
  
  bool operator !() const
  {
    return !isValid();
  }
  
  bool operator ==( INParam that )
  {
    return m_bits == that.m_bits;
  }
  
  bool operator !=( INParam that )
  {
    return m_bits != that.m_bits;
  }
  
};

template<>
struct Traits< Object >
{
  typedef Object &Result;
  typedef Object const &INParam;
  typedef Object &IOParam;
  typedef Object &OUTParam;
  
  static void ConstructEmpty( Object &val );
  static void ConstructCopy( Object &lhs, Object const &rhs );
  static void AssignCopy( Object &lhs, Object const &rhs );
  static void Destruct( Object &val );
};

inline void Traits<Object>::ConstructEmpty( Object &val )
{
  Object::ConstructEmpty( &val );
}
inline void Traits<Object>::ConstructCopy( Object &lhs, Object const &rhs )
{
  Object::ConstructCopy( &lhs, &rhs );
}
inline void Traits<Object>::AssignCopy( Object &lhs, Object const &rhs )
{
  Object::AssignCopy( &lhs, &rhs );
}
inline void Traits<Object>::Destruct( Object &val )
{
  Object::Destruct( &val );
}

template<>
struct Traits< RGB >
{
  typedef RGB &Result;
  typedef RGB const &INParam;
  typedef RGB &IOParam;
  typedef RGB &OUTParam;
  
  static void ConstructEmpty( RGB &val );
  static void ConstructCopy( RGB &lhs, RGB const &rhs );
  static void AssignCopy( RGB &lhs, RGB const &rhs );
  static void Destruct( RGB &val );
};

template<>
struct Traits< RGBA >
{
  typedef RGBA &Result;
  typedef RGBA const &INParam;
  typedef RGBA &IOParam;
  typedef RGBA &OUTParam;
  
  static void ConstructEmpty( RGBA &val );
  static void ConstructCopy( RGBA &lhs, RGBA const &rhs );
  static void AssignCopy( RGBA &lhs, RGBA const &rhs );
  static void Destruct( RGBA &val );
};

template<>
struct Traits< ARGB >
{
  typedef ARGB &Result;
  typedef ARGB const &INParam;
  typedef ARGB &IOParam;
  typedef ARGB &OUTParam;
  
  static void ConstructEmpty( ARGB &val );
  static void ConstructCopy( ARGB &lhs, ARGB const &rhs );
  static void AssignCopy( ARGB &lhs, ARGB const &rhs );
  static void Destruct( ARGB &val );
};

template<>
struct Traits< Color >
{
  typedef Color &Result;
  typedef Color const &INParam;
  typedef Color &IOParam;
  typedef Color &OUTParam;
  
  static void ConstructEmpty( Color &val );
  static void ConstructCopy( Color &lhs, Color const &rhs );
  static void AssignCopy( Color &lhs, Color const &rhs );
  static void Destruct( Color &val );
};

template<>
struct Traits< Vec2 >
{
  typedef Vec2 &Result;
  typedef Vec2 const &INParam;
  typedef Vec2 &IOParam;
  typedef Vec2 &OUTParam;
  
  static void ConstructEmpty( Vec2 &val );
  static void ConstructCopy( Vec2 &lhs, Vec2 const &rhs );
  static void AssignCopy( Vec2 &lhs, Vec2 const &rhs );
  static void Destruct( Vec2 &val );
};

template<>
struct Traits< Vec3 >
{
  typedef Vec3 &Result;
  typedef Vec3 const &INParam;
  typedef Vec3 &IOParam;
  typedef Vec3 &OUTParam;
  
  static void ConstructEmpty( Vec3 &val );
  static void ConstructCopy( Vec3 &lhs, Vec3 const &rhs );
  static void AssignCopy( Vec3 &lhs, Vec3 const &rhs );
  static void Destruct( Vec3 &val );
};

template<>
struct Traits< Vec3_d >
{
  typedef Vec3_d &Result;
  typedef Vec3_d const &INParam;
  typedef Vec3_d &IOParam;
  typedef Vec3_d &OUTParam;
  
  static void ConstructEmpty( Vec3_d &val );
  static void ConstructCopy( Vec3_d &lhs, Vec3_d const &rhs );
  static void AssignCopy( Vec3_d &lhs, Vec3_d const &rhs );
  static void Destruct( Vec3_d &val );
};

template<>
struct Traits< Vec4 >
{
  typedef Vec4 &Result;
  typedef Vec4 const &INParam;
  typedef Vec4 &IOParam;
  typedef Vec4 &OUTParam;
  
  static void ConstructEmpty( Vec4 &val );
  static void ConstructCopy( Vec4 &lhs, Vec4 const &rhs );
  static void AssignCopy( Vec4 &lhs, Vec4 const &rhs );
  static void Destruct( Vec4 &val );
};

template<>
struct Traits< Ray >
{
  typedef Ray &Result;
  typedef Ray const &INParam;
  typedef Ray &IOParam;
  typedef Ray &OUTParam;
  
  static void ConstructEmpty( Ray &val );
  static void ConstructCopy( Ray &lhs, Ray const &rhs );
  static void AssignCopy( Ray &lhs, Ray const &rhs );
  static void Destruct( Ray &val );
};

template<>
struct Traits< Mat22 >
{
  typedef Mat22 &Result;
  typedef Mat22 const &INParam;
  typedef Mat22 &IOParam;
  typedef Mat22 &OUTParam;
  
  static void ConstructEmpty( Mat22 &val );
  static void ConstructCopy( Mat22 &lhs, Mat22 const &rhs );
  static void AssignCopy( Mat22 &lhs, Mat22 const &rhs );
  static void Destruct( Mat22 &val );
};

template<>
struct Traits< Mat33 >
{
  typedef Mat33 &Result;
  typedef Mat33 const &INParam;
  typedef Mat33 &IOParam;
  typedef Mat33 &OUTParam;
  
  static void ConstructEmpty( Mat33 &val );
  static void ConstructCopy( Mat33 &lhs, Mat33 const &rhs );
  static void AssignCopy( Mat33 &lhs, Mat33 const &rhs );
  static void Destruct( Mat33 &val );
};

template<>
struct Traits< Mat44 >
{
  typedef Mat44 &Result;
  typedef Mat44 const &INParam;
  typedef Mat44 &IOParam;
  typedef Mat44 &OUTParam;
  
  static void ConstructEmpty( Mat44 &val );
  static void ConstructCopy( Mat44 &lhs, Mat44 const &rhs );
  static void AssignCopy( Mat44 &lhs, Mat44 const &rhs );
  static void Destruct( Mat44 &val );
};

template<>
struct Traits< Box2 >
{
  typedef Box2 &Result;
  typedef Box2 const &INParam;
  typedef Box2 &IOParam;
  typedef Box2 &OUTParam;
  
  static void ConstructEmpty( Box2 &val );
  static void ConstructCopy( Box2 &lhs, Box2 const &rhs );
  static void AssignCopy( Box2 &lhs, Box2 const &rhs );
  static void Destruct( Box2 &val );
};

template<>
struct Traits< Box3 >
{
  typedef Box3 &Result;
  typedef Box3 const &INParam;
  typedef Box3 &IOParam;
  typedef Box3 &OUTParam;
  
  static void ConstructEmpty( Box3 &val );
  static void ConstructCopy( Box3 &lhs, Box3 const &rhs );
  static void AssignCopy( Box3 &lhs, Box3 const &rhs );
  static void Destruct( Box3 &val );
};

template<>
struct Traits< RotationOrder >
{
  typedef RotationOrder &Result;
  typedef RotationOrder const &INParam;
  typedef RotationOrder &IOParam;
  typedef RotationOrder &OUTParam;
  
  static void ConstructEmpty( RotationOrder &val );
  static void ConstructCopy( RotationOrder &lhs, RotationOrder const &rhs );
  static void AssignCopy( RotationOrder &lhs, RotationOrder const &rhs );
  static void Destruct( RotationOrder &val );
};

template<>
struct Traits< Euler >
{
  typedef Euler &Result;
  typedef Euler const &INParam;
  typedef Euler &IOParam;
  typedef Euler &OUTParam;
  
  static void ConstructEmpty( Euler &val );
  static void ConstructCopy( Euler &lhs, Euler const &rhs );
  static void AssignCopy( Euler &lhs, Euler const &rhs );
  static void Destruct( Euler &val );
};

template<>
struct Traits< Quat >
{
  typedef Quat &Result;
  typedef Quat const &INParam;
  typedef Quat &IOParam;
  typedef Quat &OUTParam;
  
  static void ConstructEmpty( Quat &val );
  static void ConstructCopy( Quat &lhs, Quat const &rhs );
  static void AssignCopy( Quat &lhs, Quat const &rhs );
  static void Destruct( Quat &val );
};

template<>
struct Traits< Xfo >
{
  typedef Xfo &Result;
  typedef Xfo const &INParam;
  typedef Xfo &IOParam;
  typedef Xfo &OUTParam;
  
  static void ConstructEmpty( Xfo &val );
  static void ConstructCopy( Xfo &lhs, Xfo const &rhs );
  static void AssignCopy( Xfo &lhs, Xfo const &rhs );
  static void Destruct( Xfo &val );
};

template<>
struct Traits< AtParamValue >
{
  typedef AtParamValue &Result;
  typedef AtParamValue const &INParam;
  typedef AtParamValue &IOParam;
  typedef AtParamValue &OUTParam;
  
  static void ConstructEmpty( AtParamValue &val );
  static void ConstructCopy( AtParamValue &lhs, AtParamValue const &rhs );
  static void AssignCopy( AtParamValue &lhs, AtParamValue const &rhs );
  static void Destruct( AtParamValue &val );
};

template<>
struct Traits< AtArray >
{
  typedef AtArray &Result;
  typedef AtArray const &INParam;
  typedef AtArray &IOParam;
  typedef AtArray &OUTParam;
  
  static void ConstructEmpty( AtArray &val );
  static void ConstructCopy( AtArray &lhs, AtArray const &rhs );
  static void AssignCopy( AtArray &lhs, AtArray const &rhs );
  static void Destruct( AtArray &val );
};

template<>
struct Traits< AtParamEntry >
{
  typedef AtParamEntry &Result;
  typedef AtParamEntry const &INParam;
  typedef AtParamEntry &IOParam;
  typedef AtParamEntry &OUTParam;
  
  static void ConstructEmpty( AtParamEntry &val );
  static void ConstructCopy( AtParamEntry &lhs, AtParamEntry const &rhs );
  static void AssignCopy( AtParamEntry &lhs, AtParamEntry const &rhs );
  static void Destruct( AtParamEntry &val );
};

template<>
struct Traits< AtUserParamEntry >
{
  typedef AtUserParamEntry &Result;
  typedef AtUserParamEntry const &INParam;
  typedef AtUserParamEntry &IOParam;
  typedef AtUserParamEntry &OUTParam;
  
  static void ConstructEmpty( AtUserParamEntry &val );
  static void ConstructCopy( AtUserParamEntry &lhs, AtUserParamEntry const &rhs );
  static void AssignCopy( AtUserParamEntry &lhs, AtUserParamEntry const &rhs );
  static void Destruct( AtUserParamEntry &val );
};

template<>
struct Traits< AtCameraInput >
{
  typedef AtCameraInput &Result;
  typedef AtCameraInput const &INParam;
  typedef AtCameraInput &IOParam;
  typedef AtCameraInput &OUTParam;
  
  static void ConstructEmpty( AtCameraInput &val );
  static void ConstructCopy( AtCameraInput &lhs, AtCameraInput const &rhs );
  static void AssignCopy( AtCameraInput &lhs, AtCameraInput const &rhs );
  static void Destruct( AtCameraInput &val );
};

template<>
struct Traits< AtCameraOutput >
{
  typedef AtCameraOutput &Result;
  typedef AtCameraOutput const &INParam;
  typedef AtCameraOutput &IOParam;
  typedef AtCameraOutput &OUTParam;
  
  static void ConstructEmpty( AtCameraOutput &val );
  static void ConstructCopy( AtCameraOutput &lhs, AtCameraOutput const &rhs );
  static void AssignCopy( AtCameraOutput &lhs, AtCameraOutput const &rhs );
  static void Destruct( AtCameraOutput &val );
};

template<>
struct Traits< AtLicenseInfo >
{
  typedef AtLicenseInfo &Result;
  typedef AtLicenseInfo const &INParam;
  typedef AtLicenseInfo &IOParam;
  typedef AtLicenseInfo &OUTParam;
  
  static void ConstructEmpty( AtLicenseInfo &val );
  static void ConstructCopy( AtLicenseInfo &lhs, AtLicenseInfo const &rhs );
  static void AssignCopy( AtLicenseInfo &lhs, AtLicenseInfo const &rhs );
  static void Destruct( AtLicenseInfo &val );
};

template<>
struct Traits< AtMetaDataStore >
{
  typedef AtMetaDataStore &Result;
  typedef AtMetaDataStore const &INParam;
  typedef AtMetaDataStore &IOParam;
  typedef AtMetaDataStore &OUTParam;
  
  static void ConstructEmpty( AtMetaDataStore &val );
  static void ConstructCopy( AtMetaDataStore &lhs, AtMetaDataStore const &rhs );
  static void AssignCopy( AtMetaDataStore &lhs, AtMetaDataStore const &rhs );
  static void Destruct( AtMetaDataStore &val );
};

template<>
struct Traits< AtNodeEntry >
{
  typedef AtNodeEntry &Result;
  typedef AtNodeEntry const &INParam;
  typedef AtNodeEntry &IOParam;
  typedef AtNodeEntry &OUTParam;
  
  static void ConstructEmpty( AtNodeEntry &val );
  static void ConstructCopy( AtNodeEntry &lhs, AtNodeEntry const &rhs );
  static void AssignCopy( AtNodeEntry &lhs, AtNodeEntry const &rhs );
  static void Destruct( AtNodeEntry &val );
};

template<>
struct Traits< AtNodeMethods >
{
  typedef AtNodeMethods &Result;
  typedef AtNodeMethods const &INParam;
  typedef AtNodeMethods &IOParam;
  typedef AtNodeMethods &OUTParam;
  
  static void ConstructEmpty( AtNodeMethods &val );
  static void ConstructCopy( AtNodeMethods &lhs, AtNodeMethods const &rhs );
  static void AssignCopy( AtNodeMethods &lhs, AtNodeMethods const &rhs );
  static void Destruct( AtNodeMethods &val );
};

template<>
struct Traits< AtParamIterator >
{
  typedef AtParamIterator &Result;
  typedef AtParamIterator const &INParam;
  typedef AtParamIterator &IOParam;
  typedef AtParamIterator &OUTParam;
  
  static void ConstructEmpty( AtParamIterator &val );
  static void ConstructCopy( AtParamIterator &lhs, AtParamIterator const &rhs );
  static void AssignCopy( AtParamIterator &lhs, AtParamIterator const &rhs );
  static void Destruct( AtParamIterator &val );
};

template<>
struct Traits< AtMetaDataIterator >
{
  typedef AtMetaDataIterator &Result;
  typedef AtMetaDataIterator const &INParam;
  typedef AtMetaDataIterator &IOParam;
  typedef AtMetaDataIterator &OUTParam;
  
  static void ConstructEmpty( AtMetaDataIterator &val );
  static void ConstructCopy( AtMetaDataIterator &lhs, AtMetaDataIterator const &rhs );
  static void AssignCopy( AtMetaDataIterator &lhs, AtMetaDataIterator const &rhs );
  static void Destruct( AtMetaDataIterator &val );
};

template<>
struct Traits< AtMetaDataEntry >
{
  typedef AtMetaDataEntry &Result;
  typedef AtMetaDataEntry const &INParam;
  typedef AtMetaDataEntry &IOParam;
  typedef AtMetaDataEntry &OUTParam;
  
  static void ConstructEmpty( AtMetaDataEntry &val );
  static void ConstructCopy( AtMetaDataEntry &lhs, AtMetaDataEntry const &rhs );
  static void AssignCopy( AtMetaDataEntry &lhs, AtMetaDataEntry const &rhs );
  static void Destruct( AtMetaDataEntry &val );
};

template<>
struct Traits< AtNode >
{
  typedef AtNode &Result;
  typedef AtNode const &INParam;
  typedef AtNode &IOParam;
  typedef AtNode &OUTParam;
  
  static void ConstructEmpty( AtNode &val );
  static void ConstructCopy( AtNode &lhs, AtNode const &rhs );
  static void AssignCopy( AtNode &lhs, AtNode const &rhs );
  static void Destruct( AtNode &val );
};

template<>
struct Traits< AtUserParamIterator >
{
  typedef AtUserParamIterator &Result;
  typedef AtUserParamIterator const &INParam;
  typedef AtUserParamIterator &IOParam;
  typedef AtUserParamIterator &OUTParam;
  
  static void ConstructEmpty( AtUserParamIterator &val );
  static void ConstructCopy( AtUserParamIterator &lhs, AtUserParamIterator const &rhs );
  static void AssignCopy( AtUserParamIterator &lhs, AtUserParamIterator const &rhs );
  static void Destruct( AtUserParamIterator &val );
};

template<>
struct Traits< AtNodeLib >
{
  typedef AtNodeLib &Result;
  typedef AtNodeLib const &INParam;
  typedef AtNodeLib &IOParam;
  typedef AtNodeLib &OUTParam;
  
  static void ConstructEmpty( AtNodeLib &val );
  static void ConstructCopy( AtNodeLib &lhs, AtNodeLib const &rhs );
  static void AssignCopy( AtNodeLib &lhs, AtNodeLib const &rhs );
  static void Destruct( AtNodeLib &val );
};

template<>
struct Traits< AtShaderGlobals >
{
  typedef AtShaderGlobals &Result;
  typedef AtShaderGlobals const &INParam;
  typedef AtShaderGlobals &IOParam;
  typedef AtShaderGlobals &OUTParam;
  
  static void ConstructEmpty( AtShaderGlobals &val );
  static void ConstructCopy( AtShaderGlobals &lhs, AtShaderGlobals const &rhs );
  static void AssignCopy( AtShaderGlobals &lhs, AtShaderGlobals const &rhs );
  static void Destruct( AtShaderGlobals &val );
};

template<>
struct Traits< AtScrSample >
{
  typedef AtScrSample &Result;
  typedef AtScrSample const &INParam;
  typedef AtScrSample &IOParam;
  typedef AtScrSample &OUTParam;
  
  static void ConstructEmpty( AtScrSample &val );
  static void ConstructCopy( AtScrSample &lhs, AtScrSample const &rhs );
  static void AssignCopy( AtScrSample &lhs, AtScrSample const &rhs );
  static void Destruct( AtScrSample &val );
};

template<>
struct Traits< AtRay >
{
  typedef AtRay &Result;
  typedef AtRay const &INParam;
  typedef AtRay &IOParam;
  typedef AtRay &OUTParam;
  
  static void ConstructEmpty( AtRay &val );
  static void ConstructCopy( AtRay &lhs, AtRay const &rhs );
  static void AssignCopy( AtRay &lhs, AtRay const &rhs );
  static void Destruct( AtRay &val );
};

template<>
struct Traits< AtTextureHandle >
{
  typedef AtTextureHandle &Result;
  typedef AtTextureHandle const &INParam;
  typedef AtTextureHandle &IOParam;
  typedef AtTextureHandle &OUTParam;
  
  static void ConstructEmpty( AtTextureHandle &val );
  static void ConstructCopy( AtTextureHandle &lhs, AtTextureHandle const &rhs );
  static void AssignCopy( AtTextureHandle &lhs, AtTextureHandle const &rhs );
  static void Destruct( AtTextureHandle &val );
};

template<>
struct Traits< AtTextureParams >
{
  typedef AtTextureParams &Result;
  typedef AtTextureParams const &INParam;
  typedef AtTextureParams &IOParam;
  typedef AtTextureParams &OUTParam;
  
  static void ConstructEmpty( AtTextureParams &val );
  static void ConstructCopy( AtTextureParams &lhs, AtTextureParams const &rhs );
  static void AssignCopy( AtTextureParams &lhs, AtTextureParams const &rhs );
  static void Destruct( AtTextureParams &val );
};

template<>
struct Traits< AtNodeIterator >
{
  typedef AtNodeIterator &Result;
  typedef AtNodeIterator const &INParam;
  typedef AtNodeIterator &IOParam;
  typedef AtNodeIterator &OUTParam;
  
  static void ConstructEmpty( AtNodeIterator &val );
  static void ConstructCopy( AtNodeIterator &lhs, AtNodeIterator const &rhs );
  static void AssignCopy( AtNodeIterator &lhs, AtNodeIterator const &rhs );
  static void Destruct( AtNodeIterator &val );
};

template<>
struct Traits< AtNodeEntryIterator >
{
  typedef AtNodeEntryIterator &Result;
  typedef AtNodeEntryIterator const &INParam;
  typedef AtNodeEntryIterator &IOParam;
  typedef AtNodeEntryIterator &OUTParam;
  
  static void ConstructEmpty( AtNodeEntryIterator &val );
  static void ConstructCopy( AtNodeEntryIterator &lhs, AtNodeEntryIterator const &rhs );
  static void AssignCopy( AtNodeEntryIterator &lhs, AtNodeEntryIterator const &rhs );
  static void Destruct( AtNodeEntryIterator &val );
};

template<>
struct Traits< AtAOVIterator >
{
  typedef AtAOVIterator &Result;
  typedef AtAOVIterator const &INParam;
  typedef AtAOVIterator &IOParam;
  typedef AtAOVIterator &OUTParam;
  
  static void ConstructEmpty( AtAOVIterator &val );
  static void ConstructCopy( AtAOVIterator &lhs, AtAOVIterator const &rhs );
  static void AssignCopy( AtAOVIterator &lhs, AtAOVIterator const &rhs );
  static void Destruct( AtAOVIterator &val );
};

template<>
struct Traits< AtAOVEntry >
{
  typedef AtAOVEntry &Result;
  typedef AtAOVEntry const &INParam;
  typedef AtAOVEntry &IOParam;
  typedef AtAOVEntry &OUTParam;
  
  static void ConstructEmpty( AtAOVEntry &val );
  static void ConstructCopy( AtAOVEntry &lhs, AtAOVEntry const &rhs );
  static void AssignCopy( AtAOVEntry &lhs, AtAOVEntry const &rhs );
  static void Destruct( AtAOVEntry &val );
};

}}}

#endif // __KL2EDK_AUTOGEN_global__
