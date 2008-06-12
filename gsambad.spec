Summary:	A GTK+ administation tool for the SAMBA server
Name:		gsambad
Version:	0.1.9
Release:	%mkrel 1
License:	GPLv3
Group:		System/Configuration/Networking
URL:		http://www.gadmintools.org/
Source0:	http://mange.dynalias.org/linux/gsambad/%{name}-%{version}.tar.bz2
Source1:	%{name}.pam-0.77.bz2
Source2:	%{name}.pam.bz2
Patch0:		gsambad-fix-netlogon-script.patch
BuildRequires:	gtk+2-devel
BuildRequires:	ImageMagick
Requires:	samba-server >= 3.0
Requires:	openssl
Requires:	usermode-consoleonly
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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
rm -rf %{buildroot}

%makeinstall INSTALL_USER=`id -un` INSTALL_GROUP=`id -gn`

install -d %{buildroot}%{_sysconfdir}/%{name}

# pam auth
install -d %{buildroot}%{_sysconfdir}/pam.d/
install -d %{buildroot}%{_sysconfdir}/security/console.apps


install -m 644 %{name}.pam %{buildroot}%{_sysconfdir}/pam.d/%{name}
install -m 644 etc/security/console.apps/%{name} %{buildroot}%{_sysconfdir}/security/console.apps/%{name}

## locales
%find_lang %name

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
%if %mdkversion < 200900
%update_menus
%endif
mv /bin/scripts/example.bat /home/netlogon/example.bat

%postun
%if %mdkversion < 200900
%clean_menus
%endif
rm -rf /home/netlogon/example.bat

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root,0755)
%doc COPYING AUTHORS ChangeLog
%config(noreplace) %{_sysconfdir}/pam.d/%{name}
%config(noreplace) %{_sysconfdir}/security/console.apps/%{name}
%dir %{_sysconfdir}/%{name}
%{_sbindir}/%{name}
%{_sbindir}/%{name}.real
%{_datadir}/pixmaps/*.png
%{_datadir}/pixmaps/%{name}/*.png
%{_datadir}/pixmaps/%{name}/%{name}.png
%{_datadir}/applications/*
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_bindir}/*
