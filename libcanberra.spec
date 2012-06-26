%define shortname canberra 

# Majors
%define major 0
%define major_gtk 0

# Library names
%define libname %mklibname %{shortname} %{major}
%define libname_gtk %mklibname %{shortname}-gtk %{major_gtk}
%define libname_gtk3 %mklibname %{shortname}-gtk3_ %{major_gtk}
%define	libname_gtkdevel  %mklibname -d %{shortname}-gtk
%define libname_devel %mklibname -d %{shortname}

%define _with_systemd 1

Summary:	XDG compliant sound event library
Name:		libcanberra
Version:	0.29
Release:	%mkrel 1
Source0:	%{name}-%{version}.tar.xz
Source1:	%{name}-gtk-module.sh
Source2:	%{shortname}-profile-d.sh
Source3:	%{shortname}-alsa.conf
Source4:	%{shortname}-pulse.conf
Patch0:		libcanberra-0.28-underlinking.patch
License:	LGPLv2+
Group:		Sound
Url:		http://0pointer.de/lennart/projects/libcanberra/
BuildRequires:	gtk+2-devel
BuildRequires:	gtk+3-devel
BuildRequires:	libalsa-devel
BuildRequires:	libvorbis-devel
BuildRequires:	libtool-devel
BuildRequires:	gtk-doc
BuildRequires:	tdb-devel
BuildRequires:	pulseaudio-devel

# (cg) The following seem to be required to make autoreconf not moan.
BuildRequires:	gettext-devel
BuildRequires:	libGConf2-devel

%if %{_with_systemd}
BuildRequires:	udev-devel
BuildRequires:	systemd-units
%endif

