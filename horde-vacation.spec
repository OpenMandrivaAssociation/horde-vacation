%define	module	vacation
%define	name	horde-%{module}
%define version 3.1
%define release %mkrel 1

%define _requires_exceptions pear(Horde.*)

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	The Horde vacation management application
License:	GPL
Group:		System/Servers
Source0:	ftp://ftp.horde.org/pub/%{module}/%{module}-h3-%{version}.tar.bz2
Source2:	%{module}-horde.conf.bz2
Patch:		%{module}-2.2.1.path.patch
URL:		http://www.horde.org/%{module}/
Requires:	horde >= 3.0
Requires:	vacation
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}

%description
Vacation is a Horde module for managing user e-mail "vacation notices" or
"auto-responders." It works via a local vacation program which must be
installed and functioning on the server. It supports vacation programs using
the .forward-style forwarding mechanism supported by several popular mailers,
as well as qmail and sql based implementations. While it has been released and
is in production use at many sites, it is also under heavy development in an
effort to expand and improve the module.

Right now, Vacation provides fairly complete support for managing
.forward-style vacation notices on sendmail or courier mail based systems via
an FTP transport. It also has some support for qmail and exim sql based
servers.

Vacation is part of a suite of account management modules for Horde consisting
of Accounts, Forwards, Passwd, and Vacation.

%prep
%setup -q -n %{module}-h3-%{version}
%patch
# fix perms
chmod 644 files/*
chmod 644 lib/*.php

# fix encoding
for file in `find . -type f`; do
    perl -pi -e 'BEGIN {exit unless -T $ARGV[0];} tr/\r//d;' $file
done

%build

%install
rm -rf %{buildroot}

# horde configuration
install -d -m 755 %{buildroot}%{_sysconfdir}/horde/registry.d
bzcat %{SOURCE2} > %{buildroot}%{_sysconfdir}/horde/registry.d/%{module}.php

# remove .htaccess files
find . -name .htaccess -exec rm -f {} \;

# install files
install -d -m 755 %{buildroot}%{_var}/www/horde/%{module}
install -d -m 755 %{buildroot}%{_datadir}/horde/%{module}
install -d -m 755 %{buildroot}%{_sysconfdir}/horde
install -d -m 755 %{buildroot}%{_localstatedir}/lib/horde/%{module}
cp -pR *.php %{buildroot}%{_var}/www/horde/%{module}
cp -pR files/* %{buildroot}%{_localstatedir}/lib/horde/%{module}
cp -pR lib %{buildroot}%{_datadir}/horde/%{module}
cp -pR locale %{buildroot}%{_datadir}/horde/%{module}
cp -pR scripts %{buildroot}%{_datadir}/horde/%{module}
cp -pR templates %{buildroot}%{_datadir}/horde/%{module}
cp -pR config %{buildroot}%{_sysconfdir}/horde/%{module}

# use symlinks to recreate original structure
pushd %{buildroot}%{_var}/www/horde/%{module}
ln -s ../../../..%{_sysconfdir}/horde/%{module} config
ln -s ../../../..%{_datadir}/horde/%{module}/lib .
ln -s ../../../..%{_datadir}/horde/%{module}/locale .
ln -s ../../../..%{_datadir}/horde/%{module}/templates .
ln -s ../../../..%{_localstatedir}/lib/horde/%{module} files
popd

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc LICENSE README docs
%config(noreplace) %{_sysconfdir}/horde/registry.d/%{module}.php
%config(noreplace) %{_sysconfdir}/horde/%{module}
%{_datadir}/horde/%{module}
%{_var}/www/horde/%{module}
%{_localstatedir}/lib/horde/%{module}

