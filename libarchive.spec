%define	major 1
%define libname %mklibname archive %{major}
%define develname %mklibname archive -d

Summary:	Library for reading and writing streaming archives
Name:		libarchive
Version:	3.0.4
Release:	1
License:	BSD
Group:		System/Libraries
URL:		http://code.google.com/p/libarchive/
Source0:	http://libarchive.googlecode.com/files/%{name}-%{version}.tar.gz
Patch0:		libarchive-2.6.1-headers.patch
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	bzip2-devel
BuildRequires:	acl-devel
BuildRequires:	attr-devel
BuildRequires:	pkgconfig(ext2fs)
BuildRequires:	libtool
BuildRequires:	zlib-devel
BuildRequires:	pkgconfig(liblzma)
BuildRequires:	sharutils

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

%description -n	%{libname}
Libarchive is a programming library that can create and read several different
streaming archive formats, including most popular tar variants and several cpio
formats. It can also write shar archives and read ISO9660 CDROM images and ZIP
archives. The bsdtar program is an implementation of tar(1) that is built on
top of libarchive. It started as a test harness, but has grown and is now the
standard system tar for FreeBSD 5 and 6.

%package -n	%{develname}
Summary:	Development library and header files for the libarchive library
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{libname}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

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

%package -n	bsdcpio
Summary:	Copy files to and from archives
Group:		Archiving/Backup

%description -n	bsdcpio
bsdcpio copies files between archives and directories. This implementation can
extract from tar, pax, cpio, zip, jar, ar, and ISO 9660 cdrom images and can
create tar, pax, cpio, ar, and shar archives.

%prep

%setup -q
%patch0 -p0 -b .headers

%build
autoreconf -fis

%configure2_5x \
	--disable-static \
    --enable-bsdtar=shared \
    --enable-bsdcpio=shared

%make

%install
%makeinstall_std

%files -n bsdtar
%doc NEWS README
%attr(0755,root,root) %{_bindir}/bsdtar
%attr(0644,root,root) %{_mandir}/man1/bsdtar.1*

%files -n bsdcpio
%attr(0755,root,root) %{_bindir}/bsdcpio
%attr(0644,root,root) %{_mandir}/man1/bsdcpio.1*

%files -n %{libname}
%attr(0755,root,root) %{_libdir}/lib*.so.%{major}*

%files -n %{develname}
%attr(0755,root,root) %{_libdir}/*so
%attr(0644,root,root) %{_libdir}/pkgconfig/libarchive.pc
%attr(0644,root,root) %{_includedir}/*.h
%attr(0644,root,root) %{_mandir}/man3/*
%attr(0644,root,root) %{_mandir}/man5/*



%changelog
* Sat Jan 14 2012 Alexander Khrukin <akhrukin@mandriva.org> 3.0.3-1
+ Revision: 760849
- version update 3.0.3

* Tue Jan 10 2012 Alexander Khrukin <akhrukin@mandriva.org> 3.0.2-1
+ Revision: 759428
- version update 3.0.2

* Tue Dec 06 2011 Matthew Dawkins <mattydaw@mandriva.org> 2.8.5-2
+ Revision: 738429
- manually removing .la files for now
- changed BR to be more specific
- rebuild
- cleaned up spec
- removed mkrel, BuildRoot, clean section, defattr
- removed old ldconfig scriptlets
- disabled static build

* Fri Sep 09 2011 Oden Eriksson <oeriksson@mandriva.com> 2.8.5-1
+ Revision: 699097
- 2.8.5

* Fri Apr 29 2011 Oden Eriksson <oeriksson@mandriva.com> 2.8.4-3
+ Revision: 660211
- mass rebuild

* Sat Nov 27 2010 Funda Wang <fwang@mandriva.org> 2.8.4-2mdv2011.0
+ Revision: 601637
- rebuild for new liblzma

* Mon Jul 19 2010 Emmanuel Andry <eandry@mandriva.org> 2.8.4-1mdv2011.0
+ Revision: 554969
- New version 2.8.4

* Sat Mar 20 2010 Emmanuel Andry <eandry@mandriva.org> 2.8.3-1mdv2010.1
+ Revision: 525440
- New version 2.8.3

* Sun Feb 14 2010 Oden Eriksson <oeriksson@mandriva.com> 2.8.0-1mdv2010.1
+ Revision: 505805
- 2.8.0

* Fri Aug 28 2009 Frederik Himpe <fhimpe@mandriva.org> 2.7.1-1mdv2010.0
+ Revision: 422034
- update to new version 2.7.1

* Sun Jun 21 2009 Oden Eriksson <oeriksson@mandriva.com> 2.7.0-1mdv2010.0
+ Revision: 387638
- 2.7.0
- dropped one upstream patch
- rediffed one patch
- added one patch to fix build

* Sun Mar 22 2009 Funda Wang <fwang@mandriva.org> 2.6.2-1mdv2009.1
+ Revision: 360163
- new version 2.6.2

* Sun Feb 01 2009 Oden Eriksson <oeriksson@mandriva.com> 2.6.1-1mdv2009.1
+ Revision: 336156
- 2.6.1
- new url
- reconstruct autopoo
- added a header fix patch from gentoo

* Wed Jan 21 2009 Per Øyvind Karlsen <peroyvind@mandriva.org> 2.6.0-2mdv2009.1
+ Revision: 332384
- use new liblzma and also add support for new xz format (P0)
- ditch useless %%buildroot != "/" check..
- properly set dynamic build of bsdtar in stead of hackishly modify the Makefile

* Sat Jan 03 2009 Funda Wang <fwang@mandriva.org> 2.6.0-1mdv2009.1
+ Revision: 323640
- New version 2.6.0

* Thu Dec 18 2008 Oden Eriksson <oeriksson@mandriva.com> 2.5.5-2mdv2009.1
+ Revision: 315553
- rebuild

* Fri Jul 18 2008 Funda Wang <fwang@mandriva.org> 2.5.5-1mdv2009.0
+ Revision: 237992
- BR ext2fs
- New version 2.5.5

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Sat May 31 2008 Funda Wang <fwang@mandriva.org> 2.4.17-1mdv2009.0
+ Revision: 213652
- New version 2.4.17

* Mon Feb 18 2008 Thierry Vignaud <tv@mandriva.org> 2.4.11-2mdv2008.1
+ Revision: 170943
- rebuild
- fix "foobar is blabla" summary (=> "blabla") so that it looks nice in rpmdrake

* Mon Jan 21 2008 Funda Wang <fwang@mandriva.org> 2.4.11-1mdv2008.1
+ Revision: 155589
- update to new version 2.4.11

* Sun Dec 30 2007 Funda Wang <fwang@mandriva.org> 2.4.10-1mdv2008.1
+ Revision: 139575
- New version 2.4.10

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Aug 19 2007 Oden Eriksson <oeriksson@mandriva.com> 2.2.6-1mdv2008.0
+ Revision: 66729
- 2.2.6
- new major
- conform to the 2008 specs

