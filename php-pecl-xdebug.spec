%define		_modname	xdebug
%define		_status		stable

Summary:	%{_modname} - provides functions for functions traces and profiling
Summary(pl):	%{_modname} - funkcje do �ledzenia i profilowania funkcji
Name:		php-pecl-%{_modname}
Version:	1.3.0
Release:	1
License:	BSD style
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{_modname}-%{version}.tgz
# Source0-md5:	01f3dc90efa6a089eb624abf6e0825b9
URL:		http://pecl.php.net/package/xdebug/
BuildRequires:	libtool
BuildRequires:	php-devel
Requires:	php-common
Obsoletes:	php-pear-%{_modname}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/php
%define		extensionsdir	%{_libdir}/php

%description
The Xdebug extension helps you debugging your script by providing a
lot of valuable debug information. The debug information that Xdebug
can provide includes the following:

- stack and function traces in error messages with:
  - full parameter display for user defined functions
  - function name, file name and line indications
  - support for member functions
- memory allocation
- protection for infinite recursions

Xdebug also provides:

- profiling information for PHP scripts
- script execution analysis
- capabilities to debug your scripts interactively with a debug client

This extension has in PECL status: %{_status}.

%description -l pl
Rozszerzenie Xdebug pomaga przy odpluskwianiu skryptu dostarczaj�c
du�o warto�ciowych informacji. Informacje przydatne do �ledzenia,
kt�re mo�e zapewni� Xdebug, obejmuj�:

- �ledzenie stosu i funkcji w komunikatach b��d�w wraz z:
  - pe�nym wy�wietlaniem parametr�w dla funkcji zdefiniowanych przez
    u�ytkownika
  - nazwami funkcji, nazwami plik�w i numerami linii
  - obs�ug� metod klas
- przydzielanie pami�ci
- zabezpieczenie przed niesko�czon� rekurencj�

Xdebug dostarcza tak�e:

- informacje do profilowania skrypt�w PHP
- analiz� wywo�a� skryptu
- mo�liwo�� �ledzenia skrypt�w interaktywnie przy pomocy klienta
  odpluskwiacza

To rozszerzenie ma w PECL status: %{_status}.

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
%doc %{_modname}-%{version}/{README,NEWS,Changelog,CREDITS}
%attr(755,root,root) %{extensionsdir}/%{_modname}.so
