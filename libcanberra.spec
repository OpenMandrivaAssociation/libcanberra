%define _disable_ld_no_undefined 1

%define	short	canberra
%define	major	0
%define	majgtk	0

%define	libname	%mklibname %{short} %{major}
%define	libgtk	%mklibname %{short}-gtk %{majgtk}
%define	libgtk3	%mklibname %{short}-gtk3_ %{majgtk}
%define	gtkdev	%mklibname -d %{short}-gtk
%define	gtk3dev	%mklibname -d %{short}-gtk3
%define	devname	%mklibname -d %{short}

%bcond_without	systemd

Summary:	XDG compliant sound event library
Name:		libcanberra
Version:	0.30
Release:	1
License:	LGPLv2+
Group:		Sound
URL:		http://0pointer.de/lennart/projects/libcanberra/
Source0:	http://0pointer.de/lennart/projects/libcanberra/%{name}-%{version}.tar.xz
Source1:	%{name}-gtk-module.sh
Source2:	%{short}-profile-d.sh
Source3:	%{short}-alsa.conf
Source4:	%{short}-pulse.conf
Patch1:		libcanberra-0.30-use-mdv-sounds.patch

BuildRequires:	GConf2
BuildRequires:	libtool-devel
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(gstreamer-1.0)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	pkgconfig(tdb)
BuildRequires:	pkgconfig(vorbisfile)
BuildRequires:	pkgconfig(x11)
%if %{with systemd}
BuildRequires:	pkgconfig(udev) >= 186
BuildRequires:	systemd-units
%endif

