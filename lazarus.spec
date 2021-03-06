%define _disable_lto 1

Summary:	Lazarus Component Library and IDE for Freepascal
Name:		lazarus
Version:	2.0.12
Release:	1
# GNU Classpath style exception, see COPYING.modifiedLGPL
License:	GPLv2+ and MPLv1.1 and LGPLv2+ with exceptions
Group:		Development/Other
Url:		http://www.lazarus.freepascal.org/
Source0:	http://sourceforge.net/projects/%{name}/files/Lazarus%20Zip%20_%20GZip/Lazarus%20%{version}/%{name}-%{version}.tar.gz
Source1:	lazarus-miscellaneousoptions
Source10:	lazarus.rpmlintrc
#Patch1:		Desktop_patch.diff
Patch3:		add_gdb_settings.patch
BuildRequires:	desktop-file-utils
BuildRequires:	fpc >= 2.6.0
BuildRequires:	fpc-src >= 2.6.0
BuildRequires:	gdb
BuildRequires:	qmake5
BuildRequires:	pkgconfig(Qt5Core)
BuildRequires:	pkgconfig(Qt5Gui)
BuildRequires:	pkgconfig(Qt5Network)
BuildRequires:	pkgconfig(Qt5Widgets)
BuildRequires:	pkgconfig(Qt5PrintSupport)
BuildRequires:	pkgconfig(Qt5X11Extras)
Requires:	binutils
Requires:	fpc >= 2.6.0
Requires:	fpc-src >= 2.6.0
Requires:	gdb
Requires:	glibc-devel

%description
Lazarus is a free and opensource RAD tool for freepascal using the lazarus
component library - LCL, which is also included in this package.

%prep
%setup -q -c
#patch1 -p0
%patch3 -p0

# test
cat /etc/fpc.cfg

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

export LCL_PLATFORM=qt5
pushd lcl/interfaces/qt5/cbindings/
%{_libdir}/qt5/bin/qmake
%make_build
export LD_LIBRARY_PATH=$(pwd):$LD_LIBRARY_PATH
QTLCL="$(pwd)"
popd

fpcmake -Tall

cd components
fpcmake -Tall
cd ..

MAKEOPTS="-gl -gw -Fl/usr/%{_lib} -Fl${QTLCL}"

make bigide OPT="$MAKEOPTS"
make tools OPT="$MAKEOPTS"
make lazbuild OPT="$MAKEOPTS"

# Add the ability to create gtk2-applications
#export LCL_PLATFORM=gtk2
make packager/registration lazutils lcl codetools bigidecomponents OPT="$MAKEOPTS"
#export LCL_PLATFORM=
#strip lazarus
#strip startlazarus
#strip lazbuild

%install
export PATH="`pwd`/linker:$PATH"
LAZARUSDIR=%{_libdir}/%{name}
FPCDIR=%{_datadir}/fpcsrc/

export LCL_PLATFORM=qt5
pushd lazarus/lcl/interfaces/qt5/cbindings/
%make_install INSTALL_ROOT="%{buildroot}"
popd

mkdir -p %{buildroot}$LAZARUSDIR
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/pixmaps
mkdir -p %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_datadir}/mime/packages
mkdir -p %{buildroot}%{_mandir}/man1
mkdir -p %{buildroot}%{_sysconfdir}/lazarus
cp -a lazarus/* %{buildroot}$LAZARUSDIR/
install -m 0644 lazarus/images/ide_icon48x48.png %{buildroot}%{_datadir}/pixmaps/lazarus.png
install -m 0644 lazarus/install/lazarus.desktop %{buildroot}%{_datadir}/applications/lazarus.desktop
install -m 0644 lazarus/install/lazarus-mime.xml $LazBuildDir%{buildroot}%{_datadir}/mime/packages/lazarus.xml
ln -sf $LAZARUSDIR/lazarus %{buildroot}%{_bindir}/lazarus-ide
ln -sf $LAZARUSDIR/lazarus %{buildroot}%{_bindir}/lazarus
ln -sf $LAZARUSDIR/startlazarus %{buildroot}%{_bindir}/startlazarus
ln -sf $LAZARUSDIR/lazbuild %{buildroot}%{_bindir}/lazbuild
cp lazarus/install/man/man1/*.1 %{buildroot}%{_mandir}/man1/

# fix fpc and lazarus path
install lazarus/tools/install/linux/environmentoptions.xml %{buildroot}%{_sysconfdir}/lazarus/environmentoptions.xml
sed -i 's/\$(FPCVER)\///g' %{buildroot}%{_sysconfdir}/lazarus/environmentoptions.xml
sed -i 's/%LazarusVersion%//g' %{buildroot}%{_sysconfdir}/lazarus/environmentoptions.xml

#Fix config path (akdengi)
sed -i 's#__LAZARUSDIR__#'$LAZARUSDIR/'#g' %{buildroot}%{_sysconfdir}/lazarus/environmentoptions.xml
sed -i 's#__FPCSRCDIR__#'$FPCDIR'#g' %{buildroot}%{_sysconfdir}/lazarus/environmentoptions.xml

chmod 755 %{buildroot}%{_libdir}/%{name}/components/lazreport/tools/localize.sh

pushd %{buildroot}%{_libdir}/%{name}
rm -f *.txt
rm -rf install
popd

install -m 755 %{SOURCE1} %{buildroot}%{_bindir}/

%post
%{_libdir}/%{name}/tools/install/rpm/create_gtk1_links.sh

%postun
if [ $1 = 0 ]
then
	rm -rf %{_libdir}/%{name}
fi

%files
%doc lazarus/COPYING* lazarus/README.txt
%{_libdir}/%{name}
%{_bindir}/%{name}
%{_bindir}/%{name}-ide
%{_bindir}/startlazarus
%{_bindir}/lazbuild
%{_bindir}/%{name}-miscellaneousoptions
%{_libdir}/libQt5Pas.so*
%{_datadir}/pixmaps/lazarus.png
%{_datadir}/applications/%{name}.desktop
%{_datadir}/mime/packages/lazarus.xml
%dir %{_sysconfdir}/lazarus
%config(noreplace) %{_sysconfdir}/lazarus/environmentoptions.xml
%{_mandir}/*/*
