%define Werror_cflags %nil
%define rel 1

Name:		vegastrike
Version:	0.5.1	
Release:	%mkrel 1
Summary:	3D OpenGL spaceflight simulator
License:	GPLv2+
Group:		Games/Arcade
URL:		http://vegastrike.sourceforge.net/
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-src-%{version}.r%{rel}.tar.bz2
Source1:	%{name}-manpages.tar.bz2
Source11:	%{name}-16x16.png
Source12:	%{name}-32x32.png
Source13:	%{name}-48x48.png
Requires:	%{name}-data = %{version}
Suggests:	%{name}-sounds = %{version}
BuildRequires:	mesagl-devel
BuildRequires:	mesaglu-devel
BuildRequires:	freeglut-devel
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

%description
Vega Strike is a GPL 3D OpenGL Action RPG space sim for
Windows/Linux that allows a player to trade and bounty hunt
in the spirit of Elite. You start in an old beat up Wayfarer
cargo ship, with endless possibility before you and just
enough cash to scrape together a life. Yet danger lurks in
the space beyond.

%prep
%setup -q -n %{name}-src-%{version}.r%{rel} -a1
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
		--enable-flags="%{optflags} -fpermissive -DBOOST_PYTHON_NO_PY_SIGNATURES" \
		--enable-stencil-buffer

%make

%install
%makeinstall_std

%{__mkdir_p} %{buildroot}%{_libexecdir}/%{name}
chmod +x %{buildroot}%{_prefix}/objconv/*
mv %{buildroot}%{_prefix}/objconv/* \
	%{buildroot}%{_libexecdir}/%{name}
for i in asteroidgen base_maker mesh_xml mesher replace tempgen trisort \
	vsrextract vsrmake; do
mv %{buildroot}%{_gamesbindir}/$i %{buildroot}%{_libexecdir}/%{name};
done

%{__mkdir_p} %{buildroot}%{_mandir}
for i in *.6; do %{__install} -m 644 $i -D %{buildroot}%{_mandir}/man6/$i; done

%{__mkdir_p} %{buildroot}%{_datadir}/applications
%{__cat} > %{buildroot}%{_datadir}/applications/%{_real_vendor}-%{name}.desktop << EOF
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

%files
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


%changelog

* Tue Jul 31 2012 fwang <fwang> 0.5.1-13.mga3
+ Revision: 276859
- update install dir
- rebuild for new boost

* Sun Jul 01 2012 supp <supp> 0.5.1-12.mga3
+ Revision: 265952
- add -fpermissibe optflags as per ML recomendation to make it build
- update SPEC from beta->release
- update to final 0.5.1 release

* Wed May 30 2012 fwang <fwang> 0.5.1-11.mga3
+ Revision: 250032
- rebuild for new boost

* Sat Mar 03 2012 supp <supp> 0.5.1-10.mga2
+ Revision: 217645
- update to 0.5.1, Beta2

* Mon Nov 28 2011 fwang <fwang> 0.5.1-9.mga2
+ Revision: 173668
- rebuild for new boost

* Sun Sep 18 2011 fwang <fwang> 0.5.1-8.mga2
+ Revision: 145018
- it does not like latest ffmpeg
- br ffmpeg
- fix build with latest libpng
- rebuild for new libpng
- use freeglut
- more boost-mt fix
- link against boost-mt
- rebuild for new boost

* Sun May 15 2011 pterjan <pterjan> 0.5.1-6.mga1
+ Revision: 99038
- Rebuild for fixed find-requires

* Wed Apr 27 2011 wally <wally> 0.5.1-5.mga1
+ Revision: 92012
- use _real_vendor macro in desktop file name

* Tue Apr 26 2011 supp <supp> 0.5.1-4.mga1
+ Revision: 91785
- fix desktop file (mga#954)

* Sun Apr 03 2011 supp <supp> 0.5.1-3.mga1
+ Revision: 80032
- update to official 0.5.1 beta1 release, add suggests for speech+music

* Mon Feb 28 2011 supp <supp> 0.5.1-1.mga1
+ Revision: 61871
- update to 0.5.1 beta 1...
- imported package vegastrike

