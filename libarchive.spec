%define major 13
%define libname %mklibname archive %{major}
%define develname %mklibname archive -d

Summary:	Library for reading and writing streaming archives
Name:		libarchive
Version:	3.1.2
Release:	14
License:	BSD
Group:		System/Libraries
Url:		http://code.google.com/p/libarchive/
Source0:	http://www.libarchive.org/downloads/%{name}-%{version}.tar.gz
Patch0:		libarchive-2.6.1-headers.patch
Patch1:		libarchive-3.1.2-CVE-2013-0211.patch
Patch2:		libarchive-3.1.2-cpio-add-dereference-long-alias-for-gnu-cpio-compatibility.patch
Patch3:		libarchive-3.1.2-when-adding-vv-be-verbose-like-gnutar.patch
Patch4:		libarchive-3.1.2-testsuite.patch
BuildRequires:	bison
BuildRequires:	libtool
BuildRequires:	sharutils
BuildRequires:	acl-devel
BuildRequires:	attr-devel
BuildRequires:	bzip2-devel
BuildRequires:	lzo-devel
# expat is lighter with less dependencies, so considering as this package is
# now a part of basesystem, we'll use expat rather than libxml2
BuildRequires:	pkgconfig(expat)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(ext2fs)
BuildRequires:	pkgconfig(liblzma)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(zlib)

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

%description -n	%{libname}
Libarchive is a programming library that can create and read several
different streaming archive formats, including most popular tar
variants and several cpio formats. It can also write shar archives and
read ISO9660 CDROM images and ZIP archives.

The bsdtar program is an implementation of tar(1) that is built on
top of libarchive. It started as a test harness, but has grown and is
now the standard system tar for OpenMandriva Lx and FreeBSD.

%package -n %{develname}
Summary:	Development library and header files for the libarchive library
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{develname}
This package contains header files for the libarchive library.

%package -n tar
Summary:	Full-featured tar replacement built on libarchive
Group:		Archiving/Backup
Suggests:	/usr/bin/rsh
Provides:	bsdtar = %{EVRD}
Obsoletes:	bsdtar < %{EVRD}

%description -n	tar
The bsdtar program is a full-featured tar replacement built on
libarchive.

%package -n cpio
Summary:	Copy files to and from archives
Group:		Archiving/Backup
Suggests:	rmt
Provides:	bsdcpio = %{EVRD}
Obsoletes:	bsdcpio < %{EVRD}

%description -n	cpio
bsdcpio copies files between archives and directories. This
implementation can extract from tar, pax, cpio, zip, jar, ar, and
ISO 9660 cdrom images and can create tar, pax, cpio, ar, and shar
archives.

%prep
%setup -q
%apply_patches

autoreconf -fis

%build
%configure \
	--bindir=/bin \
	--libdir=/%{_lib} \
	--enable-bsdtar=shared \
	--enable-bsdcpio=shared \
	--enable-lzo2 \
	--with-expat \
	--without-xml2 \
	--with-openssl

# remove rpaths
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make

%install
%makeinstall_std

#(tpg) move to _libdir
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_libdir}/pkgconfig
mv -f %{buildroot}/%{_lib}/pkgconfig/libarchive.pc %{buildroot}%{_libdir}/pkgconfig/libarchive.pc

# Make bsdtar and bsdcpio the default tar and cpio implementations
for i in tar cpio; do
	mv %{buildroot}/bin/bsd${i} %{buildroot}/bin/${i}
	mv %{buildroot}%{_mandir}/man1/bsd${i}.1 %{buildroot}%{_mandir}/man1/${i}.1
	# For compatibility with stuff hardcoding it
	ln -s ${i} %{buildroot}/bin/bsd${i}
	ln -s ${i}.1 %{buildroot}%{_mandir}/man1/bsd${i}.1
done

%files -n tar
%doc NEWS README
/bin/tar
/bin/bsdtar
%{_mandir}/man1/tar.1*
%{_mandir}/man1/bsdtar.1*

%files -n cpio
/bin/cpio
/bin/bsdcpio
%{_mandir}/man1/cpio.1*
%{_mandir}/man1/bsdcpio.1*

%files -n %{libname}
/%{_lib}/libarchive.so.%{major}*

%files -n %{develname}
/%{_lib}/%{name}*.so
%{_libdir}/pkgconfig/libarchive.pc
%{_includedir}/*.h
%{_mandir}/man3/*
%{_mandir}/man5/*
