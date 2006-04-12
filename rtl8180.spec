#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	smp		# don't build SMP module
%bcond_with	verbose		# verbose build (V=1)
#
%define		_rel	6
Summary:	Linux driver for WLAN card base on RTL8180
Summary(pl):	Sterownik dla Linuksa do kart bezprzewodowych na uk³adzie RTL8180
Name:		rtl8180
Version:	1.6
Release:	%{_rel}
License:	GPL (interface) / closed source (actual driver)
Group:		Base/Kernel
Source0:	ftp://202.65.194.18/cn/wlan/rtl8180l/%{name}_linuxdrv_v15_rh90.zip
# Source0-md5:	85ae591e666c458570ab111cdb39fadb
Patch0:		%{name}-Makefile.patch
Patch1:		%{name}-timer.patch
URL:		http://www.realtek.com.tw/downloads/downloads1-3.aspx?software=True&compamodel=RTL8180L
%{?with_dist_kernel:BuildRequires:	kernel-module-build >= 3:2.6.7}
BuildRequires:	rpmbuild(macros) >= 1.153
BuildRequires:	unzip
Obsoletes:	kernel-net-rtl8180_24x
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is driver for WLAN card based on RTL8180 for Linux.

%description -l pl
Sterownik dla Linuksa do kart WLAN opartych o uk³ad RTL8180.

%package -n kernel-net-rtl8180
Summary:	Linux driver for WLAN card base on RTL8180
Summary(pl):	Sterownik dla Linuksa do kart bezprzewodowych na uk³adzie RTL8180
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod

%description -n kernel-net-rtl8180
This is driver for WLAN card based on RTL8180 for Linux.

%description -n kernel-net-rtl8180 -l pl
Sterownik dla Linuksa do kart WLAN opartych o uk³ad RTL8180.

%package -n kernel-smp-net-rtl8180
Summary:	Linux driver for WLAN card base on RTL8180
Summary(pl):	Sterownik dla Linuksa do kart bezprzewodowych na uk³adzie RTL8180
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_smp}
Requires(post,postun):	/sbin/depmod

%description -n kernel-smp-net-rtl8180
This is driver for WLAN card based on RTL8180 for Linux.

This package contains Linux SMP module.

%description -n kernel-smp-net-rtl8180 -l pl
Sterownik dla Linuksa do kart WLAN opartych o uk³ad RTL8180.

Ten pakiet zawiera modu³ j±dra Linuksa SMP.

%prep
%setup -q -n %{name}_1.5
%patch0 -p1
%patch1 -p1

%build
for cfg in %{?with_dist_kernel:%{?with_smp:smp} up}%{!?with_dist_kernel:nondist}; do
	if [ ! -r "%{_kernelsrcdir}/config-$cfg" ]; then
		exit 1
	fi
	rm -rf include
	install -d include/{linux,config}
	ln -sf %{_kernelsrcdir}/config-$cfg .config
	ln -sf %{_kernelsrcdir}/include/linux/autoconf-$cfg.h include/linux/autoconf.h
	ln -sf %{_kernelsrcdir}/include/asm-%{_target_base_arch} include/asm
	ln -sf %{_kernelsrcdir}/Module.symvers-$cfg Module.symvers
	touch include/config/MARKER
	%{__make} -C %{_kernelsrcdir} clean modules \
		RCS_FIND_IGNORE="-name '*.ko' -o -name priv_part.o -o" \
		M=$PWD O=$PWD \
		%{?with_verbose:V=1}
	mv rtl8180_24x.ko rtl8180_24x-$cfg.ko
done

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/misc

install rtl8180_24x-%{?with_dist_kernel:up}%{!?with_dist_kernel:nondist}.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc/rtl8180_24x.ko
%if %{with smp} && %{with dist_kernel}
install rtl8180_24x-smp.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/rtl8180_24x.ko
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post -n kernel-net-rtl8180
%depmod %{_kernel_ver}

%postun -n kernel-net-rtl8180
%depmod %{_kernel_ver}

%post -n kernel-smp-net-rtl8180
%depmod %{_kernel_ver}smp

%postun -n kernel-smp-net-rtl8180
%depmod %{_kernel_ver}smp

%files -n kernel-net-rtl8180
%defattr(644,root,root,755)
%doc readme
/lib/modules/%{_kernel_ver}/misc/*.ko*

%if %{with smp} && %{with dist_kernel}
%files -n kernel-smp-net-rtl8180
%defattr(644,root,root,755)
%doc readme
/lib/modules/%{_kernel_ver}smp/misc/*.ko*
%endif
