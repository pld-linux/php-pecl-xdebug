%define		_modname	xdebug
%define		_status		stable
Summary:	%{_modname} - provides functions for functions traces and profiling
Summary(pl):	%{_modname} - funkcje do ¶ledzenia i profilowania funkcji
Name:		php-pecl-%{_modname}
Version:	1.2.0
Release:	1
License:	PHP 2.02
Group:		Development/Languages/PHP
Source0:	http://pear.php.net/get/%{_modname}-%{version}.tgz
URL:		http://pear.php.net/
BuildRequires:	libtool
BuildRequires:	php-devel
Requires:	php-common
Obsoletes:	php-pear-%{_modname}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/php
%define		extensionsdir	%{_libdir}/php

%description
%{_modname} provides functions for function tracing, memory usage and
profiling.

This class has in PECL status: %{_status}.

%description -l pl
%{_modname} dostarcza funkcje do ¶ledzienia funkcji i wykorzystania
pamiêci oraz profilowania.

Ta klasa ma w PECL status: %{_status}.

%prep
%setup -q -c

%build
cd %{_modname}-%{version}
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{extensionsdir}

install %{_modname}-%{version}/modules/%{_modname}.so $RPM_BUILD_ROOT%{extensionsdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_sbindir}/php-module-install install %{_modname} %{_sysconfdir}/php-cgi.ini

%preun
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove %{_modname} %{_sysconfdir}/php-cgi.ini
fi

%files
%defattr(644,root,root,755)
%doc %{_modname}-%{version}/README
%doc %{_modname}-%{version}/NEWS
%doc %{_modname}-%{version}/Changelog
%doc %{_modname}-%{version}/CREDITS
%attr(755,root,root) %{extensionsdir}/%{_modname}.so
