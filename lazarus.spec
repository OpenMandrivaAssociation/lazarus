%define ver 1.0.1
%define snapshot 38517
%define reldate 20120905

Name:		lazarus
Version:	%{ver}.%{reldate}
Release:	7
Summary:	Component Library and IDE for Freepascal
Group:		Development/Other
# GNU Classpath style exception, see COPYING.modifiedLGPL
License:	GPLv2+ and MPLv1.1 and LGPLv2+ with exceptions
URL:		http://www.lazarus.freepascal.org/
Source0:	http://www.hu.freepascal.org/%{name}/%{name}-%{ver}-%{snapshot}-%{reldate}-src.tar.bz2
Source1:	%{name}.rpmlintrc
Patch1:		Desktop_patch.diff

BuildRequires:	fpc-src >= 2.6.0
BuildRequires:	fpc >= 2.6.0
BuildRequires:	gdk-pixbuf
BuildRequires:	gtk+
BuildRequires:	glibc
BuildRequires:	gdb
BuildRequires:	glib-devel
BuildRequires:	gdk-pixbuf-devel
BuildRequires:	gtk2-devel
BuildRequires:	desktop-file-utils
Requires:	fpc-src >= 2.6.0
Requires:	fpc >= 2.6.0
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
rm -rf debian
rm -rf tools/install/cross_unix/debian_crosswin32
rm tools/install/cross_unix/create_linux_cross_win32_deb.sh
rm tools/install/cross_unix/HowToCreate_fpc_crosswin32_deb.txt
# Remove scripts vulnerable to symlink-attacks (bug 460642)
#rm tools/convert_po_file_to_utf-8.sh
rm tools/install/build_fpc_snaphot_rpm.sh
rm tools/install/check_fpc_dependencies.sh
rm tools/install/create_fpc_deb.sh
rm tools/install/create_fpc_export_tgz.sh
rm tools/install/create_fpc_rpm.sh
rm tools/install/create_fpc-src_rpm.sh
rm tools/install/create_fpc_tgz_from_local_dir.sh
rm tools/install/create_lazarus_export_tgz.sh 

export FPCDIR=%{_datadir}/fpcsrc/
fpcmake -Tall

MAKEOPTS="-gl -gw -Fl/usr/%{_lib}"

make bigide OPT="$MAKEOPTS"
make tools OPT="$MAKEOPTS"
make lazbuild OPT="$MAKEOPTS"

# Add the ability to create gtk2-applications
export LCL_PLATFORM=gtk2
make packager/registration lazutils lcl ideintf codetools bigidecomponents OPT='-gl -gw'
export LCL_PLATFORM=
strip lazarus
strip startlazarus
strip lazbuild

