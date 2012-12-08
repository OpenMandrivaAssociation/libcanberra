%define _disable_ld_no_undefined 1

%define shortname canberra 
%define major 0
%define major_gtk 0

%define libname %mklibname %{shortname} %{major}
%define libgtk %mklibname %{shortname}-gtk %{major_gtk}
%define libgtk3 %mklibname %{shortname}-gtk3_ %{major_gtk}
%define libgtkdevel %mklibname -d %{shortname}-gtk
%define libgtk3devel %mklibname -d %{shortname}-gtk3
%define develname %mklibname -d %{shortname}

%bcond_without systemd

Summary:	XDG compliant sound event library
Name:		libcanberra
Version:	0.29
Release:	3
License:	LGPLv2+
Group:		Sound
URL:		http://0pointer.de/lennart/projects/libcanberra/
Source0:	http://0pointer.de/lennart/projects/libcanberra/%{name}-%{version}.tar.xz
Source1:	%{name}-gtk-module.sh
Source2:	%{shortname}-profile-d.sh
Source3:	%{shortname}-alsa.conf
Source4:	%{shortname}-pulse.conf
Patch0:		libcanberra-0.28-underlinking.patch

BuildRequires: GConf2
BuildRequires: libtool-devel
BuildRequires: pkgconfig(alsa)
BuildRequires: pkgconfig(gstreamer-0.10)
BuildRequires: pkgconfig(gtk+-2.0)
BuildRequires: pkgconfig(gtk+-3.0)
BuildRequires: pkgconfig(libpulse)
BuildRequires: pkgconfig(tdb)
BuildRequires: pkgconfig(vorbisfile)
BuildRequires: pkgconfig(x11)
%if %{with systemd}
BuildRequires: pkgconfig(udev) >= 186
BuildRequires: systemd-units
%endif

