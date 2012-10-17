%define		php_name	php%{?php_suffix}
%define		modname	xdebug
%define		status	stable
Summary:	%{modname} - provides functions for functions traces and profiling
Summary(pl.UTF-8):	%{modname} - funkcje do śledzenia i profilowania funkcji
Name:		php-pecl-%{modname}
Version:	2.2.0
Release:	2
License:	BSD style
Group:		Development/Languages/PHP
Source0:	http://www.xdebug.org/files/xdebug-%{version}.tgz
# Source0-md5:	27d8ad8224ffab04d12eecb5997a4f5d
Source1:	%{name}.ini
URL:		http://www.xdebug.org/
BuildRequires:	%{php_name}-devel >= 4:5.2.17-8
BuildRequires:	libedit-devel
BuildRequires:	libtool
BuildRequires:	rpmbuild(macros) >= 1.579
%{?requires_zend_extension}
Conflicts:	ZendOptimizer
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Xdebug extension helps you debugging your script by providing a
lot of valuable debug information. The debug information that Xdebug
can provide includes the following:

- stack and function traces in error messages with:
 - full parameter display for user defined functions
 - function name, file name and line indications
 - support for member functions memory allocation
- protection for infinite recursions

Xdebug also provides:

- profiling information for PHP scripts
- script execution analysis
- capabilities to debug your scripts interactively with a debug client

In PECL status of this package is: %{status}.

%description -l pl.UTF-8
Rozszerzenie Xdebug pomaga przy odpluskwianiu skryptu dostarczając
dużo wartościowych informacji. Informacje przydatne do śledzenia,
które może zapewnić Xdebug, obejmują:

- śledzenie stosu i funkcji w komunikatach błędów wraz z:
 - pełnym wyświetlaniem parametrów dla funkcji zdefiniowanych przez
   użytkownika
 - nazwami funkcji, nazwami plików i numerami linii
 - obsługą metod klas
- przydzielanie pamięci
- zabezpieczenie przed nieskończoną rekurencją

Xdebug dostarcza także:

- informacje do profilowania skryptów PHP
- analizę wywołań skryptu
- możliwość śledzenia skryptów interaktywnie przy pomocy klienta
  odpluskwiacza

To rozszerzenie ma w PECL status: %{status}.

%prep
%setup -qc
mv %{modname}-%{version}*/* .
chmod +x debugclient/configure

%{__sed} -e 's#^;zend_extension.*#zend_extension=%{php_extensiondir}/%{modname}.so#' %{SOURCE1} > %{modname}.ini

%build
# libtool 2.2 build fix
if [ -f %{_aclocaldir}/ltsugar.m4 ]; then
	cat %{_aclocaldir}/ltsugar.m4 >> config.m4
	cat %{_aclocaldir}/ltsugar.m4 >> debugclient/aclocal.m4

	cat %{_aclocaldir}/ltversion.m4 >> config.m4
	cat %{_aclocaldir}/ltversion.m4 >> debugclient/aclocal.m4

	cat %{_aclocaldir}/lt~obsolete.m4 >> config.m4
	cat %{_aclocaldir}/lt~obsolete.m4 >> debugclient/aclocal.m4

	cat %{_aclocaldir}/ltoptions.m4 >> config.m4
	cat %{_aclocaldir}/ltoptions.m4 >> debugclient/aclocal.m4

	cat %{_aclocaldir}/libtool.m4 >> debugclient/aclocal.m4
fi

phpize
%configure
%{__make}
cd debugclient
install /usr/share/automake/{config.*,depcomp} .
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%configure \
	--with-libedit
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{php_sysconfdir}/conf.d,%{php_extensiondir}}

install -p debugclient/debugclient $RPM_BUILD_ROOT%{_bindir}/%{modname}-debugclient
install -p modules/%{modname}.so $RPM_BUILD_ROOT%{php_extensiondir}
cp -a %{modname}.ini $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc README NEWS CREDITS contrib/xt.vim
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
%attr(755,root,root) %{_bindir}/xdebug-debugclient
