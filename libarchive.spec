%define major 20
%define oldlibname %mklibname archive 19
%define libname %mklibname archive
%define devname %mklibname archive -d

%global optflags %{optflags} -O3

# (tpg) enable PGO build
%if %{cross_compiling}
%bcond_with pgo
%else
%bcond_without pgo
%endif

Summary:	Library for reading and writing streaming archives
Name:		libarchive
Version:	3.7.4
Release:	1
License:	BSD
Group:		System/Libraries
Url:		https://www.libarchive.org/
Source0:	https://www.libarchive.org/downloads/%{name}-%{version}.tar.xz
Patch0:		libarchive.pc-no-Lusrlib.patch
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	bison
BuildRequires:	findutils
BuildRequires:	libtool
BuildRequires:	sharutils
BuildRequires:	pkgconfig(libacl)
BuildRequires:	pkgconfig(libattr)
BuildRequires:	pkgconfig(bzip2)
BuildRequires:	pkgconfig(lzo2)
BuildRequires:	pkgconfig(libzstd)
BuildRequires:	pkgconfig(libssl)
BuildRequires:	pkgconfig(ext2fs)
BuildRequires:	pkgconfig(liblzma)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(liblz4)
BuildRequires:	pkgconfig(libb2)

%description
Libarchive is a programming library that can create and read several
different streaming archive formats, including most popular tar
variants and several cpio formats.

It can also write shar archives and read ISO9660 CDROM images and ZIP
archives. The bsdtar program is an implementation of tar(1) that is
built on top of libarchive.

It started as a test harness, but has grown and is now the
standard system tar for OpenMandriva Lx and FreeBSD.

%package -n %{libname}
Summary:	Library for reading and writing streaming archives
Group:		System/Libraries
%rename		%{_lib}archive1

%description -n %{libname}
Libarchive is a programming library that can create and read several
different streaming archive formats, including most popular tar
variants and several cpio formats. It can also write shar archives and
read ISO9660 CDROM images and ZIP archives.

The bsdtar program is an implementation of tar(1) that is built on
top of libarchive. It started as a test harness, but has grown and is
now the standard system tar for OpenMandriva Lx and FreeBSD.

%package -n %{devname}
Summary:	Development library and header files for the libarchive library
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
This package contains header files for the libarchive library.

%package -n tar
Summary:	Full-featured tar replacement built on libarchive
Group:		Archiving/Backup
Suggests:	/usr/bin/rsh
%rename		bsdtar

%description -n tar
The bsdtar program is a full-featured tar replacement built on
libarchive.

%package -n cpio
Summary:	Copy files to and from archives
Group:		Archiving/Backup
Suggests:	rmt
%rename		bsdcpio

%description -n cpio
bsdcpio copies files between archives and directories. This
implementation can extract from tar, pax, cpio, zip, jar, ar, and
ISO 9660 cdrom images and can create tar, pax, cpio, ar, and shar
archives.

%package -n libarchive-unzip
Summary:	Extract files from zip archives
Group:		Archiving/Backup

%description -n libarchive-unzip
Tool to extract files from zip archives

%package -n bsdcat
Summary:	Expand files to standard output
Group:		Archiving/Backup

%description -n bsdcat
A command-line program automatically detects and
decompresses a variety of files 

%prep
%autosetup -p1

%if "%{_lib}" != "lib"
find . -name CMakeLists.txt |xargs sed -i -e 's,DESTINATION lib,DESTINATION %{_lib},g'
sed -i -e 's,DESTINATION "lib,DESTINATION "%{_lib},g' build/cmake/CreatePkgConfigFile.cmake
%endif

%build
%if %{with pgo}
export LD_LIBRARY_PATH="$(pwd)/build/libarchive"
%cmake -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_C_FLAGS="%{optflags} -fprofile-generate" \
    -DCMAKE_C_FLAGS_RELEASE="%{optflags} -fprofile-generate" \
    -DCMAKE_C_FLAGS_RELWITHDEBINFO="%{optflags} -fprofile-generate" \
    -DCMAKE_CXX_FLAGS="%{optflags} -fprofile-generate" \
    -DCMAKE_CXX_FLAGS_RELEASE="%{optflags} -fprofile-generate" \
    -DCMAKE_CXX_FLAGS_RELWITHDEBINFO="%{optflags} -fprofile-generate" \
    -DCMAKE_EXE_LINKER_FLAGS="%{build_ldflags} -fprofile-generate" \
    -DCMAKE_SHARED_LINKER_FLAGS="%{build_ldflags} -fprofile-generate" \
    -DCMAKE_MODULE_LINKER_FLAGS="%(echo %{build_ldflags} -fprofile-generate|sed -e 's#-Wl,--no-undefined##')" \
    -DENABLE_LIBXML2=OFF \
    -DENABLE_EXPAT=OFF \
    -DENABLE_NETTLE=OFF \
    -DENABLE_OPENSSL=ON \
    -DENABLE_LZO=ON \
    -DENABLE_CAT_SHARED=ON \
    -DENABLE_CPIO_SHARED=ON \
    -DENABLE_TAR_SHARED=ON \
    -DENABLE_UNZIP_SHARED=ON \
    -G Ninja

