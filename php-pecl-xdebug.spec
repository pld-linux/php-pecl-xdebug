%define		_modname	xdebug
%define		_status		beta
%define		_rc		rc1
Summary:	%{_modname} - provides functions for functions traces and profiling
Summary(pl):	%{_modname} - funkcje do ¶ledzenia i profilowania funkcji
Name:		php-pecl-%{_modname}
Version:	1.3.0
Release:	0.%{_rc}
License:	PHP 2.02
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{_modname}-%{version}%{_rc}.tgz
# Source0-md5:	f4077d26281c339e1339d942f0d1788b
URL:		http://pecl.php.net/package/xdebug/
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

This extension has in PEAR status: %{_status}.

%description -l pl
%{_modname} dostarcza funkcje do ¶ledzienia funkcji i wykorzystania
pamiêci oraz profilowania.

To rozszerzenie ma w PEAR status: %{_status}.

%prep
%setup -q -c

%build
cd %{_modname}-%{version}%{_rc}
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{extensionsdir}

install %{_modname}-%{version}%{_rc}/modules/%{_modname}.so $RPM_BUILD_ROOT%{extensionsdir}

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
%doc %{_modname}-%{version}%{_rc}/{README,NEWS,Changelog,CREDITS}
%attr(755,root,root) %{extensionsdir}/%{_modname}.so
