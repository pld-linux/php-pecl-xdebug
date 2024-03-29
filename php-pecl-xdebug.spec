#
# Conditional build:
%bcond_without	vim		# make vim syntax package

# build noarch packages only for 7.0 version
%if 0%{?_pld_builder:1} && "%{?php_suffix}" != "70"
%undefine	with_vim
%endif

%define		php_name	php%{?php_suffix}
%define		modname	xdebug
Summary:	%{modname} - provides functions for functions traces and profiling
Summary(pl.UTF-8):	%{modname} - funkcje do śledzenia i profilowania funkcji
Name:		%{php_name}-pecl-%{modname}
# https://xdebug.org/docs/compat#versions
Version:	3.2.0
Release:	1
# The Xdebug License, version 1.01
# (Based on "The PHP License", version 3.0)
License:	PHP
Group:		Development/Languages/PHP
Source0:	https://xdebug.org/files/xdebug-%{version}.tgz
# Source0-md5:	2884c58679f8a41d08beb42abc156c22
Source1:	%{modname}.ini
Source2:	vim-xt-filetype.vim
URL:		https://xdebug.org/
# Need a PHP version >= 8.0.0 and < 8.3.0
BuildRequires:	%{php_name}-devel >= 4:8.0.0
BuildRequires:	%{php_name}-devel < 4:8.3.0
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
Requires:	vim-rt >= 4:7.2.170
BuildArch:	noarch

%description -n vim-syntax-xdebug
This plugin provides syntax highlighting Xdebug trace files (context
or unified).

%prep
%setup -qc
mv %{modname}-*/* .

%{__sed} -e 's#^;zend_extension.*#zend_extension=%{php_extensiondir}/%{modname}.so#' %{SOURCE1} > %{modname}.ini

install -d vim/{syntax,ftdetect}
mv contrib/xt.vim vim/syntax
cp -p %{SOURCE2} vim/ftdetect/xt.vim

%build
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{php_sysconfdir}/conf.d,%{php_extensiondir}}

install -p modules/%{modname}.so $RPM_BUILD_ROOT%{php_extensiondir}
%if "%php_major_version.%php_minor_version" >= "7.4"
# XDebug should be loaded after opcache
cp -a %{modname}.ini $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/02_%{modname}.ini
%else
cp -a %{modname}.ini $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
%endif

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
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/*%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so

%if %{with vim}
%files -n vim-syntax-xdebug
%defattr(644,root,root,755)
%{_vimdatadir}/ftdetect/xt.vim
%{_vimdatadir}/syntax/xt.vim
%endif