%install
LAZARUSDIR=%{_libdir}/%{name}
mkdir -p %{buildroot}$LAZARUSDIR
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/pixmaps
mkdir -p %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_datadir}/mime/packages
mkdir -p %{buildroot}%{_mandir}/man1
mkdir -p %{buildroot}%{_sysconfdir}/lazarus
cp -a lazarus/* %{buildroot}$LAZARUSDIR/
  install -m 644 lazarus/images/ide_icon48x48.png %{buildroot}%{_datadir}/pixmaps/lazarus.png
  install -m 644 lazarus/install/lazarus.desktop %{buildroot}%{_datadir}/applications/lazarus.desktop
  install -m 644 lazarus/install/lazarus-mime.xml $LazBuildDir%{buildroot}%{_datadir}/mime/packages/lazarus.xml
ln -sf $LAZARUSDIR/lazarus %{buildroot}%{_bindir}/lazarus-ide
ln -sf $LAZARUSDIR/startlazarus %{buildroot}%{_bindir}/startlazarus
ln -sf $LAZARUSDIR/lazbuild %{buildroot}%{_bindir}/lazbuild
cat lazarus/install/man/man1/lazbuild.1 | gzip > %{buildroot}%{_mandir}/man1/lazbuild.1.gz
cat lazarus/install/man/man1/lazarus-ide.1 | gzip > %{buildroot}%{_mandir}/man1/lazarus-ide.1.gz
cat lazarus/install/man/man1/startlazarus.1 | gzip > %{buildroot}%{_mandir}/man1/startlazarus.1.gz
  install lazarus/tools/install/linux/editoroptions.xml %{buildroot}%{_sysconfdir}/lazarus/editoroptions.xml
# fix fpc and lazarus path  
install lazarus/tools/install/linux/environmentoptions.xml %{buildroot}%{_sysconfdir}/lazarus/environmentoptions.xml
sed -i 's/\$(FPCVER)\///g' %{buildroot}%{_sysconfdir}/lazarus/environmentoptions.xml
sed -i 's/%LazarusVersion%//g' %{buildroot}%{_sysconfdir}/lazarus/environmentoptions.xml

#Fix config path (akdengi)
sed -i 's#__LAZARUSDIR__#'$LAZARUSDIR'#g' %{buildroot}%{_sysconfdir}/lazarus/environmentoptions.xml
sed -i 's#__FPCSRCDIR__#'$FPCDIR'#g' %{buildroot}%{_sysconfdir}/lazarus/environmentoptions.xml

chmod 755 %{buildroot}%{_libdir}/%{name}/components/lazreport/tools/localize.sh

# remove gzipped man pages (uncompressed version being also in the directory, it generates a conflict with the compress_files spec-helper)
#rm -f %{buildroot}%{_mandir}/man1/*.gz

# clean %{_libdir}/%{name}
#pushd %{buildroot}%{_libdir}/%{name}
#rm -f Makefile* *.txt
#rm -rf install
#popd

%post
%{_libdir}/%{name}/tools/install/rpm/create_gtk1_links.sh

%files
%defattr(-,root,root,-)
%doc lazarus/COPYING* lazarus/README.txt
%{_libdir}/%{name}
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


%changelog
* Sun Aug 28 2011 Александр Казанцев <kazancas@mandriva.org> 0.9.30.1.32070-1mdv2011.0
+ Revision: 697267
- fix bug from non-correct path to fpcsrc and update to new bugfix snapshot

* Tue May 24 2011 Александр Казанцев <kazancas@mandriva.org> 0.9.30.1.30881-1
+ Revision: 678181
- svn fix version for new fpc 2.4.4

* Mon Mar 28 2011 Александр Казанцев <kazancas@mandriva.org> 0.9.30.1.30041-1
+ Revision: 648700
- new release 0.9.30 (fix snapshot)

* Wed Jan 26 2011 Александр Казанцев <kazancas@mandriva.org> 0.9.29.29190-1
+ Revision: 633048
-update to 0.9.29-29190 fix snapshot

* Mon Dec 27 2010 Александр Казанцев <kazancas@mandriva.org> 0.9.29.27705-1mdv2011.0
+ Revision: 625490
+ rebuild (emptylog)

* Mon Dec 06 2010 Oden Eriksson <oeriksson@mandriva.com> 0.9.28.2-5mdv2011.0
+ Revision: 612703
- the mass rebuild of 2010.1 packages

* Fri Jan 29 2010 Jérôme Brenier <incubusss@mandriva.org> 0.9.28.2-4mdv2010.1
+ Revision: 497877
- Requires: make

* Thu Dec 03 2009 Jérôme Brenier <incubusss@mandriva.org> 0.9.28.2-3mdv2010.1
+ Revision: 472753
- bump release
- fix both environmentoptions.xml files

* Wed Dec 02 2009 Jérôme Brenier <incubusss@mandriva.org> 0.9.28.2-2mdv2010.1
+ Revision: 472717
- fix environmentoptions.xml

* Wed Dec 02 2009 Jérôme Brenier <incubusss@mandriva.org> 0.9.28.2-1mdv2010.1
+ Revision: 472695
- version 0.9.8.2
- fix BuildRequires / Requires
- fix desktop file
- remove some duplicates and useless files
- fix %%files section

  + Funda Wang <fwang@mandriva.org>
    - sync with fedora's patckage
    - import lazarus


