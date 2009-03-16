Summary:	Small fast daemon to serve DNSBLs
Summary(pl.UTF-8):	Mały, szybki demon obsługujący zapytania DNSBL
Name:		rbldnsd
Version:	0.996b
Release:	1
License:	GPL v2+
Group:		Networking/Daemons
Source0:	http://www.corpit.ru/mjt/rbldnsd/%{name}_%{version}.tar.gz
# Source0-md5:	9a0f26f3b33764c325a96bd4c61b26fa
Source1:	%{name}.init
URL:		http://www.corpit.ru/mjt/rbldnsd.html
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Provides:	group(rbldns)
Provides:	user(rbldns)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define 	_homedir	/var/lib/rbldns
%define 	_logdir		/var/log/rbldns

%description
rbldnsd is a small authoritate-only DNS nameserver designed to serve
DNS-based blocklists (DNSBLs). It may handle IP-based and name-based
blocklists.

%description -l pl.UTF-8
rbldnsd to mały, wyłącznie autorytatywny serwer nazw (DNS)
zaprojektowany do udostępniania list blokujących opartych na DNS-ie
(DNSBL). Może obsługiwać listy blokujące oparte na IP lub nazwach.

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
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8,/etc/{sysconfig,rc.d/init.d}}
install -d $RPM_BUILD_ROOT{%{_homedir},%{_logdir}}

install rbldnsd $RPM_BUILD_ROOT%{_sbindir}
install rbldnsd.8 $RPM_BUILD_ROOT%{_mandir}/man8
install debian/rbldnsd.default $RPM_BUILD_ROOT/etc/sysconfig/rbldnsd
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/rbldnsd

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 83 rbldns
%useradd -u 37 -r -d %{_homedir} -M -g rbldns -s /bin/false -c "rbldnsd pseudo-user" rbldns

%post
/sbin/chkconfig --add rbldnsd
%service rbldnsd restart

%preun
if [ "$1" = "0" ]; then
	%service rbldnsd stop
	/sbin/chkconfig --del rbldnsd
fi

%postun
if [ "$1" = "0" ]; then
	%userremove rbldns
	%groupremove rbldns
fi

%files
%defattr(644,root,root,755)
%doc NEWS TODO debian/changelog CHANGES-0.81 README.user
%attr(755,root,root) %{_sbindir}/rbldnsd
%attr(754,root,root) /etc/rc.d/init.d/rbldnsd
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/rbldnsd
%{_mandir}/man8/rbldnsd.8*
%dir %{_homedir}
%dir %attr(775,root,rbldns) %{_logdir}
