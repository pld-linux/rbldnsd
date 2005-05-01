
# TODO:
# - uid and group for rbldns user
# - proper init script, .default probably should be sysconfig

Summary:	Small fast daemon to serve DNSBLs
Summary(pl):	Ma³y, szybki demon obs³uguj±cy zapytania DNSBL
Name:		rbldnsd
Version:	0.994
Release:	0.1
License:	GPL v2+
Group:		Networking/Daemons
Vendor:		Michael Tokarev <mjt@corpit.ru>
Source0:	http://www.corpit.ru/mjt/rbldnsd/%{name}_%{version}.tar.gz
# Source0-md5:	fb27cb79de6de909568c69477bab4383
URL:		http://www.corpit.ru/mjt/rbldnsd.html
BuildRequires:	rpmbuild(macros) >= 1.202
Requires(pre):	/bin/id
Requires(pre):	/usr/sbin/useradd
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/userdel
Provides:	user(rbldns)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define 	_homedir	/var/lib/rbldns

%description
rbldnsd is a small authoritate-only DNS nameserver designed to serve
DNS-based blocklists (DNSBLs). It may handle IP-based and name-based
blocklists.

%description -l pl
rbldnsd to ma³y, wy³±cznie autorytatywny serwer nazw (DNS)
zaprojektowany do udostêpniania list blokuj±cych opartych na DNS-ie
(DNSBL). Mo¿e obs³ugiwaæ listy blokuj±ce oparte na IP lub nazwach.

%prep
%setup -q

%build
# not autoconf configure
CFLAGS="%{rpmcflags}" \
CC="%{__cc}" \
./configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8,/etc/rc.d/init.d}
install -d $RPM_BUILD_ROOT%{_homedir}

install rbldnsd $RPM_BUILD_ROOT%{_sbindir}
install rbldnsd.8 $RPM_BUILD_ROOT%{_mandir}/man8
install debian/rbldnsd.default $RPM_BUILD_ROOT/etc/rbldnsd
install debian/rbldnsd.init $RPM_BUILD_ROOT/etc/rc.d/init.d/rbldnsd

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%useradd  -r -d %{_homedir} -M -c "rbldnsd pseudo-user" -s /bin/false rbldns

%post
/sbin/chkconfig --add rbldnsd
if [ -f /var/lock/subsys/rbldnsd ]; then
	/etc/rc.d/init.d/rbldnsd restart >&2
else
	echo "Run \"/etc/rc.d/init.d/rbldnsd start\" to start rbldnsd daemon." >&2
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/rbldnsd ]; then
		/etc/rc.d/init.d/rbldnsd stop >&2 || :
	fi
	/sbin/chkconfig --del rbldnsd
fi

%postun
if [ "$1" = "0" ]; then
	%userremove rbldns
fi

%files
%defattr(644,root,root,755)
%doc NEWS TODO debian/changelog CHANGES-0.81 README.user
%attr(755,root,root) %{_sbindir}/rbldnsd
%attr(754,root,root) /etc/rc.d/init.d/rbldnsd
%config(noreplace) %verify(not md5 size mtime) /etc/rbldnsd
%{_mandir}/man8/rbldnsd.8*
%dir %{_homedir}
