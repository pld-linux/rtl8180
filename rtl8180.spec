#
# Conditional build:
# _without_dist_kernel          without distribution kernel
#
# TODO:
# - mv kernel-net-rlt8180.spec,v kernel-net-rtl8180.spec,v
# - remove "_24x" from Name
# - UP/SMP scheme, pass CC and CFLAGS
%define		_orig_name	rtl8180_24x

Summary:	Linux driver for WLAN card base on RTL8180
Summary(pl):	Sterownik dla Linuksa do kart bezprzewodowych na uk³adzie RTL8180
Name:		kernel-net-%{_orig_name}
Version:	1.3
%define	_rel	0.4
Release:	%{_rel}@%{_kernel_ver_str}
License:	GPL
Group:		Base/Kernel
Source0:	ftp://pld:pld@213.186.71.170/pub/rtl8180/rtl8180_linuxdrv_v13.zip
# Source0-md5:	216d363e09f2b00ff6ededd495d0757a
URL:		http://www.realtek.com.tw/downloads/downloads1-3.aspx?software=True&compamodel=RTL8180L
%{!?_without_dist_kernel:BuildRequires:	kernel-headers >= 2.4.0}}
BuildRequires:	rpmbuild(macros) >= 1.118
%{!?_without_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is driver for WLAN card based on RTL8180 for Linux.

%description -l pl
Sterownik dla Linuksa do kart WLAN opartych o uk³ad RTL8180.

%prep
%setup -q -c %{name}-%{version}

%build
%{__make} -C release

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc
install release/%{_orig_name}.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc/%{_orig_name}.o

%clean
rm -rf $RPM_BUILD_ROOT

%post
%depmod %{_kernel_ver}

%postun
%depmod %{_kernel_ver}

%files
%defattr(644,root,root,755)
#%doc readme
/lib/modules/%{_kernel_ver}/misc/*
