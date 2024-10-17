%define	module	vacation

%if %{_use_internal_dependency_generator}
%define __noautoreq 'pear\\(Horde.*\\)'
%else
%define _requires_exceptions pear(Horde.*)
%endif

Name:		horde-%{module}
Version:	3.2.1
Release:	4
Summary:	The Horde vacation management application
License:	GPL
Group:		System/Servers
URL:		https://www.horde.org/%{module}/
Source0:	ftp://ftp.horde.org/pub/%{module}/%{module}-h3-%{version}.tar.gz
Source2:	%{module}-horde.conf.bz2
Patch:		%{module}-2.2.1.path.patch
Requires:	horde >= 3.3.5
Requires:	vacation
Requires(post):	rpm-helper
BuildArch:	noarch

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
%patch -p0
# fix perms
chmod 644 files/*
chmod 644 lib/*.php

%build

%install
# apache configuration
install -d -m 755 %{buildroot}%{_webappconfdir}
cat > %{buildroot}%{_webappconfdir}/%{name}.conf <<EOF
# %{name} Apache configuration file

<Directory %{_datadir}/horde/%{module}/lib>
    Require all denied
</Directory>

<Directory %{_datadir}/horde/%{module}/locale>
    Require all denied
</Directory>

<Directory %{_datadir}/horde/%{module}/scripts>
    Require all denied
</Directory>

<Directory %{_datadir}/horde/%{module}/templates>
    Require all denied
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

%files
%doc LICENSE README docs
%config(noreplace) %{_webappconfdir}/%{name}.conf
%config(noreplace) %{_sysconfdir}/horde/registry.d/%{module}.php
%config(noreplace) %{_sysconfdir}/horde/%{module}
%{_datadir}/horde/%{module}
%{_localstatedir}/lib/horde/%{module}


%changelog
* Sun Aug 08 2010 Thomas Spuhler <tspuhler@mandriva.org> 3.2.1-1mdv2011.0
+ Revision: 567530
- Updated to version 2.3.4
- added version 2.3.4 source file

* Tue Aug 03 2010 Thomas Spuhler <tspuhler@mandriva.org> 3.1-7mdv2011.0
+ Revision: 565218
- Increased release for rebuild

* Mon Jan 18 2010 Guillaume Rousse <guillomovitch@mandriva.org> 3.1-6mdv2010.1
+ Revision: 493353
- rely on filetrigger for reloading apache configuration begining with 2010.1, rpm-helper macros otherwise
- restrict default access permissions to localhost only, as per new policy

* Sun Sep 20 2009 Guillaume Rousse <guillomovitch@mandriva.org> 3.1-4mdv2010.0
+ Revision: 446057
- don't forget call webapps post-installation macros to load module configuration
- new setup (simpler is better)

* Fri Sep 11 2009 Thierry Vignaud <tv@mandriva.org> 3.1-2mdv2010.0
+ Revision: 437888
- rebuild

* Fri Mar 20 2009 Guillaume Rousse <guillomovitch@mandriva.org> 3.1-1mdv2009.1
+ Revision: 359175
- update to new version 3.1

* Thu Jul 24 2008 Thierry Vignaud <tv@mandriva.org> 3.0-5mdv2009.0
+ Revision: 246879
- rebuild

  + Pixel <pixel@mandriva.com>
    - adapt to %%_localstatedir now being /var instead of /var/lib (#22312)

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Tue Dec 18 2007 Guillaume Rousse <guillomovitch@mandriva.org> 3.0-3mdv2008.1
+ Revision: 132442
- rebuild

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request


* Fri Aug 25 2006 Guillaume Rousse <guillomovitch@mandriva.org> 3.0-2mdv2007.0
- Rebuild

* Mon May 22 2006 Guillaume Rousse <guillomovitch@mandriva.org> 3.0-1mdk
- new release
- %%mkrel

* Thu Jun 30 2005 Guillaume Rousse <guillomovitch@mandriva.org> 2.2.2-2mdk 
- better fix encoding
- spec cleanup

* Mon Apr 25 2005 Guillaume Rousse <guillomovitch@mandriva.org> 2.2.2-1mdk
- New release 2.2.2
- spec cleanup

* Fri Feb 18 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.2.1-3mdk
- spec file cleanups, remove the ADVX-build stuff
- strip away annoying ^M

* Fri Jan 14 2005 Guillaume Rousse <guillomovitch@mandrake.org> 2.2.1-2mdk 
- top-level is now /var/www/horde/vacation
- config is now in /etc/horde/vacation
- other non-accessible files are now in /usr/share/horde/vacation
- no more apache configuration
- rpmbuildupdate aware
- spec cleanup

* Sat Sep 04 2004 Guillaume Rousse <guillomovitch@mandrake.org> 2.2.1-1mdk 
- first mdk release

