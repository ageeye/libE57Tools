# 

cmake_minimum_required( VERSION 3.10.0 )
project(libE57Tools VERSION 0.1.0 DESCRIPTION "libe57Tools")

#

find_package( XercesC REQUIRED )

# 
add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/libE57Format/)

add_library(libE57Tools SHARED src/libE57Tools.cpp)
set_target_properties(libE57Tools PROPERTIES
    CXX_STANDARD 14
	CXX_STANDARD_REQUIRED YES
	CXX_EXTENSIONS NO
	DEBUG_POSTFIX "-d"
	POSITION_INDEPENDENT_CODE ON
    VERSION ${PROJECT_VERSION}
    SOVERSION 0
    PUBLIC_HEADER include/libE57Tools.h
	POSITION_INDEPENDENT_CODE ON
)

target_include_directories(libE57Tools PRIVATE 
	./include
	./libE57Format/include
	${CMAKE_BINARY_DIR}/libE57Format
)

target_link_libraries(libE57Tools ${CMAKE_BINARY_DIR}/libE57Format/libE57Format.a XercesC::XercesC)
