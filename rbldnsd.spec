Summary:	Small fast daemon to serve DNSBLs
Summary(pl):	Ma³y, szybki demon obs³uguj±cy zapytania DNSBL
Name:		rbldnsd
Version:	0.991
Release:	1
License:	GPLv2+
Group:		Networking/Daemons
Vendor:		Michael Tokarev <mjt@corpit.ru>
URL:		http://www.corpit.ru/mjt/rbldnsd.html
Source0:	http://www.corpit.ru/mjt/%name/%{name}_%version.tar.gz
# Source0-md5:	f7c3642a92014e8a5712386fb32a2ab0
PreReq:		/sbin/chkconfig, /sbin/nologin, shadow-utils
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define home /var/lib/rbldns

%description
Rbldnsd is a small authoritate-only DNS nameserver designed to serve
DNS-based blocklists (DNSBLs). It may handle IP-based and name-based
blocklists.

%prep
%setup -q

%build
CFLAGS="%{rpmcflags}" CC="${CC:-%__cc}" ./configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%_sbindir,%_mandir/man8,/etc/init.d,/etc/sysconfig}
install -d $RPM_BUILD_ROOT%home
cp rbldnsd $RPM_BUILD_ROOT%_sbindir/
cp -p rbldnsd.8 $RPM_BUILD_ROOT%_mandir/man8/
cp -p debian/rbldnsd.default $RPM_BUILD_ROOT/etc/sysconfig/rbldnsd
cp -p debian/rbldnsd.init $RPM_BUILD_ROOT%{_sysconfdir}/init.d/rbldnsd
chmod +x $RPM_BUILD_ROOT%{_sysconfdir}/init.d/rbldnsd

%clean
rm -rf $RPM_BUILD_ROOT

%post
getent passwd rbldns ||
  useradd -r -d %home -M -c "rbldnsd pseudo-user" -s /sbin/nologin rbldns
/sbin/chkconfig --add rbldnsd
/etc/init.d/rbldnsd restart

%preun
if [ $1 -eq 0 ]; then
   /etc/init.d/rbldnsd stop || :
   /sbin/chkconfig --del rbldnsd
   userdel rbldns || :
fi

%files
%defattr(644,root,root,755)
%doc NEWS TODO debian/changelog CHANGES-0.81
%_sbindir/rbldnsd
%_mandir/man8/rbldnsd.8*
%config(noreplace) /etc/sysconfig/rbldnsd
%{_sysconfdir}/init.d/rbldnsd
%home
