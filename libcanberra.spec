%define name libcanberra 
%define shortname canberra 
%define version 0.18
%define release %mkrel 1

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
Source2: %{shortname}-profile-d.sh
Source3: %{shortname}-alsa.conf
Source4: %{shortname}-pulse.conf
License: LGPLv2+
Group: Sound
Url: http://0pointer.de/lennart/projects/libcanberra/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: gtk+2-devel
BuildRequires: libalsa-devel
BuildRequires: libvorbis-devel
BuildRequires: libltdl-devel
BuildRequires: gtk-doc
BuildRequires: tdb-devel
BuildRequires: pulseaudio-devel

# (cg) The following seem to be required to make autoreconf not moan.
BuildRequires: gettext-devel
BuildRequires: libGConf2-devel

%description
A small and lightweight implementation of the XDG Sound Theme Specification
(http://0pointer.de/public/sound-theme-spec.html).

%package -n %{shortname}-common
Summary: Common files needed for libcanberra
Group: Sound
# (cg) This is just temporary. This should really be a generic requires.
Requires: sound-theme-freedesktop

%description -n %{shortname}-common
Common files needed for libcanberra


%package -n %{libname}
Summary: XDG complient sound event library
Group: System/Libraries
Requires: %{shortname}-common

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

%post -n %{shortname}-gtk
%post_install_gconf_schemas %{name}

%preun -n %{shortname}-gtk
%preun_uninstall_gconf_schemas %{name}


%package -n %{libname_gtk}
Summary: GTK modules for the %{name} XDG complient sound event library
Group: System/Libraries
Requires: %{shortname}-gtk >= %version

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
./autogen.sh -V
%configure2_5x --disable-gstreamer --disable-oss

%make

%install
rm -rf %{buildroot}
%makeinstall_std

# Remove static and metalink libraries
find %{buildroot} \( -name *.a -o -name *.la \) -exec rm {} \;
install -D -m755  %{SOURCE1} %{buildroot}%{_sysconfdir}/X11/xinit.d/libcanberra-gtk-module.sh
install -D -m755  %{SOURCE2} %{buildroot}%{_sysconfdir}/profile.d/canberra.sh
install -D -m644  %{SOURCE3} %{buildroot}%{_sysconfdir}/sound/profiles/alsa/canberra.conf
install -D -m644  %{SOURCE4} %{buildroot}%{_sysconfdir}/sound/profiles/pulse/canberra.conf
# Remove the multi output module until it's more stable
rm -f %{buildroot}%{_libdir}/libcanberra-%{version}/libcanberra-multi.so

%clean
rm -rf %{buildroot}


%files -n %{shortname}-common
%defattr(-,root,root)
%{_sysconfdir}/profile.d/canberra.sh
%{_sysconfdir}/sound/profiles/alsa/canberra.conf
%{_sysconfdir}/sound/profiles/pulse/canberra.conf


%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/%{name}.so.%{major}*
%dir %{_libdir}/%{name}-%{version}
%{_libdir}/%{name}-%{version}/%{name}-alsa.so
%{_libdir}/%{name}-%{version}/%{name}-pulse.so
%{_libdir}/%{name}-%{version}/%{name}-null.so

%files -n %{libname_gtk}
%defattr(-,root,root)
%{_libdir}/%{name}-gtk.so.%{major_gtk}*
%{_libdir}/gtk-2.0/modules/%{name}-gtk-module.so

%files -n %{shortname}-gtk
%defattr(-,root,root)
%{_sysconfdir}/gconf/schemas/libcanberra.schemas
%{_sysconfdir}/X11/xinit.d/libcanberra-gtk-module.sh
%{_bindir}/canberra-gtk-play
%{_datadir}/gdm/autostart/LoginWindow/libcanberra-ready-sound.desktop
%{_datadir}/gnome/autostart/libcanberra-login-sound.desktop
%{_datadir}/gnome/shutdown/libcanberra-logout-sound.sh

%files -n %{libname_devel}
%defattr(-,root,root)
%dir %{_docdir}/%{name}
%doc %{_docdir}/%{name}/README
%doc %{_datadir}/gtk-doc/html/%{name}
%{_includedir}/%{shortname}-gtk.h
%{_includedir}/%{shortname}.h
%{_libdir}/%{name}-gtk.so
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}-gtk.pc
%{_libdir}/pkgconfig/%{name}.pc
%{_datadir}/vala/vapi/libcanberra*.vapi
