Name:           lazarus
Version:        0.9.24
Release:        %mkrel 1
Summary:        Lazarus Component Library and IDE for Freepascal
Group:          Development/Other
# GNU Classpath style exception, see COPYING.modifiedLGPL
License:        GPLv2+ and MPLv1.1 and LGPLv2+ with exceptions
URL:            http://www.lazarus.freepascal.org/
Source0:        http://download.sourceforge.net/%{name}/%{name}-%{version}-0.tar.gz
patch0:         Makefile_patch.diff
patch1:         Desktop_patch.diff
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires:  fpc >= 2.2.0, binutils, gdk-pixbuf-devel, glibc-devel, desktop-file-utils, gtk2-devel
Requires:       fpc >= 2.2.0, binutils, gdk-pixbuf-devel, gtk+-devel, glibc-devel, gdb

%description
Lazarus is a free and opensource RAD tool for freepascal using the lazarus
component library - LCL, which is also included in this package.

%prep
%setup -c -q
%patch0 -p0
%patch1 -p0

%build
cd lazarus
# Remove the files for building debian-repositories
rm -rf debian
rm -rf tools/install/cross_unix/debian_crosswin32
rm tools/install/cross_unix/create_linux_cross_win32_deb.sh
rm tools/install/cross_unix/HowToCreate_fpc_crosswin32_deb.txt
export FPCDIR=/usr/share/fpcsrc
fpcmake -Tall
make all OPT='-gl'
# Add the ability to create gtk2-applications
make -C lcl/interfaces/gtk2/ OPT='-gl'

%install
rm -rf %{buildroot}
make -C lazarus install INSTALL_PREFIX=%{buildroot}%{_prefix} _LIB=%{_lib}

install -D -p -m 0644 lazarus/images/ide_icon48x48.png %{buildroot}%{_datadir}/pixmaps/lazarus.png
desktop-file-install --vendor='' \
        --dir %{buildroot}%{_datadir}/applications \
        lazarus/install/%{name}.desktop

ln -sf ../%{_lib}/%{name}/lazarus %{buildroot}%{_bindir}/lazarus-ide
ln -sf ../%{_lib}/%{name}/startlazarus %{buildroot}%{_bindir}/startlazarus
ln -sf ../%{_lib}/%{name}/lazbuild %{buildroot}%{_bindir}/lazbuild

chmod 755 %{buildroot}%{_libdir}/lazarus/components/lazreport/doc/cvs2cl.pl
chmod 755 %{buildroot}%{_libdir}/%{name}/components/lazreport/tools/localize.sh

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
%{_datadir}/applications/*.desktop
%{_mandir}/*/*
