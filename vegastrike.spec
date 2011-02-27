%define Werror_cflags %nil

Name:		vegastrike
Version:	0.5.0
Release:	%mkrel 12
Summary:	3D OpenGL spaceflight simulator
License:	GPLv2+
Group:		Games/Arcade
URL:		http://vegastrike.sourceforge.net/
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-src-%{version}.tar.bz2
Source1:	%{name}-manpages.tar.bz2
Source11:	%{name}-16x16.png
Source12:	%{name}-32x32.png
Source13:	%{name}-48x48.png
Patch0:		vegastrike-0.4.2-char-fix.patch
Patch1:		vegastrike-0.4.2-docs-fix.patch
Patch2:		vegastrike-0.4.2-launcher-fix.patch
Patch3:		vegastrike-0.5.0-paths-fix.patch
Patch4:		vegastrike-0.5.0-64-bit.patch
Patch5:		vegastrike-0.5.0-vssetup-fix.patch
Patch6:		vegastrike-0.5.0-openal.patch
Patch7:		vegastrike-0.4.3-sys-python.patch
Patch8:		vegastrike-0.5.0-fix-format-errors.patch
Patch9:		vegastrike-0.5.0-gcc44-fix.patch
Patch10:	vegastrike-0.5.0-gcc45.patch
Patch11:	vegastrike-0.5.0-link.patch
Patch12:	vegastrike-0.5.0-boost-make_shared.patch
Requires:	%{name}-data = %{version}
BuildRequires:	mesagl-devel
BuildRequires:	mesaglu-devel
BuildRequires:	mesaglut-devel
BuildRequires:	SDL-devel
BuildRequires:	boost-devel
BuildRequires:	expat-devel
BuildRequires:	gtk+2-devel
BuildRequires:	jpeg-devel
BuildRequires:	png-devel
BuildRequires:	zlib-devel
BuildRequires:	openal-devel
BuildRequires:	python-devel
BuildRequires:	libvorbis-devel
BuildRequires:	ogre-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Vega Strike is a GPL 3D OpenGL Action RPG space sim for
Windows/Linux that allows a player to trade and bounty hunt
in the spirit of Elite. You start in an old beat up Wayfarer
cargo ship, with endless possibility before you and just
enough cash to scrape together a life. Yet danger lurks in
the space beyond.

%prep
%setup -q -n %{name}-source-%{version} -a1
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1 -b .64-bit
%patch5 -p1 -b .vssetup
%patch6 -p1 -b .openal
%patch7 -p1 -b .sys-python
%patch8 -p1 -b .format
%patch9 -p1
%patch10 -p1
%patch11 -p0 -b .link
%patch12 -p1
iconv -f ISO-8859-1 -t UTF-8 README > README.tmp
touch -r README README.tmp
mv README.tmp README

# we want to use the system version of expat.h
rm objconv/mesher/expat.h

%build
autoreconf -fi
%configure2_5x	--bindir=%{_gamesbindir} \
		--with-data-dir=%{_gamesdatadir}/%{name} \
		--enable-release \
		--with-boost=system \
		--enable-flags="%{optflags} -DBOOST_PYTHON_NO_PY_SIGNATURES" \
		--enable-stencil-buffer

%make

%install
%{__rm} -rf %{buildroot}
%makeinstall

%{__mkdir_p} %{buildroot}%{_libexecdir}/%{name}
chmod +x %{buildroot}%{_prefix}/objconv/*
mv %{buildroot}%{_prefix}/objconv/* \
	%{buildroot}%{_libexecdir}/%{name}
for i in asteroidgen base_maker mesh_xml mesher replace tempgen trisort \
	vsrextract vsrmake; do
mv %{buildroot}%{_bindir}/$i %{buildroot}%{_libexecdir}/%{name};
done


%{__mkdir_p} %{buildroot}%{_gamesbindir}
for i in vegaserver vegastrike vssetup; do
  mv %{buildroot}%{_bindir}/$i %{buildroot}%{_gamesbindir};
done


%{__mkdir_p} %{buildroot}%{_mandir}
for i in *.6; do %{__install} -m 644 $i -D %{buildroot}%{_mandir}/man6/$i; done



%{__mkdir_p} %{buildroot}%{_datadir}/applications
%{__cat} > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=Vega Strike
Comment=3D OpenGL spaceflight simulator
Exec=%{_gamesbindir}/vegastrike
Icon=%{name}
Terminal=false
Type=Application
Categories=Game;ArcadeGame;
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
%{_libexecdir}/%{name}



