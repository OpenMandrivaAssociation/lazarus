%define ver 0.9.30.1
%define snapshot 32070
%define reldate 20110828

Name:		lazarus
Version:	%{ver}.%{snapshot}
Release:	%mkrel 3
Summary:	Lazarus Component Library and IDE for Freepascal
Group:		Development/Other
# GNU Classpath style exception, see COPYING.modifiedLGPL
License:	GPLv2+ and MPLv1.1 and LGPLv2+ with exceptions
URL:		http://www.lazarus.freepascal.org/
Source0:	http://www.hu.freepascal.org/%{name}/%{name}-%{ver}-%{snapshot}-%{reldate}-src.tar.bz2
Patch1:		Desktop_patch.diff
BuildRequires:	fpc-src >= 2.4.2
BuildRequires:	fpc >= 2.4.2
BuildRequires:	gdk-pixbuf
BuildRequires:	gtk+
BuildRequires:	glibc
BuildRequires:	gdb
BuildRequires:	glib-devel
BuildRequires:	gdk-pixbuf-devel
BuildRequires:	gtk2-devel
BuildRequires:	desktop-file-utils
Requires:	fpc-src >= 2.4.2
Requires:	fpc >= 2.4.2
Requires:	gdk-pixbuf
Requires:	gtk+
Requires:	glibc
Requires:	gdb
Requires:	glib-devel
Requires:	gdk-pixbuf-devel
Requires:	binutils
Requires:	gtk2-devel
Requires:	glibc-devel
Requires:	jpeg-devel

%description
Lazarus is a free and opensource RAD tool for freepascal using the lazarus
component library - LCL, which is also included in this package.

%prep
%setup -q -c
%patch1 -p0

%build
cd lazarus
# Remove the files for building debian-repositories
%__rm -rf debian
%__rm -rf tools/install/cross_unix/debian_crosswin32
%__rm tools/install/cross_unix/create_linux_cross_win32_deb.sh
%__rm tools/install/cross_unix/HowToCreate_fpc_crosswin32_deb.txt
# Remove scripts vulnerable to symlink-attacks (bug 460642)
#rm tools/convert_po_file_to_utf-8.sh
%__rm tools/install/build_fpc_snaphot_rpm.sh
%__rm tools/install/check_fpc_dependencies.sh
%__rm tools/install/create_fpc_deb.sh
%__rm tools/install/create_fpc_export_tgz.sh
%__rm tools/install/create_fpc_rpm.sh
%__rm tools/install/create_fpc-src_rpm.sh
%__rm tools/install/create_fpc_tgz_from_local_dir.sh
%__rm tools/install/create_lazarus_export_tgz.sh 

export FPCDIR=%{_datadir}/fpcsrc/
fpcmake -Tall
MAKEOPTS="-gl -Fl/usr/%{_lib}"
%__make tools OPT="$MAKEOPTS"
%__make bigide OPT="$MAKEOPTS"
%__make lazbuilder OPT="$MAKEOPTS"

# build Qt4 interface
pushd lcl/interfaces/qt
    %__make all \
        LCL_PLATFORM=qt \
        OPT="-dUSE_QT_45 \
        -dQT_NATIVE_DIALOGS"
popd

# Add the ability to create gtk2-applications
export LCL_PLATFORM=gtk2
%__make lcl ideintf packager/registration bigidecomponents OPT='-gl'
export LCL_PLATFORM=
strip lazarus
strip startlazarus
strip lazbuild

%install
%__rm -rf %{buildroot}
LAZARUSDIR=/usr/lib/%{name}
%__mkdir_p %{buildroot}$LAZARUSDIR
%__mkdir_p %{buildroot}%{_bindir}
%__mkdir_p %{buildroot}%{_datadir}/pixmaps
%__mkdir_p %{buildroot}%{_datadir}/applications
%__mkdir_p %{buildroot}%{_datadir}/mime/packages
%__mkdir_p %{buildroot}%{_mandir}/man1
%__mkdir_p %{buildroot}%{_sysconfdir}/lazarus
%__cp -a lazarus/* %{buildroot}$LAZARUSDIR/
  install -m 644 lazarus/images/ide_icon48x48.png %{buildroot}%{_datadir}/pixmaps/lazarus.png
  install -m 644 lazarus/install/lazarus.desktop %{buildroot}%{_datadir}/applications/lazarus.desktop
  install -m 644 lazarus/install/lazarus-mime.xml $LazBuildDir%{buildroot}%{_datadir}/mime/packages/lazarus.xml
ln -sf $LAZARUSDIR/lazarus %{buildroot}%{_bindir}/lazarus-ide
ln -sf $LAZARUSDIR/startlazarus %{buildroot}%{_bindir}/startlazarus
ln -sf $LAZARUSDIR/lazbuild %{buildroot}%{_bindir}/lazbuild
%__cat lazarus/install/man/man1/lazbuild.1 | gzip > %{buildroot}%{_mandir}/man1/lazbuild.1.gz
%__cat lazarus/install/man/man1/lazarus-ide.1 | gzip > %{buildroot}%{_mandir}/man1/lazarus-ide.1.gz
%__cat lazarus/install/man/man1/startlazarus.1 | gzip > %{buildroot}%{_mandir}/man1/startlazarus.1.gz
%__install lazarus/tools/install/linux/editoroptions.xml %{buildroot}%{_sysconfdir}/lazarus/editoroptions.xml
# fix fpc and lazarus path  
%__install lazarus/tools/install/linux/environmentoptions.xml %{buildroot}%{_sysconfdir}/lazarus/environmentoptions.xml
%__sed -i 's/\$(FPCVER)\///g' %{buildroot}%{_sysconfdir}/lazarus/environmentoptions.xml
%__sed -i 's/%LazarusVersion%//g' %{buildroot}%{_sysconfdir}/lazarus/environmentoptions.xml

%__chmod 755 %{buildroot}/usr/lib/%{name}/components/lazreport/tools/localize.sh

# remove gzipped man pages (uncompressed version being also in the directory, it generates a conflict with the compress_files spec-helper)
#rm -f %{buildroot}%{_mandir}/man1/*.gz

# clean %{_libdir}/%{name}
pushd %{buildroot}/usr/lib/%{name}
%__rm -f Makefile* *.txt
%__rm -rf install
popd

%clean
%__rm -rf %{buildroot}

%post
/usr/lib/%{name}/tools/install/rpm/create_gtk1_links.sh

%files
%defattr(-,root,root,-)
%doc lazarus/COPYING* lazarus/README.txt
/usr/lib/%{name}
%{_bindir}/%{name}-ide
%{_bindir}/startlazarus
%{_bindir}/lazbuild
%{_datadir}/pixmaps/lazarus.png
%{_datadir}/applications/%{name}.desktop
%{_datadir}/mime/packages/lazarus.xml
%dir %{_sysconfdir}/lazarus
%config(noreplace) %{_sysconfdir}/lazarus/editoroptions.xml
%config(noreplace) %{_sysconfdir}/lazarus/environmentoptions.xml
%{_mandir}/*/*
