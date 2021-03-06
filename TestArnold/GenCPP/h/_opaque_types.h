/* 
 * This auto-generated file contains simple conversion fn
 * declarations for the opaque data-types found in Fabric2Arnold
 *  - Do not modify this file, it will be overwritten
 */

#pragma once

#include "AtBucket.h"
inline bool KLAtBucket_to_CPAtBucket(const Fabric::EDK::KL::AtBucket & from, AtBucket* & to) {
  to = reinterpret_cast<AtBucket*>(from._handle); 
  return true; 
}

inline bool CPAtBucket_to_KLAtBucket(const AtBucket* const& from, Fabric::EDK::KL::AtBucket & to) {
  to._handle = const_cast<AtBucket*>(from); 
  return true; 
}

#include "AtList.h"
inline bool KLAtList_to_CPAtList(const Fabric::EDK::KL::AtList & from, AtList* & to) {
  to = reinterpret_cast<AtList*>(from._handle); 
  return true; 
}

inline bool CPAtList_to_KLAtList(const AtList* const& from, Fabric::EDK::KL::AtList & to) {
  to._handle = const_cast<AtList*>(from); 
  return true; 
}

#include "AtNode.h"
inline bool KLAtNode_to_CPAtNode(const Fabric::EDK::KL::AtNode & from, AtNode* & to) {
  to = reinterpret_cast<AtNode*>(from._handle); 
  return true; 
}

inline bool CPAtNode_to_KLAtNode(const AtNode* const& from, Fabric::EDK::KL::AtNode & to) {
  to._handle = const_cast<AtNode*>(from); 
  return true; 
}

#include "AtNodeEntry.h"
inline bool KLAtNodeEntry_to_CPAtNodeEntry(const Fabric::EDK::KL::AtNodeEntry & from, AtNodeEntry* & to) {
  to = reinterpret_cast<AtNodeEntry*>(from._handle); 
  return true; 
}

inline bool CPAtNodeEntry_to_KLAtNodeEntry(const AtNodeEntry* const& from, Fabric::EDK::KL::AtNodeEntry & to) {
  to._handle = const_cast<AtNodeEntry*>(from); 
  return true; 
}

#include "AtNodeMethods.h"
inline bool KLAtNodeMethods_to_CPAtNodeMethods(const Fabric::EDK::KL::AtNodeMethods & from, AtNodeMethods* & to) {
  to = reinterpret_cast<AtNodeMethods*>(from._handle); 
  return true; 
}

inline bool CPAtNodeMethods_to_KLAtNodeMethods(const AtNodeMethods* const& from, Fabric::EDK::KL::AtNodeMethods & to) {
  to._handle = const_cast<AtNodeMethods*>(from); 
  return true; 
}

#include "AtParamIterator.h"
inline bool KLAtParamIterator_to_CPAtParamIterator(const Fabric::EDK::KL::AtParamIterator & from, AtParamIterator* & to) {
  to = reinterpret_cast<AtParamIterator*>(from._handle); 
  return true; 
}

inline bool CPAtParamIterator_to_KLAtParamIterator(const AtParamIterator* const& from, Fabric::EDK::KL::AtParamIterator & to) {
  to._handle = const_cast<AtParamIterator*>(from); 
  return true; 
}

#include "AtMetaDataIterator.h"
inline bool KLAtMetaDataIterator_to_CPAtMetaDataIterator(const Fabric::EDK::KL::AtMetaDataIterator & from, AtMetaDataIterator* & to) {
  to = reinterpret_cast<AtMetaDataIterator*>(from._handle); 
  return true; 
}

inline bool CPAtMetaDataIterator_to_KLAtMetaDataIterator(const AtMetaDataIterator* const& from, Fabric::EDK::KL::AtMetaDataIterator & to) {
  to._handle = const_cast<AtMetaDataIterator*>(from); 
  return true; 
}

#include "AtUserParamIterator.h"
inline bool KLAtUserParamIterator_to_CPAtUserParamIterator(const Fabric::EDK::KL::AtUserParamIterator & from, AtUserParamIterator* & to) {
  to = reinterpret_cast<AtUserParamIterator*>(from._handle); 
  return true; 
}

inline bool CPAtUserParamIterator_to_KLAtUserParamIterator(const AtUserParamIterator* const& from, Fabric::EDK::KL::AtUserParamIterator & to) {
  to._handle = const_cast<AtUserParamIterator*>(from); 
  return true; 
}

#include "AtTextureHandle.h"
inline bool KLAtTextureHandle_to_CPAtTextureHandle(const Fabric::EDK::KL::AtTextureHandle & from, AtTextureHandle* & to) {
  to = reinterpret_cast<AtTextureHandle*>(from._handle); 
  return true; 
}

