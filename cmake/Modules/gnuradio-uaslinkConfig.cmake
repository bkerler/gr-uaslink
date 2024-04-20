find_package(PkgConfig)

PKG_CHECK_MODULES(PC_GR_UASLINK gnuradio-uaslink)

FIND_PATH(
    GR_UASLINK_INCLUDE_DIRS
    NAMES gnuradio/uaslink/api.h
    HINTS $ENV{UASLINK_DIR}/include
        ${PC_UASLINK_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    GR_UASLINK_LIBRARIES
    NAMES gnuradio-uaslink
    HINTS $ENV{UASLINK_DIR}/lib
        ${PC_UASLINK_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/gnuradio-uaslinkTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(GR_UASLINK DEFAULT_MSG GR_UASLINK_LIBRARIES GR_UASLINK_INCLUDE_DIRS)
MARK_AS_ADVANCED(GR_UASLINK_LIBRARIES GR_UASLINK_INCLUDE_DIRS)
