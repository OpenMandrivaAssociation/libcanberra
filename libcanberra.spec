%define _disable_ld_no_undefined 1

%define shortname canberra 
%define major 0
%define major_gtk 0

%define libname %mklibname %{shortname} %{major}
%define gtkname %mklibname %{shortname}-gtk %{major_gtk}
%define gtk3name %mklibname %{shortname}-gtk3_ %{major_gtk}
%define gtkdevel  %mklibname -d %{shortname}-gtk
%define gtk3devel  %mklibname -d %{shortname}-gtk3
%define develname %mklibname -d %{shortname}

%define _with_systemd 1

Summary: XDG compliant sound event library
Name: libcanberra
Version: 0.28
Release: 2
License: LGPLv2+
Group: Sound
Url: http://0pointer.de/lennart/projects/libcanberra/
Source0: %{name}-%{version}.tar.gz
Source1: %{name}-gtk-module.sh
Source2: %{shortname}-profile-d.sh
Source3: %{shortname}-alsa.conf
Source4: %{shortname}-pulse.conf

BuildRequires: GConf2
BuildRequires: libltdl-devel
BuildRequires: pkgconfig(gstreamer-0.10)
BuildRequires: pkgconfig(gtk+-2.0)
BuildRequires: pkgconfig(gtk+-3.0)
BuildRequires: pkgconfig(alsa)
BuildRequires: pkgconfig(vorbisfile)
BuildRequires: pkgconfig(tdb)
BuildRequires: pkgconfig(libpulse)
%if %{_with_systemd}
BuildRequires: pkgconfig(udev)
BuildRequires: systemd-units
%endif

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

%description -n %{libname}
A small and lightweight implementation of the XDG Sound Theme Specification
(http://0pointer.de/public/sound-theme-spec.html).

%package -n %{shortname}-gtk
Summary: GTK module for the %{name} XDG complient sound event library
Group: System/Libraries
# all the utilies and files were moved
Requires: %{shortname}-gtk3 = %{version}-%{release}

%description -n %{shortname}-gtk
GTK specific module for %{name}

%package -n %{shortname}-gtk3
Summary: GTK3 utilities for the %{name} XDG complient sound event library
Group: System/Libraries
Obsoletes: %{name}-gtk2

%description -n %{shortname}-gtk3
GTK3 specific utilities & modules for %{name}, a small and lightweight 
implementation of the XDG Sound Theme Specification 
(http://0pointer.de/public/sound-theme-spec.html).

%preun -n %{shortname}-gtk3
%preun_uninstall_gconf_schemas %{name}

%package -n %{gtkname}
Summary: GTK libraries for the %{name}
Group: System/Libraries

%description -n %{gtkname}
GTK specific libraries for %{name}

%package -n %{gtk3name}
Summary: GTK3 libraries for the %{name}
Group: System/Libraries

%description -n %{gtk3name}
GTK3 specific libraries for %{name}.

%package -n %{gtkdevel}
Summary: GTK library for %{name} development
Group: Development/C
Provides: %{name}-gtk-devel = %{version}-%{release}
Requires: %gtkname = %{version}-%{release}
# moved the gtk header file & vala to gtk3devel
Requires: %gtk3devel = %{version}-%{release}

%description -n %{gtkdevel}
GTK specific development library for %{name}.

%package -n %{gtk3devel}
Summary: GTK3 header and library for %{name} development
Group: Development/C
Provides: %{name}-gtk3-devel = %{version}-%{release}
Requires: %gtk3name = %{version}-%{release}

%description -n %{gtk3devel}
GTK3 specific development library and header for %{name}.

%package -n %{develname}
Summary: Headers and libraries for %{name} development
Group: Development/C
Provides: %{name}-devel = %{version}-%{release}
Requires: %libname = %{version}-%{release}

%description -n %{develname}
Development files for %{name}.


%prep
%setup -q
%apply_patches

%build
%configure2_5x \
	--disable-static \
	--disable-oss \
%if %{_with_systemd}
	--with-systemdsystemunitdir=/lib/systemd/system
%endif

%make

%install
rm -rf %{buildroot}
%makeinstall_std

# Remove metalink libraries
find %{buildroot} -name '*.la' -exec rm -f {} ';'
# Remove the multi output module until it's more stable
rm -f %{buildroot}%{_libdir}/libcanberra-%{version}/libcanberra-multi.so

install -D -m755  %{SOURCE1} %{buildroot}%{_sysconfdir}/X11/xinit.d/libcanberra-gtk-module.sh
install -D -m644  %{SOURCE2} %{buildroot}%{_sysconfdir}/profile.d/40canberra.sh
install -D -m644  %{SOURCE3} %{buildroot}%{_sysconfdir}/sound/profiles/alsa/canberra.conf
install -D -m644  %{SOURCE4} %{buildroot}%{_sysconfdir}/sound/profiles/pulse/canberra.conf


%files -n %{shortname}-common
%{_sysconfdir}/profile.d/40canberra.sh
%{_sysconfdir}/sound/profiles/alsa/canberra.conf
%{_sysconfdir}/sound/profiles/pulse/canberra.conf
%dir %{_libdir}/%{name}-%{version}
%{_libdir}/%{name}-%{version}/%{name}-alsa.so
%{_libdir}/%{name}-%{version}/%{name}-gstreamer.so
%{_libdir}/%{name}-%{version}/%{name}-pulse.so
%{_libdir}/%{name}-%{version}/%{name}-null.so
%if %{_with_systemd}
%{_bindir}/canberra-boot
/lib/systemd/system/canberra-system-bootup.service
/lib/systemd/system/canberra-system-shutdown-reboot.service
/lib/systemd/system/canberra-system-shutdown.service
%endif

%files -n %{libname}
%{_libdir}/%{name}.so.%{major}*

%files -n %{gtkname}
%{_libdir}/%{name}-gtk.so.%{major_gtk}*

%files -n %{gtk3name}
%{_libdir}/%{name}-gtk3.so.%{major_gtk}*

%files -n %{shortname}-gtk
%{_libdir}/gtk-2.0/modules/%{name}-gtk-module.so

%files -n %{shortname}-gtk3
%{_sysconfdir}/gconf/schemas/libcanberra.schemas
%{_sysconfdir}/X11/xinit.d/libcanberra-gtk-module.sh
%{_bindir}/canberra-gtk-play
%{_datadir}/gdm/autostart/LoginWindow/libcanberra-ready-sound.desktop
%{_datadir}/gnome/autostart/libcanberra-login-sound.desktop
%{_datadir}/gnome/shutdown/libcanberra-logout-sound.sh
%{_libdir}/gnome-settings-daemon-3.0/gtk-modules/canberra-gtk-module.desktop
%{_libdir}/gtk-3.0/modules/%{name}-gtk-module.so
%{_libdir}/gtk-3.0/modules/%{name}-gtk3-module.so

%files -n %{gtkdevel}
%dir %{_docdir}/%{name}
%doc %{_datadir}/gtk-doc/html/%{name}
%{_libdir}/%{name}-gtk.so
%{_libdir}/pkgconfig/%{name}-gtk.pc

%files -n %{gtk3devel}
%{_libdir}/libcanberra-gtk3.so
%{_libdir}/pkgconfig/libcanberra-gtk3.pc
%{_includedir}/%{shortname}-gtk.h
%{_datadir}/vala/vapi/libcanberra-gtk.vapi

%files -n %{develname}
%doc %{_docdir}/%{name}/README
%{_includedir}/%{shortname}.h
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_datadir}/vala/vapi/libcanberra.vapi

