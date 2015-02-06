%define Werror_cflags %nil
%define rel 1

%define dataver 0.5.1

Name:		vegastrike
Version:	0.5.1.r%{rel}
Release:	4
Summary:	3D OpenGL spaceflight simulator
License:	GPLv2+
Group:		Games/Arcade
URL:		http://vegastrike.sourceforge.net/
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-src-%{version}.tar.bz2
Source1:	%{name}-manpages.tar.bz2
Source11:	%{name}-16x16.png
Source12:	%{name}-32x32.png
Source13:	%{name}-48x48.png
Patch0:		vegastrike-src-0.5.1.r1-cflags.patch
Patch1:		vegastrike-0.4.2-vssetup-fix.patch
Patch2:		vegastrike-0.5.0-glext.patch
Patch3:		vegastrike-0.5.1-music.patch
Patch4:		vegastrike-0.5.1-openal.patch
Patch5:		vegastrike-0.5.1-sys-python.patch
BuildRequires:	boost-devel
BuildRequires:	jpeg-devel
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(glut)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(expat)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(OGRE)
BuildRequires:	pkgconfig(openal)
BuildRequires:	pkgconfig(python)
BuildRequires:	pkgconfig(sdl)
BuildRequires:	pkgconfig(vorbis)
BuildRequires:	pkgconfig(zlib)
Requires:	%{name}-data >= %{dataver}
Suggests:	%{name}-sounds >= %{dataver}

%description
Vega Strike is a GPL 3D OpenGL Action RPG space sim for
Windows/Linux that allows a player to trade and bounty hunt
in the spirit of Elite. You start in an old beat up Wayfarer
cargo ship, with endless possibility before you and just
enough cash to scrape together a life. Yet danger lurks in
the space beyond.

%prep
%setup -q -n %{name}-src-%{version} -a1
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p3
%patch4 -p0
%patch5 -p0
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
		--disable-ffmpeg \
		--with-al-inc=/usr/include/AL \
		--enable-flags="%{optflags} -fpermissive -DBOOST_PYTHON_NO_PY_SIGNATURES" \
		--enable-stencil-buffer

%make

%install
%makeinstall_std

mkdir -p %{buildroot}%{_libexecdir}/%{name}
chmod +x %{buildroot}%{_prefix}/objconv/*
mv %{buildroot}%{_prefix}/objconv/* \
	%{buildroot}%{_libexecdir}/%{name}
for i in asteroidgen base_maker mesh_xml mesher replace tempgen trisort \
	vsrextract vsrmake; do
mv %{buildroot}%{_gamesbindir}/$i %{buildroot}%{_libexecdir}/%{name};
done

mkdir -p %{buildroot}%{_mandir}
for i in *.6; do %{__install} -m 644 $i -D %{buildroot}%{_mandir}/man6/$i; done

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Name=Vega Strike
Comment=3D OpenGL spaceflight simulator
Exec=%{_gamesbindir}/vegastrike
Icon=%{name}
Terminal=false
Type=Application
Categories=Game;ArcadeGame;
EOF

install -m 644 %{SOURCE11} -D %{buildroot}%{_miconsdir}/%{name}.png
install -m 644 %{SOURCE12} -D %{buildroot}%{_iconsdir}/%{name}.png
install -m 644 %{SOURCE13} -D %{buildroot}%{_liconsdir}/%{name}.png

install -d %{buildroot}%{_gamesdatadir}/%{name}

perl -pi -e 's|\r$||g' README

%files
%doc README
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_datadir}/applications/%{name}.desktop
%{_mandir}/man6/*
%dir %{_gamesdatadir}/%{name}
%defattr(755,root,root,755)
%{_gamesbindir}/*
%{_libexecdir}/%{name}

