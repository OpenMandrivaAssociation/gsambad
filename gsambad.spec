Summary:	A GTK+ administation tool for the SAMBA server
Name:		gsambad
Version:	0.1.9
Release:	%mkrel 5
License:	GPLv3
Group:		System/Configuration/Networking
URL:		http://www.gadmintools.org/
Source0:	http://mange.dynalias.org/linux/gsambad/%{name}-%{version}.tar.bz2
Source1:	%{name}.pam-0.77.bz2
Source2:	%{name}.pam.bz2
Patch0:		gsambad-fix-netlogon-script.patch
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	imagemagick
Requires:	samba-server >= 3.0
Requires:	openssl
Requires:	usermode-consoleonly

%description
GSAMBAD is a fast and easy to use GTK+ administration tool for the
SAMBA server.

%prep

%setup -q
%patch0 

# fix conditional pam config file
%if %{mdkversion} < 200610
bzcat %{SOURCE1} > %{name}.pam
%else
bzcat %{SOURCE2} > %{name}.pam
%endif

%build

%configure2_5x

perl -pi -e 's|^#define SAMBA_USER .*|#define SAMBA_USER \"root\"|g' config.h

%make

%install

%makeinstall INSTALL_USER=`id -un` INSTALL_GROUP=`id -gn`

install -d %{buildroot}%{_sysconfdir}/%{name}

# pam auth
install -d %{buildroot}%{_sysconfdir}/pam.d/
install -d %{buildroot}%{_sysconfdir}/security/console.apps


install -m 644 %{name}.pam %{buildroot}%{_sysconfdir}/pam.d/%{name}
install -m 644 etc/security/console.apps/%{name} %{buildroot}%{_sysconfdir}/security/console.apps/%{name}

## locales
%find_lang %name || touch %{name}.lang

# Mandriva Icons
install -d %{buildroot}%{_iconsdir}
install -d %{buildroot}%{_miconsdir}
install -d %{buildroot}%{_liconsdir}
convert -geometry 48x48 pixmaps/%{name}.png %{buildroot}%{_liconsdir}/%{name}.png
convert -geometry 32x32 pixmaps/%{name}.png %{buildroot}%{_iconsdir}/%{name}.png
convert -geometry 16x16 pixmaps/%{name}.png %{buildroot}%{_miconsdir}/%{name}.png

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=Gsambad
Comment=%{summary}
Exec=%{_sbindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=Settings;Network;
EOF

# Prepare usermode entry
mv %{buildroot}%{_sbindir}/%{name} %{buildroot}%{_sbindir}/%{name}.real
ln -s %{_bindir}/consolehelper %{buildroot}%{_sbindir}/%{name}

# Scripts
install -d %{buildroot}%{_bindir}
install -m 755 scripts/gsambadpdf %{buildroot}%{_bindir}
install -m 755 scripts/example.bat %{buildroot}%{_bindir}

mkdir -p %{buildroot}%{_sysconfdir}/security/console.apps
cat > %{buildroot}%{_sysconfdir}/security/console.apps/%{name} <<_EOF_
USER=root
PROGRAM=%{_sbindir}/%{name}.real
SESSION=true
FALLBACK=false
_EOF_

rm -rf %{buildroot}%{_datadir}/doc/%{name}

%post
mv /bin/scripts/example.bat /home/netlogon/example.bat

%postun
rm -rf /home/netlogon/example.bat

%files -f %{name}.lang
%defattr(-,root,root,0755)
%doc COPYING AUTHORS ChangeLog
%config(noreplace) %{_sysconfdir}/pam.d/%{name}
%config(noreplace) %{_sysconfdir}/security/console.apps/%{name}
%dir %{_sysconfdir}/%{name}
%{_sbindir}/%{name}
%{_sbindir}/%{name}.real
%{_datadir}/pixmaps/*.png
%{_datadir}/pixmaps/%{name}/%{name}.png
%{_datadir}/applications/*
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_bindir}/*


%changelog
* Fri Dec 10 2010 Oden Eriksson <oeriksson@mandriva.com> 0.1.9-5mdv2011.0
+ Revision: 619256
- the mass rebuild of 2010.0 packages

* Fri Sep 04 2009 Thierry Vignaud <tv@mandriva.org> 0.1.9-4mdv2010.0
+ Revision: 429324
- rebuild

  + Oden Eriksson <oeriksson@mandriva.com>
    - lowercase ImageMagick

* Thu Jul 24 2008 Thierry Vignaud <tv@mandriva.org> 0.1.9-3mdv2009.0
+ Revision: 246649
- rebuild
- kill re-definition of %%buildroot on Pixel's request
- fix summary

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Fri Oct 19 2007 Funda Wang <fwang@mandriva.org> 0.1.9-1mdv2008.1
+ Revision: 100378
- update to new version 0.1.9

  + Thierry Vignaud <tv@mandriva.org>
    - s/Mandrake/Mandriva/

* Sun Aug 26 2007 Funda Wang <fwang@mandriva.org> 0.1.8-1mdv2008.0
+ Revision: 71680
- New versino 0.1.8

* Tue Aug 07 2007 Funda Wang <fwang@mandriva.org> 0.1.7-1mdv2008.0
+ Revision: 59666
- New version 0.1.7

* Sat Jul 21 2007 Funda Wang <fwang@mandriva.org> 0.1.6-1mdv2008.0
+ Revision: 54131
- New version


* Wed Jan 03 2007 Emmanuel Andry <eandry@mandriva.org> 0.1.5-1mdv2007.0
+ Revision: 103911
- New version 0.1.5

* Tue Dec 26 2006 Emmanuel Andry <eandry@mandriva.org> 0.1.3-2mdv2007.1
+ Revision: 102097
- fix menu entry (bug #27830)
- Import gsambad

* Wed Jul 19 2006 Emmanuel Andry <eandry@mandriva.org> 0.1.3-1mdv2007.0
- 0.1.3
- diff patch to avoid installation of example.bat in a static /home/netlogon
- xdg menu

* Fri May 19 2006 Emmanuel Andry <eandry@mandriva.org> 0.0.8-1mdk
- 0.0.8

* Sun May 14 2006 Emmanuel Andry <eandry@mandriva.org> 0.0.7-1mdk
- 0.0.7

* Sun Mar 05 2006 Oden Eriksson <oeriksson@mandriva.com> 0.0.4-0.beta12.1mdk
- initial Mandriva package

