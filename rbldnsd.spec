
# TODO:
# - uid and group for rbldns user
# - proper init script, .default probably should be sysconfig

Summary:	Small fast daemon to serve DNSBLs
Summary(pl):	Ma�y, szybki demon obs�uguj�cy zapytania DNSBL
Name:		rbldnsd
Version:	0.991
Release:	0.1
License:	GPL v2+
Group:		Networking/Daemons
Vendor:		Michael Tokarev <mjt@corpit.ru>
Source0:	http://www.corpit.ru/mjt/rbldnsd/%{name}_%{version}.tar.gz
# Source0-md5:	f7c3642a92014e8a5712386fb32a2ab0
URL:		http://www.corpit.ru/mjt/rbldnsd.html
Requires(pre):	/bin/id
Requires(pre):	/usr/sbin/useradd
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/userdel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define 	_homedir	/var/lib/rbldns

%description
rbldnsd is a small authoritate-only DNS nameserver designed to serve
DNS-based blocklists (DNSBLs). It may handle IP-based and name-based
blocklists.

%description -l pl
rbldnsd to ma�y, wy��cznie autorytatywny serwer nazw (DNS)
zaprojektowany do udost�pniania list blokuj�cych opartych na DNS-ie
(DNSBL). Mo�e obs�ugiwa� listy blokuj�ce oparte na IP lub nazwach.

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
if [ -n "`/bin/id -u rbldnsd 2>/dev/null`" ]; then
:
#	if [ "`/bin/id -u rbldnsd`" != "XXX" ]; then
#		echo "Error: user rbldnsd doesn't have uid=62. Correct this before installing rbldnsd." 1>&2
#		exit 1
#	fi
else
	/usr/sbin/useradd  -r -d %{_homedir} -M -c "rbldnsd pseudo-user" -s /bin/false rbldns
fi

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
	/usr/sbin/userdel rbldns || :
fi

%files
%defattr(644,root,root,755)
%doc NEWS TODO debian/changelog CHANGES-0.81
%attr(755,root,root) %{_sbindir}/rbldnsd
%attr(754,root,root) /etc/rc.d/init.d/rbldnsd
%config(noreplace) %verify(not md5 size mtime) /etc/rbldnsd
%{_mandir}/man8/rbldnsd.8*
%dir %{_homedir}
