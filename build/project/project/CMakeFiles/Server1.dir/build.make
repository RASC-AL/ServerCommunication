# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 2.8

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list

# Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/sbrover/Rover2015/src

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/sbrover/Rover2015/build

# Include any dependencies generated for this target.
include project/project/CMakeFiles/Server1.dir/depend.make

# Include the progress variables for this target.
include project/project/CMakeFiles/Server1.dir/progress.make

# Include the compile flags for this target's objects.
include project/project/CMakeFiles/Server1.dir/flags.make

project/project/CMakeFiles/Server1.dir/src/tcpServer.cpp.o: project/project/CMakeFiles/Server1.dir/flags.make
project/project/CMakeFiles/Server1.dir/src/tcpServer.cpp.o: /home/sbrover/Rover2015/src/project/project/src/tcpServer.cpp
	$(CMAKE_COMMAND) -E cmake_progress_report /home/sbrover/Rover2015/build/CMakeFiles $(CMAKE_PROGRESS_1)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Building CXX object project/project/CMakeFiles/Server1.dir/src/tcpServer.cpp.o"
	cd /home/sbrover/Rover2015/build/project/project && /usr/bin/c++   $(CXX_DEFINES) $(CXX_FLAGS) -o CMakeFiles/Server1.dir/src/tcpServer.cpp.o -c /home/sbrover/Rover2015/src/project/project/src/tcpServer.cpp

project/project/CMakeFiles/Server1.dir/src/tcpServer.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/Server1.dir/src/tcpServer.cpp.i"
	cd /home/sbrover/Rover2015/build/project/project && /usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS) -E /home/sbrover/Rover2015/src/project/project/src/tcpServer.cpp > CMakeFiles/Server1.dir/src/tcpServer.cpp.i

project/project/CMakeFiles/Server1.dir/src/tcpServer.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/Server1.dir/src/tcpServer.cpp.s"
	cd /home/sbrover/Rover2015/build/project/project && /usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS) -S /home/sbrover/Rover2015/src/project/project/src/tcpServer.cpp -o CMakeFiles/Server1.dir/src/tcpServer.cpp.s

project/project/CMakeFiles/Server1.dir/src/tcpServer.cpp.o.requires:
.PHONY : project/project/CMakeFiles/Server1.dir/src/tcpServer.cpp.o.requires

project/project/CMakeFiles/Server1.dir/src/tcpServer.cpp.o.provides: project/project/CMakeFiles/Server1.dir/src/tcpServer.cpp.o.requires
	$(MAKE) -f project/project/CMakeFiles/Server1.dir/build.make project/project/CMakeFiles/Server1.dir/src/tcpServer.cpp.o.provides.build
.PHONY : project/project/CMakeFiles/Server1.dir/src/tcpServer.cpp.o.provides

project/project/CMakeFiles/Server1.dir/src/tcpServer.cpp.o.provides.build: project/project/CMakeFiles/Server1.dir/src/tcpServer.cpp.o

# Object files for target Server1
Server1_OBJECTS = \
"CMakeFiles/Server1.dir/src/tcpServer.cpp.o"

# External object files for target Server1
Server1_EXTERNAL_OBJECTS =

/home/sbrover/Rover2015/devel/lib/project/Server1: project/project/CMakeFiles/Server1.dir/src/tcpServer.cpp.o
/home/sbrover/Rover2015/devel/lib/project/Server1: /opt/ros/hydro/lib/libroscpp.so
/home/sbrover/Rover2015/devel/lib/project/Server1: /usr/lib/libboost_signals-mt.so
/home/sbrover/Rover2015/devel/lib/project/Server1: /usr/lib/libboost_filesystem-mt.so
/home/sbrover/Rover2015/devel/lib/project/Server1: /opt/ros/hydro/lib/librosconsole.so
/home/sbrover/Rover2015/devel/lib/project/Server1: /opt/ros/hydro/lib/librosconsole_log4cxx.so
/home/sbrover/Rover2015/devel/lib/project/Server1: /opt/ros/hydro/lib/librosconsole_backend_interface.so
/home/sbrover/Rover2015/devel/lib/project/Server1: /usr/lib/liblog4cxx.so
/home/sbrover/Rover2015/devel/lib/project/Server1: /usr/lib/libboost_regex-mt.so
/home/sbrover/Rover2015/devel/lib/project/Server1: /opt/ros/hydro/lib/libxmlrpcpp.so
/home/sbrover/Rover2015/devel/lib/project/Server1: /opt/ros/hydro/lib/libroscpp_serialization.so
/home/sbrover/Rover2015/devel/lib/project/Server1: /opt/ros/hydro/lib/librostime.so
/home/sbrover/Rover2015/devel/lib/project/Server1: /usr/lib/libboost_date_time-mt.so
/home/sbrover/Rover2015/devel/lib/project/Server1: /usr/lib/libboost_system-mt.so
/home/sbrover/Rover2015/devel/lib/project/Server1: /usr/lib/libboost_thread-mt.so
/home/sbrover/Rover2015/devel/lib/project/Server1: /usr/lib/x86_64-linux-gnu/libpthread.so
/home/sbrover/Rover2015/devel/lib/project/Server1: /opt/ros/hydro/lib/libcpp_common.so
/home/sbrover/Rover2015/devel/lib/project/Server1: /opt/ros/hydro/lib/libconsole_bridge.so
/home/sbrover/Rover2015/devel/lib/project/Server1: project/project/CMakeFiles/Server1.dir/build.make
/home/sbrover/Rover2015/devel/lib/project/Server1: project/project/CMakeFiles/Server1.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --red --bold "Linking CXX executable /home/sbrover/Rover2015/devel/lib/project/Server1"
	cd /home/sbrover/Rover2015/build/project/project && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/Server1.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
project/project/CMakeFiles/Server1.dir/build: /home/sbrover/Rover2015/devel/lib/project/Server1
.PHONY : project/project/CMakeFiles/Server1.dir/build

project/project/CMakeFiles/Server1.dir/requires: project/project/CMakeFiles/Server1.dir/src/tcpServer.cpp.o.requires
.PHONY : project/project/CMakeFiles/Server1.dir/requires

project/project/CMakeFiles/Server1.dir/clean:
	cd /home/sbrover/Rover2015/build/project/project && $(CMAKE_COMMAND) -P CMakeFiles/Server1.dir/cmake_clean.cmake
.PHONY : project/project/CMakeFiles/Server1.dir/clean

project/project/CMakeFiles/Server1.dir/depend:
	cd /home/sbrover/Rover2015/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/sbrover/Rover2015/src /home/sbrover/Rover2015/src/project/project /home/sbrover/Rover2015/build /home/sbrover/Rover2015/build/project/project /home/sbrover/Rover2015/build/project/project/CMakeFiles/Server1.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : project/project/CMakeFiles/Server1.dir/depend
