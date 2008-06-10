%define name libcanberra 
%define shortname canberra 
%define version 0.1
%define rel 1
%define release %mkrel %rel

# Majors
%define major 0
%define major_gtk 0

# Library names
%define libname %mklibname %{shortname} %{major}
%define libname_gtk %mklibname %{shortname}-gtk %{major_gtk}
%define libname_devel %mklibname -d %{shortname}

Summary: XDG compliant sound event library
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{version}.tar.gz

License: LGPL
Group: Sound
Url: http://0pointer.de/blog/projects/sixfold-announcement.html
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: gtk+2-devel
BuildRequires: libalsa-devel
BuildRequires: libvorbis-devel
BuildRequires: libltdl-devel
BuildRequires: gtk-doc

%description
A small and lightweight impelmentation of the XDG Sound Theme Specification
(http://0pointer.de/public/sound-theme-spec.html).

%package -n %{libname}
Summary: XDG complient sound event library
Group: System/Libraries

%description -n %{libname}
A small and lightweight impelmentation of the XDG Sound Theme Specification
(http://0pointer.de/public/sound-theme-spec.html).

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%package -n %{libname_gtk}
Summary: GTK modules for the %{name} XDG complient sound event library
Group: System/Libraries

%description -n %{libname_gtk}
GTK specific libraries for %{name}, a small and lightweight impelmentation of
the XDG Sound Theme Specification (http://0pointer.de/public/sound-theme-spec.html).

%post -n %{libname_gtk} -p /sbin/ldconfig
%postun -n %{libname_gtk} -p /sbin/ldconfig


%package -n %{libname_devel}
Summary: Headers and libraries for %{name} development
Group: Development/C
Provides: %{name}-devel = %{version}-%{release}

%description -n %{libname_devel}
Development files for %{name}, a small and lightweight impelmentation of
the XDG Sound Theme Specification (http://0pointer.de/public/sound-theme-spec.html).

%prep
%setup -q

%build
%configure2_5x

%make

%install
rm -rf %{buildroot}
%makeinstall_std

# Remove static and metalink libraries
find %{buildroot} \( -name *.a -o -name *.la \) -exec rm {} \;

%clean
rm -rf %{buildroot}


%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libcanberra.so.%{major}*
%{_libdir}/libcanberra-alsa.so
%{_libdir}/libcanberra-null.so

%files -n %{libname_gtk}
%defattr(-,root,root)
%{_libdir}/libcanberra-gtk.so.%{major_gtk}*
%{_libdir}/gtk-2.0/modules/libcanberra-gtk-module.so

%files -n %{libname_devel}
%defattr(-,root,root)
%doc %{_datadir}/gtk-doc/html/%{name}
%{_includedir}/%{shortname}-gtk.h
%{_includedir}/%{shortname}.h
%{_libdir}/%{name}-gtk.so
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}-gtk.pc
%{_libdir}/pkgconfig/%{name}.pc

