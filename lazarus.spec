%define prerelease 20101015

Name:           lazarus
Version:        0.9.29.27705
Release:        %mkrel 1
Summary:        Lazarus Component Library and IDE for Freepascal
Group:          Development/Other
Packager: 	Alexander Kazancev <kazancas@mandriva.ru>
# GNU Classpath style exception, see COPYING.modifiedLGPL
License:        GPLv2+ and MPLv1.1 and LGPLv2+ with exceptions
URL:            http://www.lazarus.freepascal.org/
Source0:        http://prdownloads.sourceforge.net/%{name}/%{name}-%{version}-%{prerelease}.tar.gz
patch0:         Makefile_patch.diff
patch1:         Desktop_patch.diff
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: fpc-src >= 2.4, fpc >= 2.4, gdk-pixbuf, gtk+, glibc, gdb, glib-devel, gdk-pixbuf-devel, gtk2-devel, desktop-file-utils
Requires: fpc-src >= 2.4, fpc >= 2.4, gdk-pixbuf, gtk+, glibc, gdb, glib-devel, gdk-pixbuf-devel, binutils, gtk2-devel, glibc-devel

%description
Lazarus is a free and opensource RAD tool for freepascal using the lazarus
component library - LCL, which is also included in this package.

%prep
%setup -qc
%patch0 -p0
%patch1 -p0

%build
cd lazarus
# Remove the files for building debian-repositories
rm -rf debian
rm -rf tools/install/cross_unix/debian_crosswin32
rm tools/install/cross_unix/create_linux_cross_win32_deb.sh
rm tools/install/cross_unix/HowToCreate_fpc_crosswin32_deb.txt
# Remove scripts vulnerable to symlink-attacks (bug 460642)
rm tools/convert_po_file_to_utf-8.sh
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
make tools OPT='-gl'
make bigide OPT='-gl'
make lazbuilder OPT='-gl'
# Add the ability to create gtk2-applications
export LCL_PLATFORM=gtk2
make lcl ideintf packager/registration bigidecomponents OPT='-gl'
export LCL_PLATFORM=

%install
rm -rf %{buildroot}
make -C lazarus install INSTALL_PREFIX=%{buildroot}%{_prefix} _LIB=%{_lib}
make -C lazarus/install/man INSTALL_MANDIR=%{buildroot}%{_mandir}

install -D -p -m 0644 lazarus/install/lazarus-mime.xml $LazBuildDir%{buildroot}%{_datadir}/mime/packages/lazarus.xml
install -D -p -m 0644 lazarus/images/ide_icon48x48.png %{buildroot}%{_datadir}/pixmaps/lazarus.png
desktop-file-install \
        --dir %{buildroot}%{_datadir}/applications \
        lazarus/install/%{name}.desktop

ln -sf ../%{_lib}/%{name}/lazarus %{buildroot}%{_bindir}/lazarus-ide
ln -sf ../%{_lib}/%{name}/startlazarus %{buildroot}%{_bindir}/startlazarus
ln -sf ../%{_lib}/%{name}/lazbuild %{buildroot}%{_bindir}/lazbuild

install -D -p -m 0644 lazarus/tools/install/linux/editoroptions.xml %{buildroot}%{_sysconfdir}/lazarus/editoroptions.xml
sed -i -e 's#\%LazarusVersion\%##' -e 's#/usr/lib/lazarus/#%{_libdir}/%{name}#' -e 's#/\$(FPCVER)##' %{buildroot}%{_libdir}/%{name}/tools/install/linux/environmentoptions.xml
install %{buildroot}%{_libdir}/%{name}/tools/install/linux/environmentoptions.xml %{buildroot}%{_sysconfdir}/lazarus/environmentoptions.xml

chmod 755 %{buildroot}%{_libdir}/%{name}/components/lazreport/tools/localize.sh

# remove gzipped man pages (uncompressed version being also in the directory, it generates a conflict with the compress_files spec-helper)
rm -f %{buildroot}%{_mandir}/man1/*.gz

# clean %{_libdir}/%{name}
pushd %{buildroot}%{_libdir}/%{name}
rm -f Makefile* *.txt
rm -rf install
popd

%clean
rm -rf %{buildroot}

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