%ninja

# run some tests, it may fail but still use data which we got
%ninja test ||:

unset LD_LIBRARY_PATH
llvm-profdata merge --output=%{name}-llvm.profdata $(find . -name "*.profraw" -type f)
PROFDATA="$(realpath %{name}-llvm.profdata)"
find . -name "*.profraw" -type f -delete
ninja -t clean
cd ..
%endif

%cmake -DCMAKE_BUILD_TYPE=Release \
%if %{with pgo}
    -DCMAKE_C_FLAGS="%{optflags} -fprofile-use=$PROFDATA" \
    -DCMAKE_C_FLAGS_RELEASE="%{optflags} -fprofile-use=$PROFDATA" \
    -DCMAKE_C_FLAGS_RELWITHDEBINFO="%{optflags} -fprofile-use=$PROFDATA" \
    -DCMAKE_CXX_FLAGS="%{optflags} -fprofile-use=$PROFDATA" \
    -DCMAKE_CXX_FLAGS_RELEASE="%{optflags} -fprofile-use=$PROFDATA" \
    -DCMAKE_CXX_FLAGS_RELWITHDEBINFO="%{optflags} -fprofile-use=$PROFDATA" \
    -DCMAKE_EXE_LINKER_FLAGS="%{build_ldflags} -fprofile-use=$PROFDATA" \
    -DCMAKE_SHARED_LINKER_FLAGS="%{build_ldflags} -fprofile-use=$PROFDATA" \
    -DCMAKE_MODULE_LINKER_FLAGS="%(echo %{build_ldflags} -fprofile-use=$PROFDATA" \|sed -e 's#-Wl,--no-undefined##')" \
%endif
    -DENABLE_LIBXML2=FALSE \
    -DENABLE_EXPAT=FALSE \
    -DENABLE_NETTLE=OFF \
    -DENABLE_OPENSSL=ON \
    -DENABLE_LZO=ON \
    -DENABLE_CAT_SHARED=ON \
    -DENABLE_CPIO_SHARED=ON \
    -DENABLE_TAR_SHARED=ON \
    -DENABLE_UNZIP=ON \
    -G Ninja

%ninja

%install
%ninja_install -C build

# (tpg) not needed
rm %{buildroot}/%{_libdir}/libarchive.a

# Make bsdtar and bsdcpio the default tar and cpio implementations
for i in tar cpio; do
    ln -sf %{_bindir}/bsd${i} %{buildroot}%{_bindir}/${i}
    ln -sf %{_mandir}/man1/bsd${i}.1 %{buildroot}%{_mandir}/man1/${i}.1
done

%if ! %{cross_compiling}
# (tpg) checks for i586 and x86_64 fails for some very strange reasons
# here is a good explanation and possible workaround... but no time for this
# https://github.com/libarchive/libarchive/issues/723
#check
#ninja -C build test
%endif

%files -n tar
%doc NEWS
%{_bindir}/tar
%{_bindir}/bsdtar
%doc %{_mandir}/man1/tar.1*
%doc %{_mandir}/man1/bsdtar.1*

%files -n cpio
%{_bindir}/cpio
%{_bindir}/bsdcpio
%doc %{_mandir}/man1/cpio.1*
%doc %{_mandir}/man1/bsdcpio.1*

%files -n libarchive-unzip
%{_bindir}/bsdunzip
%doc %{_mandir}/man1/bsdunzip.1*

%files -n bsdcat
%{_bindir}/bsdcat
%doc %{_mandir}/man1/bsdcat.1*

%files -n %{libname}
%{_libdir}/libarchive.so.%{major}*

%files -n %{devname}
%{_libdir}/%{name}*.so
%{_libdir}/pkgconfig/libarchive.pc
%{_includedir}/*.h
%doc %{_mandir}/man3/*
%doc %{_mandir}/man5/*