%description
A small and lightweight implementation of the XDG Sound Theme Specification
(http://0pointer.de/public/sound-theme-spec.html).

%package -n %{shortname}-common
Summary:	Common files needed for libcanberra
Group:		Sound
# (cg) This is just temporary. This should really be a generic requires.
Requires:	sound-theme-freedesktop
Conflicts:	%{shortname}-gtk3 < 0.28-6

%description -n %{shortname}-common
Common files needed for libcanberra

%post -n %{shortname}-common
if [ $1 -eq 1 ]; then
    /bin/systemctl daemon-reload
fi
systemctl enable canberra-system-bootup.service

%preun -n %{shortname}-common
if [ $1 -eq 0 ]; then
    /bin/systemctl --no-reload disable canberra-system-bootup.service canberra-system-shutdown.service canberra-system-shutdown-reboot.service
    /bin/systemctl stop canberra-system-bootup.service canberra-system-shutdown.service canberra-system-shutdown-reboot.service
fi

%postun -n %{shortname}-common
/bin/systemctl daemon-reload

%package -n %{shortname}-gtk3
Summary:	GTK3 utilities for the %{name} XDG complient sound event library
Group:		System/Libraries
Requires:	gtk+3.0
Requires:	%{shortname}-common
Obsoletes:	%{name}-gtk2

%description -n %{shortname}-gtk3
GTK3 specific utilities & modules for %{name}, a small and lightweight 
implementation of the XDG Sound Theme Specification 
(http://0pointer.de/public/sound-theme-spec.html).

%package -n %{libname}
Summary:	XDG complient sound event library
Group:		System/Libraries

%description -n %{libname}
A small and lightweight implementation of the XDG Sound Theme Specification
(http://0pointer.de/public/sound-theme-spec.html).

%package -n %{libgtk}
Summary:	GTK libraries for the %{name}
Group:		System/Libraries
Provides:	canberra-gtk-module
%rename		canberra-gtk

%description -n %{libgtk}
GTK specific libraries for %{name}

%package -n %{libgtk3}
Summary:	GTK3 libraries for the %{name}
Group:		System/Libraries

%description -n %{libgtk3}
GTK3 specific libraries for %{name}.

%package -n %{libgtkdevel}
Summary:	GTK library for %{name} development
Group:		Development/C
Provides:	%{name}-gtk-devel = %{version}-%{release}
Requires:	%{libgtk} = %{version}-%{release}
# moved the gtk header file & vala to gtk3devel
Requires:	%{libgtk3devel} = %{version}-%{release}

%description -n %{libgtkdevel}
GTK specific development library for %{name}.

%package -n %{libgtk3devel}
Summary:	GTK3 header and library for %{name} development
Group:		Development/C
Provides:	%{name}-gtk3-devel = %{version}-%{release}
Requires:	%{libgtk3} = %{version}-%{release}

%description -n %{libgtk3devel}
GTK3 specific development library and header for %{name}.

%package -n %{develname}
Summary:	Headers and libraries for %{name} development
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{develname}
Development files for %{name}.

%prep
%setup -q
%apply_patches

%build
%configure2_5x \
    --disable-static \
    --disable-oss \
    --disable-lynx \
%if %{with systemd}
    --with-systemdsystemunitdir=%{_unitdir}
%endif

%make

%install
%makeinstall_std

# Remove metalink libraries
find %{buildroot} -name '*.la' -exec rm -f {} ';'

install -D -m755  %{SOURCE1} %{buildroot}%{_sysconfdir}/X11/xinit.d/libcanberra-gtk-module.sh
install -D -m644  %{SOURCE2} %{buildroot}%{_sysconfdir}/profile.d/40canberra.sh
install -D -m644  %{SOURCE3} %{buildroot}%{_sysconfdir}/sound/profiles/alsa/canberra.conf
install -D -m644  %{SOURCE4} %{buildroot}%{_sysconfdir}/sound/profiles/pulse/canberra.conf

%files -n %{shortname}-common
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

%files -n %{shortname}-gtk3
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

%files -n %{libgtk}
%{_libdir}/%{name}-gtk.so.%{major_gtk}*
%{_libdir}/gtk-2.0/modules/%{name}-gtk-module.so

%files -n %{libgtk3}
%{_libdir}/%{name}-gtk3.so.%{major_gtk}*
%{_libdir}/gtk-3.0/modules/%{name}-gtk-module.so
%{_libdir}/gtk-3.0/modules/%{name}-gtk3-module.so
%{_libdir}/gnome-settings-daemon-3.0/gtk-modules/canberra-gtk-module.desktop

%files -n %{libgtkdevel}
%doc %{_datadir}/gtk-doc/html/%{name}
%{_libdir}/%{name}-gtk.so
%{_libdir}/pkgconfig/%{name}-gtk.pc

%files -n %{libgtk3devel}
%{_libdir}/libcanberra-gtk3.so
%{_libdir}/pkgconfig/libcanberra-gtk3.pc
%{_includedir}/%{shortname}-gtk.h
%{_datadir}/vala/vapi/libcanberra-gtk.vapi

%files -n %{develname}
%docdir %{_docdir}/%{name}
%doc %{_docdir}/%{name}/README
%{_includedir}/%{shortname}.h
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_datadir}/vala/vapi/libcanberra.vapi


%changelog
* Sun Jul 08 2012 Tomasz Pawel Gajc <tpg@mandriva.org> 0.29-3
+ Revision: 808519
- rebuild for new udev >= 186
- enable canberra-system-bootup.service

* Tue Jun 26 2012 Matthew Dawkins <mattydaw@mandriva.org> 0.29-2
+ Revision: 807038
- fixed files list
- slight spec clean up

  + Alexander Khrukin <akhrukin@mandriva.org>
    - revert to r806781

* Tue Jun 26 2012 Alexander Khrukin <akhrukin@mandriva.org> 0.29-1
+ Revision: 806970
- synced with mageia
- version update 0.29

* Tue Jan 03 2012 Paulo Andrade <pcpa@mandriva.com.br> 0.28-6
+ Revision: 748755
- use bcond
- move file arch dependant to proper packages
- name macros to match lib packages
- provide alignment
- no need to remove multi output module
- add scriptlets for systemd and to set gconf scheme

* Tue Dec 06 2011 Matthew Dawkins <mattydaw@mandriva.org> 0.28-5
+ Revision: 738391
- removed last loop

* Tue Dec 06 2011 Matthew Dawkins <mattydaw@mandriva.org> 0.28-4
+ Revision: 738387
- rebuild
- added requires for common pkg by canberra-gtk and canberra-gtk3 pkgs
- added requires for respective gtk+2.0/3.0 by canberra-gtk and canberra-gtk3 pkgs
- dropped require for common pkg by lib

* Tue Dec 06 2011 Zé <ze@mandriva.org> 0.28-3
+ Revision: 738279
- fix release
- modules need to be installed by default, so until a better solution can be found this needs to be done this way

* Tue Dec 06 2011 Zé <ze@mandriva.org> 0.28-2
+ Revision: 738264
- enable undefined
- clean defattr
- rebuild

* Sat Nov 19 2011 Matthew Dawkins <mattydaw@mandriva.org> 0.28-1
+ Revision: 731820
- new version 0.28
- enabled gkt3 build
- moved modules to common pkg
- moved gtk modules to proper pkgs
- removed cleaned section
- disabled static build
- removed .la files
- corrected systemd configure
- shortened & corrected summaries & descriptions
- converted BRs to pkgconfig provides
- cleaned up spec
- cleaned up BRs
- removed mkrel & BuildRoot
- enabled gstreamer build

* Sun May 22 2011 Funda Wang <fwang@mandriva.org> 0.27-3
+ Revision: 677068
- rebuild to add gconf2 as req

* Mon May 02 2011 Oden Eriksson <oeriksson@mandriva.com> 0.27-2
+ Revision: 662351
- mass rebuild

* Mon Feb 21 2011 Colin Guthrie <cguthrie@mandriva.org> 0.27-1
+ Revision: 639101
- systemd support requires udev
- New version (adds systemd units for boot sounds)

  + John Balcaen <mikala@mandriva.org>
    - Split -gtk files from -devel in a -gtk-devel

* Mon Oct 11 2010 Colin Guthrie <cguthrie@mandriva.org> 0.26-1mdv2011.0
+ Revision: 584968
- New version: 0.26

* Tue Jul 13 2010 Colin Guthrie <cguthrie@mandriva.org> 0.25-1mdv2011.0
+ Revision: 552107
- New version: 0.25

* Tue Apr 27 2010 Christophe Fergeau <cfergeau@mandriva.com> 0.24-2mdv2010.1
+ Revision: 539588
- rebuild so that shared libraries are properly stripped again

* Mon Apr 19 2010 Frederic Crozat <fcrozat@mandriva.com> 0.24-1mdv2010.1
+ Revision: 536764
- Release 0.24
- Remove patches 0, 1 (merged upstream)

* Sun Feb 21 2010 Colin Guthrie <cguthrie@mandriva.org> 0.23-2mdv2010.1
+ Revision: 508983
- Add some patches from git master relating to sample playing finish notification

* Sun Feb 21 2010 Tomasz Pawel Gajc <tpg@mandriva.org> 0.23-1mdv2010.1
+ Revision: 508906
- update to new version 0.23

  + Guillaume Rousse <guillomovitch@mandriva.org>
    - files in /etc/profile.d should not be executable, but should have an order prefix

* Tue Oct 20 2009 Colin Guthrie <cguthrie@mandriva.org> 0.22-1mdv2010.0
+ Revision: 458338
- New version: 0.22 (bug fixes)

* Fri Oct 16 2009 Colin Guthrie <cguthrie@mandriva.org> 0.21-1mdv2010.0
+ Revision: 457819
- New version: wrap up my path into official release.
- Rethink my last patch to fix errors on exit.
- Add patch to prevent error on application exit.
- New version (fixes one bug with previous release)

* Wed Oct 14 2009 Colin Guthrie <cguthrie@mandriva.org> 0.19-1mdv2010.0
+ Revision: 457465
- New version (just wraps up patches we already had)

* Wed Oct 07 2009 Colin Guthrie <cguthrie@mandriva.org> 0.18-2mdv2010.0
+ Revision: 455373
- Fix XID collisions when GDK window is not an X11 windows (mdv#54010)

* Mon Sep 21 2009 Colin Guthrie <cguthrie@mandriva.org> 0.18-1mdv2010.0
+ Revision: 446449
- New version 0.18

* Mon Sep 14 2009 Colin Guthrie <cguthrie@mandriva.org> 0.17-1mdv2010.0
+ Revision: 439917
- New version: 0.17 (improved GTK/GDM integration + Vala API)

* Thu Aug 27 2009 Colin Guthrie <cguthrie@mandriva.org> 0.16-1mdv2010.0
+ Revision: 421660
- New version: 0.16

* Sun Aug 16 2009 Colin Guthrie <cguthrie@mandriva.org> 0.15-2mdv2010.0
+ Revision: 416912
- Provide CANBERRA_DRIVER env variable setter for various sound profiles.

* Thu Aug 06 2009 Colin Guthrie <cguthrie@mandriva.org> 0.15-1mdv2010.0
+ Revision: 410788
- New version: 0.15

* Sun Jul 05 2009 Colin Guthrie <cguthrie@mandriva.org> 0.14-1mdv2010.0
+ Revision: 392637
- New version (also fixes mdv#51889)

* Tue Jun 30 2009 Colin Guthrie <cguthrie@mandriva.org> 0.13-3mdv2010.0
+ Revision: 390783
- Revert the upstream nofail patch that causes things to fail pretty bad when pulse is not running (mdv#51889)

* Mon Jun 29 2009 Colin Guthrie <cguthrie@mandriva.org> 0.13-2mdv2010.0
+ Revision: 390441
- Use the canberra alsa driver if the user is not using pulseaudio (mdv#51889)

* Wed Jun 24 2009 Colin Guthrie <cguthrie@mandriva.org> 0.13-1mdv2010.0
+ Revision: 388802
- New version: 0.13

* Sat Jun 06 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 0.12-1mdv2010.0
+ Revision: 383253
- update to new version 0.12
- drop all patches, merged upstream
- correct license

* Tue Apr 21 2009 Frederic Crozat <fcrozat@mandriva.com> 0.11-4mdv2009.1
+ Revision: 368481
- Do no set GTK_MODULES under GNOME, gnome-settings-daemon handles it

* Fri Apr 03 2009 Colin Guthrie <cguthrie@mandriva.org> 0.11-3mdv2009.1
+ Revision: 363733
- Add more buildrequires (not strictly needed, but it stops autoreconf running)
- Missing buildrequire gettext-devel(not 100%% sure about this but I have it locally and it builds locally)
- Add a few fixes from upstream

* Sat Mar 28 2009 Götz Waschk <waschk@mandriva.org> 0.11-2mdv2009.1
+ Revision: 361920
- rebuild for new tdb

* Thu Jan 22 2009 Frederic Crozat <fcrozat@mandriva.com> 0.11-1mdv2009.1
+ Revision: 332433
- Release 0.11
- Remove patch0 (merged upstream)

* Sat Oct 11 2008 Colin Guthrie <cguthrie@mandriva.org> 0.10-1mdv2009.1
+ Revision: 291931
- New version: 0.10
- Enable pulse backend

* Sat Sep 13 2008 Colin Guthrie <cguthrie@mandriva.org> 0.9-3mdv2009.0
+ Revision: 284497
- Rebuild against new samba for tdb-based cache support

* Wed Sep 10 2008 Frederic Crozat <fcrozat@mandriva.com> 0.9-2mdv2009.0
+ Revision: 283533
- Patch0: start login sound later, to ensure g-s-d is already running, selecting the right sound theme

* Tue Sep 09 2008 Colin Guthrie <cguthrie@mandriva.org> 0.9-1mdv2009.0
+ Revision: 283147
- New version: 0.9

* Thu Aug 28 2008 Colin Guthrie <cguthrie@mandriva.org> 0.8-1mdv2009.0
+ Revision: 277010
- New version 0.8
- NB Gstreamer and OSS outputs are disabled as their usefulness is aligned to Mandriva setup

* Mon Aug 18 2008 Colin Guthrie <cguthrie@mandriva.org> 0.7-1mdv2009.0
+ Revision: 273123
- New version: 0.7.0
- Fix website
- Drop patches applied upstream

* Tue Aug 12 2008 Frederic Crozat <fcrozat@mandriva.com> 0.6-3mdv2009.0
+ Revision: 271084
- Patch0: disable warnings when no sound file is found

* Tue Aug 05 2008 Götz Waschk <waschk@mandriva.org> 0.6-2mdv2009.0
+ Revision: 264083
- add dep on canberra-gtk to the lib package to make it work out of the box

* Tue Aug 05 2008 Götz Waschk <waschk@mandriva.org> 0.6-1mdv2009.0
+ Revision: 263876
- fix devel deps again

  + Colin Guthrie <cguthrie@mandriva.org>
    - Fix package names to avoid lib prefix when not a library.
    - Fix registration module (drop the 'lib' prefix, it's added automatically)
    - New version: 0.6

* Tue Aug 05 2008 Götz Waschk <waschk@mandriva.org> 0.4-2mdv2009.0
+ Revision: 263850
- add missing deps to the devel package

* Mon Jul 28 2008 Colin Guthrie <cguthrie@mandriva.org> 0.4-1mdv2009.0
+ Revision: 250736
- Update to 0.4
- Add a -gtk2 subpackage (this could cause naming problems when major changes to 2 on i586)
- Add xinit.d file to define module support

* Mon Jun 16 2008 Thierry Vignaud <tv@mandriva.org> 0.3-2mdv2009.0
+ Revision: 219452
- typo fixes in descriptions

* Sun Jun 15 2008 Colin Guthrie <cguthrie@mandriva.org> 0.3-1mdv2009.0
+ Revision: 219331
- Update to 0.3
- Remove %%post scripts as now handled by file triggers
- Minor macro adjustments for less name quoting.
- import libcanberra


