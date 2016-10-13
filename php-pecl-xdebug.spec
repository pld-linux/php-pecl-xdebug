#
# Conditional build:
%bcond_without	vim		# make vim syntax package

# build noarch packages only for 5.5 version
%if 0%{?_pld_builder:1} && "%{?php_suffix}" != "55"
%undefine	with_vim
%endif

%define		php_name	php%{?php_suffix}
%define		modname	xdebug
Summary:	%{modname} - provides functions for functions traces and profiling
Summary(pl.UTF-8):	%{modname} - funkcje do śledzenia i profilowania funkcji
Name:		%{php_name}-pecl-%{modname}
Version:	2.4.1
Release:	1
# The Xdebug License, version 1.01
# (Based on "The PHP License", version 3.0)
License:	PHP
Group:		Development/Languages/PHP
Source0:	http://www.xdebug.org/files/xdebug-%{version}.tgz
# Source0-md5:	03f52af10108450942c9c0ac3b72637f
Source1:	%{modname}.ini
Source2:	vim-xt-filetype.vim
URL:		http://www.xdebug.org/
BuildRequires:	%{php_name}-devel >= 4:5.4.0-1
BuildRequires:	libedit-devel
BuildRequires:	libtool
BuildRequires:	rpmbuild(macros) >= 1.650
%{?requires_zend_extension}
Provides:	php(%{modname}) = %{version}
Obsoletes:	php-pecl-xdebug < 2.2.4-1
Conflicts:	ZendOptimizer
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_vimdatadir		%{_datadir}/vim

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
- code coverage analysis
- capabilities to debug your scripts interactively with a debug client

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

%package -n vim-syntax-xdebug
Summary:	Vim syntax: Xdebug trace files
Group:		Applications/Editors/Vim
Requires:	php(%{modname}) = %{version}
Requires:	vim-rt >= 4:7.2.170
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description -n vim-syntax-xdebug
This plugin provides syntax highlighting Xdebug trace files (context
or unified).

%prep
%setup -qc
mv %{modname}-%{version}*/* .
chmod +x debugclient/configure

%{__sed} -e 's#^;zend_extension.*#zend_extension=%{php_extensiondir}/%{modname}.so#' %{SOURCE1} > %{modname}.ini

install -d vim/{syntax,ftdetect}
mv contrib/xt.vim vim/syntax
cp -p %{SOURCE2} vim/ftdetect/xt.vim

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
%configure \
	--with-libedit
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{php_sysconfdir}/conf.d,%{php_extensiondir}}

install -p debugclient/debugclient $RPM_BUILD_ROOT%{_bindir}/%{modname}%{?php_suffix}-debugclient
install -p modules/%{modname}.so $RPM_BUILD_ROOT%{php_extensiondir}
cp -a %{modname}.ini $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d

%if %{with vim}
# vim syntax
install -d $RPM_BUILD_ROOT%{_vimdatadir}
cp -a vim/* $RPM_BUILD_ROOT%{_vimdatadir}
%endif

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
%doc README.rst CREDITS contrib
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
%attr(755,root,root) %{_bindir}/xdebug*-debugclient

%if %{with vim}
%files -n vim-syntax-xdebug
%defattr(644,root,root,755)
%{_vimdatadir}/ftdetect/xt.vim
%{_vimdatadir}/syntax/xt.vim
%endif
