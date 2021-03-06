cmake_minimum_required(VERSION 3.16)

project("app")

set(CMAKE_C_FLAGS_DEBUG "-g -rdynamic -funwind-tables")
set(CMAKE_C_FLAGS "-Wall -Wextra -Werror=return-type")
set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_C_FLAGS_DEBUG}")
set(CMAKE_CXX_FLAGS "${CMAKE_C_FLAGS} -std=c++17 -fno-exceptions -pedantic")
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

include_directories(
    "src"
    "${EPICS_BASE}/include"
    "${EPICS_BASE}/include/os/Linux"
    "${EPICS_BASE}/include/compiler/gcc"
)

set(BASE_SRC
    "src/core/panic.cpp"
    "src/channel/base.cpp"
)
set(EPICS_SRC
    "src/record/base.cpp"
    "src/record/waveform.cpp"
)
set(MAIN_SRC
    ${BASE_SRC}
    ${EPICS_SRC}
    "src/channel/rpmsg.cpp"
    "src/framework.cpp"
)
set(FAKEDEV_SRC
    ${BASE_SRC}
    ${EPICS_SRC}
    "src/channel/zmq.cpp"
    "src/framework.cpp"
)
set(UNITTEST_SRC
    ${BASE_SRC}
    "src/core/io_test.cpp"
    "src/channel/zmq.cpp"
    "src/channel/zmq_test.cpp"
    "src/unittest.cpp"
)

set(COMMON_DEFS)
set(MAIN_DEFS
    ${COMMON_DEFS}
)
set(FAKEDEV_DEFS
    ${COMMON_DEFS}
    "FAKEDEV"
)
set(UNITTEST_DEFS
    ${FAKEDEV_DEFS}
    "UNITTEST"
)

set(COMMON_LIBS)
set(MAIN_LIBS
    ${COMMON_LIBS}
)
set(FAKEDEV_LIBS
    ${COMMON_LIBS}
    "pthread"
    "zmq"
)
set(UNITTEST_LIBS
    "gtest"
    ${FAKEDEV_LIBS}
)

set(MAIN ${PROJECT_NAME})
add_library(${MAIN} SHARED ${MAIN_SRC})
target_compile_definitions(${MAIN} PRIVATE ${MAIN_DEFS})
target_link_libraries(${MAIN} PRIVATE ${MAIN_LIBS})

set(FAKEDEV "${PROJECT_NAME}_fakedev")
add_library(${FAKEDEV} SHARED ${FAKEDEV_SRC})
target_compile_definitions(${FAKEDEV} PRIVATE ${FAKEDEV_DEFS})
target_link_libraries(${FAKEDEV} PRIVATE ${FAKEDEV_LIBS})

enable_testing()
set(UNITTEST "${PROJECT_NAME}_unittest")
add_executable(${UNITTEST} ${UNITTEST_SRC})
target_compile_definitions(${UNITTEST} PRIVATE ${UNITTEST_DEFS})
target_link_libraries(${UNITTEST} PRIVATE ${UNITTEST_LIBS})
add_test(${UNITTEST} ${UNITTEST})
