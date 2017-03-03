//! \file
/*
**  Copyright (C) - Triton
**
**  This program is under the terms of the BSD License.
*/

#if defined(__unix__) || defined(__APPLE__)

#include <triton/syscalls.hpp>
#include <triton/tritonTypes.hpp>
#include <triton/unix.hpp>



namespace triton {
  namespace os {
    namespace posix {

      #if defined(__unix__)
      const char* syscall32NumberToString(triton::uint32 syscallNumber) {
        if (syscallNumber < static_cast<triton::uint32>(triton::os::posix::NB_SYSCALL32))
          return triton::os::posix::syscallmap32[syscallNumber];
        else
          return nullptr;
      }
      #endif

      const char* syscall64NumberToString(triton::uint32 syscallNumber) {
        if (syscallNumber < static_cast<triton::uint32>(triton::os::posix::NB_SYSCALL64))
          return triton::os::posix::syscallmap64[syscallNumber];
        else
          return nullptr;
      }

    }; /* posix namespace */
  }; /* os namespace */
}; /* triton namespace */

#endif /* __unix__ || __APPLE__ */
