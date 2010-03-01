%define		_modname	xdebug
%define		_status		stable
%define		_sysconfdir	/etc/php
%define		extensionsdir	%(php-config --extension-dir 2>/dev/null)
%define		beta		beta3
Summary:	%{_modname} - provides functions for functions traces and profiling
Summary(pl.UTF-8):	%{_modname} - funkcje do śledzenia i profilowania funkcji
Name:		php-pecl-%{_modname}
Version:	2.1.0
Release:	0.%{beta}.1
License:	BSD style
Group:		Development/Languages/PHP
Source0:	http://www.xdebug.org/files/%{_modname}-%{version}%{beta}.tgz
# Source0-md5:	51eff76e85280ea14860bcf7dbffa899
Source1:	%{name}.ini
URL:		http://www.xdebug.org/
BuildRequires:	libedit-devel
BuildRequires:	libtool
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.465
Requires:	%{_sysconfdir}/conf.d
%{?requires_zend_extension}
Conflicts:	ZendOptimizer
Obsoletes:	php-pear-%{_modname}
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

In PECL status of this package is: %{_status}.

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

To rozszerzenie ma w PECL status: %{_status}.

%prep
%setup -q -c
mv %{_modname}-%{version}%{beta}/* .
rmdir %{_modname}-%{version}%{beta}
chmod +x debugclient/configure

sed -e 's#^;zend_extension.*#zend_extension%{?zend_zts:_ts}=%{extensionsdir}/%{_modname}.so#' %{SOURCE1} > %{_modname}.ini

%build
# libtool 2.2 build fix
if [ -f /usr/share/aclocal/ltsugar.m4 ]; then
	cat /usr/share/aclocal/ltsugar.m4 >> config.m4
	cat /usr/share/aclocal/ltsugar.m4 >> debugclient/aclocal.m4
																																													
	cat /usr/share/aclocal/ltversion.m4 >> config.m4
	cat /usr/share/aclocal/ltversion.m4 >> debugclient/aclocal.m4
																																													
	cat /usr/share/aclocal/lt~obsolete.m4 >> config.m4
	cat /usr/share/aclocal/lt~obsolete.m4 >> debugclient/aclocal.m4
																																													
	cat /usr/share/aclocal/ltoptions.m4 >> config.m4
	cat /usr/share/aclocal/ltoptions.m4 >> debugclient/aclocal.m4
																																													
	cat /usr/share/aclocal/libtool.m4 >> debugclient/aclocal.m4
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
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sysconfdir}/conf.d,%{extensionsdir}}

install debugclient/debugclient $RPM_BUILD_ROOT%{_bindir}/%{_modname}-debugclient
install modules/%{_modname}.so $RPM_BUILD_ROOT%{extensionsdir}
install %{_modname}.ini $RPM_BUILD_ROOT%{_sysconfdir}/conf.d

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
%doc README NEWS Changelog CREDITS xt.vim
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{extensionsdir}/%{_modname}.so
%attr(755,root,root) %{_bindir}/*
