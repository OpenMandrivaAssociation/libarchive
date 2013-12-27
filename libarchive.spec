%define	major	13
%define	libname	%mklibname archive %{major}
%define	devname	%mklibname archive -d

Summary:	Library for reading and writing streaming archives
Name:		libarchive
Version:	3.1.2
Release:	1
License:	BSD
Group:		System/Libraries
Url:		http://code.google.com/p/libarchive/
Source0:	http://www.libarchive.org/downloads/%{name}-%{version}.tar.gz
Patch0:		libarchive-2.6.1-headers.patch

BuildRequires:	bison
BuildRequires:	libtool
BuildRequires:	sharutils
BuildRequires:	acl-devel
BuildRequires:	attr-devel
BuildRequires:	bzip2-devel
BuildRequires:	pkgconfig(ext2fs)
BuildRequires:	pkgconfig(liblzma)
BuildRequires:	pkgconfig(zlib)

%description
Libarchive is a programming library that can create and read several different
streaming archive formats, including most popular tar variants and several cpio
formats. It can also write shar archives and read ISO9660 CDROM images and ZIP
archives. The bsdtar program is an implementation of tar(1) that is built on
top of libarchive. It started as a test harness, but has grown and is now the
standard system tar for FreeBSD 5 and 6.

%package -n	%{libname}
Summary:	Library for reading and writing streaming archives
Group:		System/Libraries
%rename		%{_lib}archive1

%description -n	%{libname}
Libarchive is a programming library that can create and read several different
streaming archive formats, including most popular tar variants and several cpio
formats. It can also write shar archives and read ISO9660 CDROM images and ZIP
archives. The bsdtar program is an implementation of tar(1) that is built on
top of libarchive. It started as a test harness, but has grown and is now the
standard system tar for FreeBSD 5 and 6.

%package -n	%{devname}
Summary:	Development library and header files for the libarchive library
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{devname}
This package contains header files for the libarchive library.

%package -n	bsdtar
Summary:	Full-featured tar replacement built on libarchive
Group:		Archiving/Backup

%description -n	bsdtar
The bsdtar program is a full-featured tar replacement built on libarchive.

%package -n	bsdcpio
Summary:	Copy files to and from archives
Group:		Archiving/Backup

%description -n	bsdcpio
bsdcpio copies files between archives and directories. This implementation can
extract from tar, pax, cpio, zip, jar, ar, and ISO 9660 cdrom images and can
create tar, pax, cpio, ar, and shar archives.

%prep
%setup -q
%apply_patches
autoreconf -fis

%build
%configure2_5x \
	--disable-static \
	--enable-bsdtar=shared \
	--enable-bsdcpio=shared
%make

%install
%makeinstall_std

%files -n bsdtar
%doc NEWS README
%{_bindir}/bsdtar
%{_mandir}/man1/bsdtar.1*

%files -n bsdcpio
%{_bindir}/bsdcpio
%{_mandir}/man1/bsdcpio.1*

%files -n %{libname}
%{_libdir}/libarchive.so.%{major}*

%files -n %{devname}
%{_libdir}/*so
%{_libdir}/pkgconfig/libarchive.pc
%{_includedir}/*.h
%{_mandir}/man3/*
%{_mandir}/man5/*