%description
A small and lightweight implementation of the XDG Sound Theme Specification
(http://0pointer.de/public/sound-theme-spec.html).

%package -n %{shortname}-common
Summary:	Common files needed for libcanberra
Group:		Sound
# (cg) This is just temporary. This should really be a generic requires.
Requires:	sound-theme-freedesktop
Requires(post):  rpm-helper >= 0.24.8-1
Requires(preun): rpm-helper >= 0.24.8-1


%description -n %{shortname}-common
Common files needed for libcanberra

%package -n %{libname}
Summary:	XDG complient sound event library
Group:		System/Libraries
Requires:	%{shortname}-common

%description -n %{libname}
A small and lightweight implementation of the XDG Sound Theme Specification
(http://0pointer.de/public/sound-theme-spec.html).

%package -n %{shortname}-gtk
Summary:	GTK utilities for the %{name} XDG complient sound event library
Group:		System/Libraries
Obsoletes:	%{name}-gtk2

%description -n %{shortname}-gtk
GTK specific utilities for %{name}, a small and lightweight implementation of
the XDG Sound Theme Specification (http://0pointer.de/public/sound-theme-spec.html).

%package -n %{libname_gtk}
Summary:	GTK modules for the %{name} XDG complient sound event library
Group:		System/Libraries
Requires:	%{shortname}-gtk = %{version}-%{release}

%description -n %{libname_gtk}
GTK specific libraries for %{name}, a small and lightweight implementation of
the XDG Sound Theme Specification (http://0pointer.de/public/sound-theme-spec.html).


%package -n %{libname_gtk3}
Summary:	GTK 3 modules for the %{name} XDG complient sound event library
Group:		System/Libraries
Requires:	%{shortname}-gtk >= %{version}-%{release}
Obsoletes:	%{_lib}%{shortname}-gtk30 < 0.28-3

%description -n %{libname_gtk3}
GTK specific libraries for %{name}, a small and lightweight implementation of
the XDG Sound Theme Specification (http://0pointer.de/public/sound-theme-spec.html).

%package -n %{libname_gtkdevel}
Summary:	GTK modules for the %{name} XDG complient sound event library
Group:		System/Libraries
Provides:	%{name}-gtk-devel = %{version}-%{release}
Requires:	%{libname_gtk} = %{version}-%{release}
Requires:	%{libname_gtk3} = %{version}-%{release}
Requires:	%{libname_devel} = %{version}-%{release}

%description -n %{libname_gtkdevel}
GTK specific libraries for %{name}, a small and lightweight implementation of
the XDG Sound Theme Specification (http://0pointer.de/public/sound-theme-spec.html).

%package -n %{libname_devel}
Summary:	Headers and libraries for %{name} development
Group:		Development/C
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}

%description -n %{libname_devel}
Development files for %{name}, a small and lightweight implementation of
the XDG Sound Theme Specification (http://0pointer.de/public/sound-theme-spec.html).

%prep
%setup -q
%apply_patches

%build
%configure2_5x \
	--disable-gstreamer \
	--disable-oss \
	--disable-static \
%if !%{_with_systemd}
	--without-systemdsystemunitdir 
%else
	--with-systemdsystemunitdir=%{_unitdir}
%endif

%make

%install
rm -rf %{buildroot}
%makeinstall_std

# Remove metalink libraries
find %{buildroot} -name *.la -delete

install -D -m755  %{SOURCE1} %{buildroot}%{_sysconfdir}/X11/xinit.d/libcanberra-gtk-module.sh
install -D -m644  %{SOURCE2} %{buildroot}%{_sysconfdir}/profile.d/40canberra.sh
install -D -m644  %{SOURCE3} %{buildroot}%{_sysconfdir}/sound/profiles/alsa/canberra.conf
install -D -m644  %{SOURCE4} %{buildroot}%{_sysconfdir}/sound/profiles/pulse/canberra.conf

# Remove the multi output module until it's more stable
rm -f %{buildroot}%{_libdir}/libcanberra-%{version}/libcanberra-multi.so

# handle docs in files section
rm -rf %{buildroot}%{_defaultdocdir}

%files -n %{shortname}-common
%{_sysconfdir}/profile.d/40canberra.sh
%{_sysconfdir}/sound/profiles/alsa/canberra.conf
%{_sysconfdir}/sound/profiles/pulse/canberra.conf

%if %{_with_systemd}
%{_bindir}/canberra-boot
%{_unitdir}/canberra-system-bootup.service
%{_unitdir}/canberra-system-shutdown-reboot.service
%{_unitdir}/canberra-system-shutdown.service
%endif

%files -n %{libname}
%{_libdir}/%{name}.so.%{major}*
%dir %{_libdir}/%{name}-%{version}
%{_libdir}/%{name}-%{version}/%{name}-alsa.so
%{_libdir}/%{name}-%{version}/%{name}-pulse.so
%{_libdir}/%{name}-%{version}/%{name}-null.so

%files -n %{libname_gtk}
%{_libdir}/%{name}-gtk.so.%{major_gtk}*
%{_libdir}/gtk-2.0/modules/%{name}-gtk-module.so

%files -n %{libname_gtk3}
%dir %{_libdir}/gtk-3.0/modules
%{_libdir}/%{name}-gtk3.so.%{major_gtk}*
%{_libdir}/gtk-3.0/modules/%{name}-gtk3-module.so
%{_libdir}/gtk-3.0/modules/libcanberra-gtk-module.so

%files -n %{shortname}-gtk
%{_sysconfdir}/X11/xinit.d/libcanberra-gtk-module.sh
%{_bindir}/canberra-gtk-play
%{_datadir}/gdm/autostart/LoginWindow/libcanberra-ready-sound.desktop
%{_datadir}/gnome/autostart/libcanberra-login-sound.desktop
%{_datadir}/gnome/shutdown/libcanberra-logout-sound.sh
%{_libdir}/gnome-settings-daemon-3.0/gtk-modules/canberra-gtk-module.desktop

%files -n %{libname_gtkdevel}
%doc %{_datadir}/gtk-doc/html/%{name}
%doc README
%{_includedir}/%{shortname}-gtk.h
%{_libdir}/%{name}-gtk.so
%{_libdir}/libcanberra-gtk3.so
%{_libdir}/pkgconfig/%{name}-gtk.pc
%{_libdir}/pkgconfig/libcanberra-gtk3.pc
%{_datadir}/vala/vapi/libcanberra-gtk.vapi

%files -n %{libname_devel}
%doc README
%{_includedir}/%{shortname}.h
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_datadir}/vala/vapi/libcanberra.vapi