%description
A small and lightweight implementation of the XDG Sound Theme Specification
(http://0pointer.de/public/sound-theme-spec.html).

%package -n	%{short}-common
Summary:	Common files needed for libcanberra
Group:		Sound
# (cg) This is just temporary. This should really be a generic requires.
Requires:	sound-theme-freedesktop
Conflicts:	%{short}-gtk3 < 0.28-6

%description -n	%{short}-common
Common files needed for libcanberra

%package -n	%{short}-gtk3
Summary:	GTK3 utilities for the %{name} XDG complient sound event library
Group:		System/Libraries
Requires:	gtk+3.0
Requires:	%{short}-common
Obsoletes:	%{name}-gtk2

%description -n	%{short}-gtk3
GTK3 specific utilities & modules for %{name}, a small and lightweight 
implementation of the XDG Sound Theme Specification 
(http://0pointer.de/public/sound-theme-spec.html).

%package -n	%{libname}
Summary:	XDG complient sound event library
Group:		System/Libraries

%description -n	%{libname}
A small and lightweight implementation of the XDG Sound Theme Specification
(http://0pointer.de/public/sound-theme-spec.html).

%package -n	%{libgtk}
Summary:	GTK libraries for the %{name}
Group:		System/Libraries
Provides:	canberra-gtk-module
%rename		canberra-gtk

%description -n	%{libgtk}
GTK specific libraries for %{name}

%package -n	%{libgtk3}
Summary:	GTK3 libraries for the %{name}
Group:		System/Libraries

%description -n %{libgtk3}
GTK3 specific libraries for %{name}.

%package -n	%{gtkdev}
Summary:	GTK library for %{name} development
Group:		Development/C
Provides:	%{name}-gtk-devel = %{version}-%{release}
Requires:	%{libgtk} = %{version}-%{release}
# moved the gtk header file & vala to gtk3devel
Requires:	%{gtk3dev} = %{version}-%{release}

%description -n	%{gtkdev}
GTK specific development library for %{name}.

%package -n	%{gtk3dev}
Summary:	GTK3 header and library for %{name} development
Group:		Development/C
Provides:	%{name}-gtk3-devel = %{version}-%{release}
Requires:	%{libgtk3} = %{version}-%{release}

%description -n	%{gtk3dev}
GTK3 specific development library and header for %{name}.

%package -n	%{devname}
Summary:	Headers and libraries for %{name} development
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
Development files for %{name}.

%prep
%setup -q
%apply_patches

%build
%configure2_5x \
    --disable-static \
    --enable-oss \
    --disable-lynx \
%if %{with systemd}
    --with-systemdsystemunitdir=%{_unitdir}
%endif

%make

%install
%makeinstall_std

install -D -m755  %{SOURCE1} %{buildroot}%{_sysconfdir}/X11/xinit.d/libcanberra-gtk-module.sh
install -D -m644  %{SOURCE2} %{buildroot}%{_sysconfdir}/profile.d/40canberra.sh
install -D -m644  %{SOURCE3} %{buildroot}%{_sysconfdir}/sound/profiles/alsa/canberra.conf
install -D -m644  %{SOURCE4} %{buildroot}%{_sysconfdir}/sound/profiles/pulse/canberra.conf


%post -n %{short}-common
if [ $1 -eq 1 ]; then
    /bin/systemctl daemon-reload
fi
systemctl enable canberra-system-bootup.service

%preun -n %{short}-common
if [ $1 -eq 0 ]; then
    /bin/systemctl --no-reload disable canberra-system-bootup.service canberra-system-shutdown.service canberra-system-shutdown-reboot.service
    /bin/systemctl stop canberra-system-bootup.service canberra-system-shutdown.service canberra-system-shutdown-reboot.service
fi

%postun -n %{short}-common
/bin/systemctl daemon-reload

%files -n %{short}-common
%{_sysconfdir}/X11/xinit.d/libcanberra-gtk-module.sh
%{_sysconfdir}/profile.d/40canberra.sh
%{_sysconfdir}/sound/profiles/alsa/canberra.conf
%{_sysconfdir}/sound/profiles/pulse/canberra.conf
%if %{with systemd}
%{_bindir}/canberra-boot
/lib/systemd/system/canberra-system-bootup.service
/lib/systemd/system/canberra-system-shutdown-reboot.service
/lib/systemd/system/canberra-system-shutdown.service
%endif

%files -n %{short}-gtk3
%{_bindir}/canberra-gtk-play
%{_datadir}/gdm/autostart/LoginWindow/libcanberra-ready-sound.desktop
%{_datadir}/gnome/autostart/libcanberra-login-sound.desktop
%{_datadir}/gnome/shutdown/libcanberra-logout-sound.sh

%files -n %{libname}
%{_libdir}/%{name}.so.%{major}*
%dir %{_libdir}/%{name}-%{version}
%{_libdir}/%{name}-%{version}/%{name}-alsa.so
%{_libdir}/%{name}-%{version}/%{name}-gstreamer.so
%{_libdir}/%{name}-%{version}/%{name}-pulse.so
%{_libdir}/%{name}-%{version}/%{name}-multi.so
%{_libdir}/%{name}-%{version}/%{name}-null.so
%{_libdir}/%{name}-%{version}/%{name}-oss.so

%files -n %{libgtk}
%{_libdir}/%{name}-gtk.so.%{majgtk}*
%{_libdir}/gtk-2.0/modules/%{name}-gtk-module.so

%files -n %{libgtk3}
%{_libdir}/%{name}-gtk3.so.%{majgtk}*
%{_libdir}/gtk-3.0/modules/%{name}-gtk-module.so
%{_libdir}/gtk-3.0/modules/%{name}-gtk3-module.so
%{_libdir}/gnome-settings-daemon-3.0/gtk-modules/canberra-gtk-module.desktop

%files -n %{gtkdev}
%doc %{_datadir}/gtk-doc/html/%{name}
%{_libdir}/%{name}-gtk.so
%{_libdir}/pkgconfig/%{name}-gtk.pc

%files -n %{gtk3dev}
%{_libdir}/libcanberra-gtk3.so
%{_libdir}/pkgconfig/libcanberra-gtk3.pc
%{_includedir}/%{short}-gtk.h
%{_datadir}/vala/vapi/libcanberra-gtk.vapi

%files -n %{devname}
%docdir %{_docdir}/%{name}
%doc %{_docdir}/%{name}/README
%{_includedir}/%{short}.h
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_datadir}/vala/vapi/libcanberra.vapi
