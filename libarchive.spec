%define	major 2
%define libname %mklibname archive %{major}
%define develname %mklibname archive -d

Summary:	Library for reading and writing streaming archives
Name:		libarchive
Version:	2.6.2
Release:	%mkrel 1
License:	BSD
Group:		System/Libraries
URL:		http://code.google.com/p/libarchive/
Source0:	http://libarchive.googlecode.com/files/%{name}-%{version}.tar.gz
Patch0:		libarchive-2.6.0-xz-support.patch
Patch1:		libarchive-2.6.1-headers.patch
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	bzip2-devel
BuildRequires:	libacl-devel
BuildRequires:	libattr-devel
BuildRequires:	e2fsprogs-devel
BuildRequires:	libtool
BuildRequires:	zlib-devel
BuildRequires:	lzma-devel
BuildRequires:	sharutils
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Libarchive is a programming library that can create and read several different
streaming archive formats, including most popular tar variants and several cpio
formats. It can also write shar archives and read ISO9660 CDROM images and ZIP
archives. The bsdtar program is an implementation of tar(1) that is built on
top of libarchive. It started as a test harness, but has grown and is now the
standard system tar for FreeBSD 5 and 6.

%package -n	%{libname}
Summary:	Library for reading and writing streaming archives
Group:          System/Libraries

%description -n	%{libname}
Libarchive is a programming library that can create and read several different
streaming archive formats, including most popular tar variants and several cpio
formats. It can also write shar archives and read ISO9660 CDROM images and ZIP
archives. The bsdtar program is an implementation of tar(1) that is built on
top of libarchive. It started as a test harness, but has grown and is now the
standard system tar for FreeBSD 5 and 6.

%package -n	%{develname}
Summary:	Static library and header files for the libarchive library
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{libname}-devel = %{version}
Obsoletes:	%{libname}-devel
Obsoletes:	%{mklibname archive 1}-devel
Provides:	%{name}-devel = %{version}

%description -n	%{develname}
Libarchive is a programming library that can create and read several different
streaming archive formats, including most popular tar variants and several cpio
formats. It can also write shar archives and read ISO9660 CDROM images and ZIP
archives. The bsdtar program is an implementation of tar(1) that is built on
top of libarchive. It started as a test harness, but has grown and is now the
standard system tar for FreeBSD 5 and 6.

This package contains header files for the libarchive library.

%package -n	bsdtar
Summary:	Full-featured tar replacement built on libarchive
Group:		Archiving/Backup

%description -n	bsdtar
The bsdtar program is a full-featured tar replacement built on libarchive.

%prep
%setup -q
%patch0 -p1 -b .xz~
%patch1 -p1 -b .headers

%build
autoreconf -fi
%configure2_5x \
    --enable-bsdtar=shared
%make

%install
rm -rf %{buildroot}

%makeinstall_std

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files -n bsdtar
%defattr(-,root,root)
%attr(0755,root,root) %{_bindir}/bsdtar
%attr(0644,root,root) %{_mandir}/man1/*

%files -n %{libname}
%defattr(-,root,root)
%doc NEWS README
%attr(0755,root,root) %{_libdir}/lib*.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%attr(0755,root,root) %{_libdir}/*so
%attr(0644,root,root) %{_libdir}/*.a
%attr(0644,root,root) %{_libdir}/*.la
%attr(0644,root,root) %{_includedir}/*.h
%attr(0644,root,root) %{_mandir}/man3/*
%attr(0644,root,root) %{_mandir}/man5/*
