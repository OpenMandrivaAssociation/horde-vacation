%define	module	vacation
%define	name	horde-%{module}
%define version 3.1
%define release %mkrel 3

%define _requires_exceptions pear(Horde.*)

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	The Horde vacation management application
License:	GPL
Group:		System/Servers
URL:		http://www.horde.org/%{module}/
Source0:	ftp://ftp.horde.org/pub/%{module}/%{module}-h3-%{version}.tar.bz2
Source2:	%{module}-horde.conf.bz2
Patch:		%{module}-2.2.1.path.patch
Requires:	horde >= 3.3.5
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

%build

%install
rm -rf %{buildroot}

# apache configuration
install -d -m 755 %{buildroot}%{_webappconfdir}
cat > %{buildroot}%{_webappconfdir}/%{name}.conf <<EOF
# %{name} Apache configuration file

<Directory %{_datadir}/horde/%{module}/lib>
    Deny from all
</Directory>

<Directory %{_datadir}/horde/%{module}/locale>
    Deny from all
</Directory>

<Directory %{_datadir}/horde/%{module}/scripts>
    Deny from all
</Directory>

<Directory %{_datadir}/horde/%{module}/templates>
    Deny from all
</Directory>
EOF

# horde configuration
install -d -m 755 %{buildroot}%{_sysconfdir}/horde/registry.d
cat > %{buildroot}%{_sysconfdir}/horde/registry.d/%{module}.php <<'EOF'
<?php
//
// Vacation Horde configuration file
//
 
$this->applications['vacation'] = array(
    'fileroot'    => $this->applications['horde']['fileroot'] . '/vacation',
    'webroot'     => $this->applications['horde']['webroot'] . '/vacation',
    'name'        => _("Vacation"),
    'status'      => 'active',
    'provides'    => 'vacation',
    'menu_parent' => 'myaccount'
);
EOF

# remove .htaccess files
find . -name .htaccess -exec rm -f {} \;

# install files
install -d -m 755 %{buildroot}%{_datadir}/horde/%{module}
install -d -m 755 %{buildroot}%{_localstatedir}/lib/horde/%{module}
cp -pR *.php %{buildroot}%{_datadir}/horde/%{module}
cp -pR files/* %{buildroot}%{_localstatedir}/lib/horde/%{module}
cp -pR lib %{buildroot}%{_datadir}/horde/%{module}
cp -pR locale %{buildroot}%{_datadir}/horde/%{module}
cp -pR scripts %{buildroot}%{_datadir}/horde/%{module}
cp -pR templates %{buildroot}%{_datadir}/horde/%{module}
cp -pR config %{buildroot}%{_sysconfdir}/horde/%{module}

install -d -m 755 %{buildroot}%{_sysconfdir}/horde
pushd %{buildroot}%{_datadir}/horde/%{module}
ln -s ../../../..%{_sysconfdir}/horde/%{module} config
popd

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc LICENSE README docs
%config(noreplace) %{_webappconfdir}/%{name}.conf
%config(noreplace) %{_sysconfdir}/horde/registry.d/%{module}.php
%config(noreplace) %{_sysconfdir}/horde/%{module}
%{_datadir}/horde/%{module}
%{_localstatedir}/lib/horde/%{module}
