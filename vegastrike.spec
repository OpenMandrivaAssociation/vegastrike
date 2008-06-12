Name:		vegastrike
Version:	0.4.3
Release:	%mkrel 16
Summary:	3D OpenGL spaceflight simulator
License:	GPL
Group:		Games/Arcade
URL:		http://vegastrike.sourceforge.net/
Source0:	%{name}-%{version}-MDVCLEAN.tar.bz2
Source1:	%{name}-manpages.tar.bz2
Source2:	vssetup.tar.bz2
Source11:	%{name}-16x16.png
Source12:	%{name}-32x32.png
Source13:	%{name}-48x48.png
Patch0:		vegastrike-0.4.2-char-fix.patch
Patch1:		vegastrike-0.4.2-docs-fix.patch
Patch2:		vegastrike-0.4.2-launcher-fix.patch
Patch3:		vegastrike-0.4.3-makefiles-fix.patch
Patch4:		vegastrike-0.4.2-opengl-fix.patch
Patch5:		vegastrike-0.4.2-paths-fix.patch
Patch6:		vegastrike-0.4.2-posh-fix.patch
Patch8:		vegastrike-0.4.3-gcc4-fix.patch
Patch9:		vegastrike-0.4.3-64-bit.patch
Patch10:	vegastrike-0.4.3-gtk2.patch
Patch11:	vegastrike-0.4.2-vssetup-fix.patch
Patch12:	vegastrike-0.4.3-gcc41-fix.patch
Patch13:	vegastrike-0.4.3-use-system-boost.patch
Patch14:	vegastrike-0.4.3-openal.patch
Requires:	%{name}-data = %{version}
BuildRequires:	autoconf >= 2.5
BuildRequires:	gtk2-devel
BuildRequires:	freealut-devel
BuildRequires:	jpeg-devel
BuildRequires:	boost-devel
BuildRequires:	libexpat-devel
BuildRequires:	libvorbis-devel
BuildRequires:	Mesa-common-devel
BuildRequires:	mesaglu-devel
BuildRequires:	nas-devel
BuildRequires:	oggvorbis-devel
BuildRequires:	openal-devel
BuildRequires:	png-devel
BuildRequires:	python-devel
BuildRequires:	SDL_mixer-devel
BuildRequires:	SDL_net-devel
BuildRequires:	X11-devel
BuildRequires:	zlib-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Vega Strike is a GPL 3D OpenGL Action RPG space sim for
Windows/Linux that allows a player to trade and bounty hunt
in the spirit of Elite. You start in an old beat up Wayfarer
cargo ship, with endless possibility before you and just
enough cash to scrape together a life. Yet danger lurks in
the space beyond.

%prep
%setup -q -a1 -a2
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch8 -p1 -b .gcc4
%patch9 -p1 -b .64-bit
%patch10 -p1 -b .gtk2
%patch11 -p1 -b .vssetup
%patch12 -p1 -b .gcc41
%patch13 -p1 -b .boost
%patch14 -p1 -b .openal

%build
(cd vssetup/src && %make RPM_OPT_FLAGS="%{optflags}")
%{__perl} -pi -e "s#lib/python#%{_lib}/python#g" configure.in
export WANT_AUTOCONF_2_5=1
%{__aclocal}
%{__autoheader}
%{__automake} --foreign --add-missing
%{__autoconf}
%configure2_5x	--with-bindir=%{_gamesbindir} \
		--with-data-dir=%{_gamesdatadir}/%{name} \
		--enable-release \
		--enable-flags="%{optflags}" \
		--with-gl-libs=%{_prefix}/X11R6/%{_lib}
%make

%install
%{__rm} -rf %{buildroot}
(cd vssetup/src %makeinstall bindir=%{buildroot}%{_gamesbindir})
%makeinstall bindir=%{buildroot}%{_gamesbindir}
%{__install} -m 755 vsinstall %{buildroot}%{_gamesbindir}/vsinstall

%{__mkdir_p} %{buildroot}%{_mandir}
for i in *.6; do %{__install} -m 644 $i -D %{buildroot}%{_mandir}/man6/$i; done



%{__mkdir_p} %{buildroot}%{_datadir}/applications
%{__cat} > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=Vega Strike
Comment=3D OpenGL spaceflight simulator
Exec=%{_gamesbindir}/vslauncher
Icon=%{name}
Terminal=false
Type=Application
Categories=Game;Arcade;
EOF

%{__install} -m 644 %{SOURCE11} -D %{buildroot}%{_miconsdir}/%{name}.png
%{__install} -m 644 %{SOURCE12} -D %{buildroot}%{_iconsdir}/%{name}.png
%{__install} -m 644 %{SOURCE13} -D %{buildroot}%{_liconsdir}/%{name}.png

%{__install} -d %{buildroot}%{_gamesdatadir}/%{name}

%{__perl} -pi -e 's|\r$||g' README

%if %mdkversion < 200900
%post
%{update_menus}
%endif

%if %mdkversion < 200900
%postun
%{clean_menus}
%endif

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(644,root,root,755)
%doc README
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_datadir}/applications/*
%{_mandir}/man6/*
%dir %{_gamesdatadir}/%{name}
%defattr(755,root,root,755)
%{_gamesbindir}/*


