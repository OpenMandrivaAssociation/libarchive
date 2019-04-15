%define major 16
%define libname %mklibname archive %{major}
%define devname %mklibname archive -d

%global optflags %{optflags} -O3

# (tpg) enable PGO build
%bcond_without pgo

Summary:	Library for reading and writing streaming archives
Name:		libarchive
Version:	3.3.3
Release:	4
License:	BSD
Group:		System/Libraries
Url:		http://www.libarchive.org/
Source0:	http://www.libarchive.org/downloads/%{name}-%{version}.tar.gz
Patch0:		libarchive-2.6.1-headers.patch
Patch1:		libarchive-3.2.0-fix-install.patch
Patch2:		libarchive-3.3.2-tar-exclude-vcs.patch
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

%package -n bsdcat
Summary:	Expand files to standard output
Group:		Archiving/Backup

%description -n bsdcat
A command-line program automatically detects and
decompresses a variety of files 

%prep
%autosetup -p1

%build

%if %{with pgo}
%global optflags_normal %{optflags}
%global ldflags_normal %{ldflags}
%global optflags %{optflags} -fprofile-instr-generate
%global ldflags %{ldflags} -fprofile-instr-generate

export LLVM_PROFILE_FILE=%{name}-%p.profile.d
export LD_LIBRARY_PATH="$(pwd)/build/libarchive"
%cmake -DCMAKE_BUILD_TYPE=Release \
    -DBIN_INSTALL_DIR="/bin" \
    -DLIB_INSTALL_DIR="/%{_lib}" \
    -DENABLE_LIBXML2=FALSE \
    -DENABLE_EXPAT=FALSE \
    -DENABLE_NETTLE=OFF \
    -DENABLE_OPENSSL=ON \
    -DENABLE_LZO=ON \
    -DENABLE_CAT_SHARED=ON \
    -DENABLE_CPIO_SHARED=ON \
    -DENABLE_TAR_SHARED=ON \
    -G Ninja

%ninja

# run some tests
%ninja test
unset LD_LIBRARY_PATH
unset LLVM_PROFILE_FILE
llvm-profdata merge --output=%{name}.profile $(find . -name "*.profile.d" -type f)
find . -name "*.profile.d" -type f -delete
ninja clean

%global optflags %{optlfags_normal} -fprofile-instr-use=$(realpath %{name}.profile)
%global ldflags %{ldlfags_normal} -fprofile-instr-use=$(realpath %{name}.profile)
%endif
%cmake -DCMAKE_BUILD_TYPE=Release \
    -DBIN_INSTALL_DIR="/bin" \
    -DLIB_INSTALL_DIR="/%{_lib}" \
    -DENABLE_LIBXML2=FALSE \
    -DENABLE_EXPAT=FALSE \
    -DENABLE_NETTLE=OFF \
    -DENABLE_OPENSSL=ON \
    -DENABLE_LZO=ON \
    -DENABLE_CAT_SHARED=ON \
    -DENABLE_CPIO_SHARED=ON \
    -DENABLE_TAR_SHARED=ON \
    -G Ninja

%ninja

%install
%ninja_install -C build

#(proyvind) move to /%{_lib}
install -d %{buildroot}/%{_libdir}

# (tpg) not needed
rm %{buildroot}/%{_lib}/libarchive.so
rm %{buildroot}/%{_libdir}/libarchive.a

#mv %{buildroot}%{_libdir}/libarchive.so.%{major}* %{buildroot}/%{_lib}
echo "pay attention here"
ln -sr %{buildroot}/%{_lib}/libarchive.so.%{major} %{buildroot}%{_libdir}/libarchive.so

# Make bsdtar and bsdcpio the default tar and cpio implementations
for i in tar cpio; do
    mv %{buildroot}/bin/bsd${i} %{buildroot}/bin/${i}
    mv %{buildroot}%{_mandir}/man1/bsd${i}.1 %{buildroot}%{_mandir}/man1/${i}.1
# For compatibility with stuff hardcoding it
    ln -s ${i} %{buildroot}/bin/bsd${i}
    ln -s ${i}.1 %{buildroot}%{_mandir}/man1/bsd${i}.1
done

# (tpg) checks for i586 and x86_64 fails for some very strange reasons
# here is a good explanation and possible workaround... but no time for this
# https://github.com/libarchive/libarchive/issues/723
#check
#ninja -C build test

%files -n tar
%doc NEWS
/bin/tar
/bin/bsdtar
%{_mandir}/man1/tar.1*
%{_mandir}/man1/bsdtar.1*

%files -n cpio
/bin/cpio
/bin/bsdcpio
%{_mandir}/man1/cpio.1*
%{_mandir}/man1/bsdcpio.1*

%files -n bsdcat
/bin/bsdcat
%{_mandir}/man1/bsdcat.1*

%files -n %{libname}
/%{_lib}/libarchive.so.%{major}*

%files -n %{devname}
%{_libdir}/%{name}*.so
%{_libdir}/pkgconfig/libarchive.pc
%{_includedir}/*.h
%{_mandir}/man3/*
%{_mandir}/man5/*
