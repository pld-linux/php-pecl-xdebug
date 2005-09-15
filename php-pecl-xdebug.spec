%define		_modname	xdebug
%define		_status		stable
%define		_sysconfdir	/etc/php
%define		extensionsdir	%(php-config --extension-dir 2>/dev/null)

Summary:	%{_modname} - provides functions for functions traces and profiling
Summary(pl):	%{_modname} - funkcje do ¶ledzenia i profilowania funkcji
Name:		php-pecl-%{_modname}
Version:	2.0.0
%define	_snap	beta3
Release:	0.%{_snap}.1
License:	BSD style
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{_modname}-%{version}%{_snap}.tgz
# Source0-md5:	05a688515e37f93552333f7f3e95402f
URL:		http://pecl.php.net/package/xdebug/
BuildRequires:	libedit-devel
BuildRequires:	libtool
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.238
Requires:	%{_sysconfdir}/conf.d
%{?requires_php_extension}
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

%description -l pl
Rozszerzenie Xdebug pomaga przy odpluskwianiu skryptu dostarczaj±c
du¿o warto¶ciowych informacji. Informacje przydatne do ¶ledzenia,
które mo¿e zapewniæ Xdebug, obejmuj±:

- ¶ledzenie stosu i funkcji w komunikatach b³êdów wraz z:
 - pe³nym wy¶wietlaniem parametrów dla funkcji zdefiniowanych przez
   u¿ytkownika
 - nazwami funkcji, nazwami plików i numerami linii
 - obs³ug± metod klas
- przydzielanie pamiêci
- zabezpieczenie przed nieskoñczon± rekurencj±

Xdebug dostarcza tak¿e:

- informacje do profilowania skryptów PHP
- analizê wywo³añ skryptu
- mo¿liwo¶æ ¶ledzenia skryptów interaktywnie przy pomocy klienta
  odpluskwiacza

To rozszerzenie ma w PECL status: %{_status}.

%prep
%setup -q -c

%build
cd %{_modname}-%{version}%{_snap}
phpize
%configure
%{__make}
cd debugclient
install %{_datadir}/automake/config.* .
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%configure \
	--with-libedit
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sysconfdir}/conf.d,%{extensionsdir}}

install %{_modname}-*/debugclient/debugclient $RPM_BUILD_ROOT%{_bindir}/%{_modname}-debugclient
install %{_modname}-*/modules/%{_modname}.so $RPM_BUILD_ROOT%{extensionsdir}
cat <<'EOF' > $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/%{_modname}.ini
; Enable %{_modname} extension module
zend_extension=%{_modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -f /etc/apache/conf.d/??_mod_php.conf ] || %service -q apache restart
[ ! -f /etc/httpd/httpd.conf/??_mod_php.conf ] || %service -q httpd restart

%postun
if [ "$1" = 0 ]; then
	[ ! -f /etc/apache/conf.d/??_mod_php.conf ] || %service -q apache restart
	[ ! -f /etc/httpd/httpd.conf/??_mod_php.conf ] || %service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc %{_modname}-*/{README,NEWS,Changelog,CREDITS}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{extensionsdir}/%{_modname}.so
%attr(755,root,root) %{_bindir}/*
