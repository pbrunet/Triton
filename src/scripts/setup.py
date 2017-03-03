#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# Copyright (C) - Triton
# This program is under the terms of the BSD License.
#

from   setuptools import setup, Extension
import sys
import shutil
import os
import platform

package_name        = 'triton'
version             = '0.4'
package_description = '''
Triton is a dynamic binary analysis (DBA) framework. It provides internal components like a
Dynamic Symbolic Exuction (DSE) engine, a Taint Engine, AST Semantics representations of the x86 and
the x86-64 instruction set, SMT simplification passes, a Z3 interface to solve constraints and,
the last but not least, Python bindings. Based on these components, you are able to build
program analysis tools, automate reverse engineering and perform software verification.
'''.strip()

BINDING_FILES = [
    "init.cpp",
    "modules/astCallbacks.cpp",
    "modules/tritonCallbacks.cpp",
    "namespaces/initArchNamespace.cpp",
    "namespaces/initAstNodeNamespace.cpp",
    "namespaces/initAstRepresentationNamespace.cpp",
    "namespaces/initCallbackNamespace.cpp",
    "namespaces/initCpuSizeNamespace.cpp",
    "namespaces/initElfNamespace.cpp",
    "namespaces/initModeNamespace.cpp",
    "namespaces/initOperandNamespace.cpp",
    "namespaces/initPeNamespace.cpp",
    "namespaces/initRegNamespace.cpp",
    "namespaces/initSymExprNamespace.cpp",
    "namespaces/initSyscallNamespace.cpp",
    "namespaces/initVersionNamespace.cpp",
    "namespaces/initX86OpcodesNamespace.cpp",
    "namespaces/initX86PrefixesNamespace.cpp",
    "objects/pyAstNode.cpp",
    "objects/pyBitvector.cpp",
    "objects/pyElf.cpp",
    "objects/pyElfDynamicTable.cpp",
    "objects/pyElfHeader.cpp",
    "objects/pyElfProgramHeader.cpp",
    "objects/pyElfRelocationTable.cpp",
    "objects/pyElfSectionHeader.cpp",
    "objects/pyElfSymbolTable.cpp",
    "objects/pyImmediate.cpp",
    "objects/pyInstruction.cpp",
    "objects/pyMemoryAccess.cpp",
    "objects/pyPathConstraint.cpp",
    "objects/pyPe.cpp",
    "objects/pyPeExportEntry.cpp",
    "objects/pyPeExportTable.cpp",
    "objects/pyPeHeader.cpp",
    "objects/pyPeImportLookup.cpp",
    "objects/pyPeImportTable.cpp",
    "objects/pyPeSectionHeader.cpp",
    "objects/pyRegister.cpp",
    "objects/pySolverModel.cpp",
    "objects/pySymbolicExpression.cpp",
    "objects/pySymbolicVariable.cpp",
    "pyXFunctions.cpp",
    "utils.cpp",
]

if platform.system() == 'Linux':
    TRITON_LIBRARY = '@CMAKE_BINARY_DIR@/src/libtriton/libtriton.so'
    TRITON_MODULE  = '@CMAKE_BINARY_DIR@/src/libtriton/triton.so'
    TRITON_MODULES = [TRITON_MODULE]

elif platform.system() == 'Darwin':
    TRITON_LIBRARY = '@CMAKE_BINARY_DIR@/src/libtriton/libtriton.dylib'
    TRITON_MODULE  = '@CMAKE_BINARY_DIR@/src/libtriton/triton.so'
    TRITON_MODULES = [TRITON_MODULE]

elif platform.system() == 'Windows':
    Z3_LIB_PATH    = r'@Z3_LIBRARIES@'.replace('.lib', '.dll')
    TRITON_LIBRARY = '@CMAKE_BINARY_DIR@/src/libtriton/Release/triton.dll'.replace('/', '\\')
    TRITON_MODULE  = '@CMAKE_BINARY_DIR@/src/libtriton/Release/triton.pyd'.replace('/', '\\')
    TRITON_MODULES = [TRITON_MODULE, Z3_LIB_PATH]

else:
    print '[+] Invalid platform - Send us a pull request :)'
    sys.exit(1)

#shutil.copyfile(TRITON_LIBRARY, TRITON_MODULE)
module = Extension("triton",
                   language="c++",
                   define_macros=[("_GLIBCXX_USE_CXX11_ABI", "0")],
                   include_dirs=[os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "libtriton", "includes")),
                                 "/home/pbrunet/dev/Triton/build/src/libtriton/"],
                   sources=[os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "libtriton", "bindings", "python", f)) for f in BINDING_FILES],
                   libraries=["triton"],
                   library_dirs=["/home/pbrunet/dev/Triton/build/src/libtriton/"]
                   )

setup(
    name                 = package_name,
    version              = version,
    description          = package_description,
    license              = 'BSD',
    author               = 'Jonathan Salwan',
    author_email         = 'jsalwan@quarkslab.com',
    url                  = 'http://triton.quarkslab.com',
    zip_safe             = False,
    include_package_data = True,
    data_files           = [("", TRITON_MODULES)],
    classifiers          = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: C++',
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering',
        'Topic :: Security',
    ],
    ext_modules=[module]
)

