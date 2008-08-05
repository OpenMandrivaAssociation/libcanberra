%define name libcanberra 
%define shortname canberra 
%define version 0.6
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
Source1: %{name}-gtk-module.sh
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
A small and lightweight implementation of the XDG Sound Theme Specification
(http://0pointer.de/public/sound-theme-spec.html).

%package -n %{libname}
Summary: XDG complient sound event library
Group: System/Libraries
# (cg) This is just temporary. This should really be a generic requires.
Requires: sound-theme-freedesktop

%description -n %{libname}
A small and lightweight implementation of the XDG Sound Theme Specification
(http://0pointer.de/public/sound-theme-spec.html).


%package -n %{shortname}-gtk
Summary: GTK utilities for the %{name} XDG complient sound event library
Group: System/Libraries
Obsoletes: %{name}-gtk2

%description -n %{shortname}-gtk
GTK specific utilities for %{name}, a small and lightweight implementation of
the XDG Sound Theme Specification (http://0pointer.de/public/sound-theme-spec.html).


%package -n %{libname_gtk}
Summary: GTK modules for the %{name} XDG complient sound event library
Group: System/Libraries

%description -n %{libname_gtk}
GTK specific libraries for %{name}, a small and lightweight implementation of
the XDG Sound Theme Specification (http://0pointer.de/public/sound-theme-spec.html).


%package -n %{libname_devel}
Summary: Headers and libraries for %{name} development
Group: Development/C
Provides: %{name}-devel = %{version}-%{release}
Requires: %libname = %version
Requires: %libname_gtk = %version

%description -n %{libname_devel}
Development files for %{name}, a small and lightweight implementation of
the XDG Sound Theme Specification (http://0pointer.de/public/sound-theme-spec.html).

%prep
%setup -q

%build
%configure2_5x --disable-pulse

%make

%install
rm -rf %{buildroot}
%makeinstall_std

# Remove static and metalink libraries
find %{buildroot} \( -name *.a -o -name *.la \) -exec rm {} \;
install -D -m755  %{SOURCE1} %{buildroot}%{_sysconfdir}/X11/xinit.d/libcanberra-gtk-module.sh
# Remove the multi output module until it's more stable
rm -f %{buildroot}%{_libdir}/libcanberra/libcanberra-multi.so

%clean
rm -rf %{buildroot}


%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/%{name}.so.%{major}*
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/%{name}-alsa.so
%{_libdir}/%{name}/%{name}-null.so

%files -n %{libname_gtk}
%defattr(-,root,root)
%{_libdir}/%{name}-gtk.so.%{major_gtk}*
%{_libdir}/gtk-2.0/modules/%{name}-gtk-module.so

%files -n %{shortname}-gtk
%defattr(-,root,root)
%{_sysconfdir}/X11/xinit.d/libcanberra-gtk-module.sh
%{_bindir}/canberra-gtk-play
%{_datadir}/gnome/autostart/libcanberra-login-sound.desktop
%{_datadir}/gnome/shutdown/libcanberra-logout-sound.sh


%files -n %{libname_devel}
%defattr(-,root,root)
%doc README
%doc %{_datadir}/gtk-doc/html/%{name}
%{_includedir}/%{shortname}-gtk.h
%{_includedir}/%{shortname}.h
%{_libdir}/%{name}-gtk.so
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}-gtk.pc
%{_libdir}/pkgconfig/%{name}.pc