inline bool CPAtTextureHandle_to_KLAtTextureHandle(const AtTextureHandle* const& from, Fabric::EDK::KL::AtTextureHandle & to) {
  to._handle = const_cast<AtTextureHandle*>(from); 
  return true; 
}

#include "AtShaderGlobals.h"
inline bool KLAtShaderGlobals_to_CPAtShaderGlobals(const Fabric::EDK::KL::AtShaderGlobals & from, AtShaderGlobals* & to) {
  to = reinterpret_cast<AtShaderGlobals*>(from._handle); 
  return true; 
}

inline bool CPAtShaderGlobals_to_KLAtShaderGlobals(const AtShaderGlobals* const& from, Fabric::EDK::KL::AtShaderGlobals & to) {
  to._handle = const_cast<AtShaderGlobals*>(from); 
  return true; 
}

#include "AtScrSample.h"
inline bool KLAtScrSample_to_CPAtScrSample(const Fabric::EDK::KL::AtScrSample & from, AtScrSample* & to) {
  to = reinterpret_cast<AtScrSample*>(from._handle); 
  return true; 
}

inline bool CPAtScrSample_to_KLAtScrSample(const AtScrSample* const& from, Fabric::EDK::KL::AtScrSample & to) {
  to._handle = const_cast<AtScrSample*>(from); 
  return true; 
}

#include "AtNodeIterator.h"
inline bool KLAtNodeIterator_to_CPAtNodeIterator(const Fabric::EDK::KL::AtNodeIterator & from, AtNodeIterator* & to) {
  to = reinterpret_cast<AtNodeIterator*>(from._handle); 
  return true; 
}

inline bool CPAtNodeIterator_to_KLAtNodeIterator(const AtNodeIterator* const& from, Fabric::EDK::KL::AtNodeIterator & to) {
  to._handle = const_cast<AtNodeIterator*>(from); 
  return true; 
}

#include "AtNodeEntryIterator.h"
inline bool KLAtNodeEntryIterator_to_CPAtNodeEntryIterator(const Fabric::EDK::KL::AtNodeEntryIterator & from, AtNodeEntryIterator* & to) {
  to = reinterpret_cast<AtNodeEntryIterator*>(from._handle); 
  return true; 
}

inline bool CPAtNodeEntryIterator_to_KLAtNodeEntryIterator(const AtNodeEntryIterator* const& from, Fabric::EDK::KL::AtNodeEntryIterator & to) {
  to._handle = const_cast<AtNodeEntryIterator*>(from); 
  return true; 
}

#include "AtAOVIterator.h"
inline bool KLAtAOVIterator_to_CPAtAOVIterator(const Fabric::EDK::KL::AtAOVIterator & from, AtAOVIterator* & to) {
  to = reinterpret_cast<AtAOVIterator*>(from._handle); 
  return true; 
}

inline bool CPAtAOVIterator_to_KLAtAOVIterator(const AtAOVIterator* const& from, Fabric::EDK::KL::AtAOVIterator & to) {
  to._handle = const_cast<AtAOVIterator*>(from); 
  return true; 
}

#include "AtParamEntry.h"
inline bool KLAtParamEntry_to_CPAtParamEntry(const Fabric::EDK::KL::AtParamEntry & from, AtParamEntry* & to) {
  to = reinterpret_cast<AtParamEntry*>(from._handle); 
  return true; 
}

inline bool CPAtParamEntry_to_KLAtParamEntry(const AtParamEntry* const& from, Fabric::EDK::KL::AtParamEntry & to) {
  to._handle = const_cast<AtParamEntry*>(from); 
  return true; 
}

#include "AtUserParamEntry.h"
inline bool KLAtUserParamEntry_to_CPAtUserParamEntry(const Fabric::EDK::KL::AtUserParamEntry & from, AtUserParamEntry* & to) {
  to = reinterpret_cast<AtUserParamEntry*>(from._handle); 
  return true; 
}

inline bool CPAtUserParamEntry_to_KLAtUserParamEntry(const AtUserParamEntry* const& from, Fabric::EDK::KL::AtUserParamEntry & to) {
  to._handle = const_cast<AtUserParamEntry*>(from); 
  return true; 
}

#include "AtMetaDataStore.h"
inline bool KLAtMetaDataStore_to_CPAtMetaDataStore(const Fabric::EDK::KL::AtMetaDataStore & from, AtMetaDataStore* & to) {
  to = reinterpret_cast<AtMetaDataStore*>(from._handle); 
  return true; 
}

inline bool CPAtMetaDataStore_to_KLAtMetaDataStore(const AtMetaDataStore* const& from, Fabric::EDK::KL::AtMetaDataStore & to) {
  to._handle = const_cast<AtMetaDataStore*>(from); 
  return true; 
}

