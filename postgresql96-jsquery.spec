%define _name   postgresql96-jsquery
%define _pgdir   /usr/pgsql-9.6
%define _bindir  %{_pgdir}/bin
%define _libdir  %{_pgdir}/lib
%define _datadir %{_pgdir}/share/extension
%define _incdir %{_pgdir}/include/server
%define _build_timestamp %(date +"%Y%m%d")
%define debug_package %{nil}

Summary: Language to query jsonb data type for PostgreSQL
Name: %{_name}
Version: %{_build_timestamp}
Release: 1%{?dist}
Group: Applications/Databases
License: PostgreSQL
URL: https://github.com/postgrespro/jsquery
Source0: %{_name}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: x86_64

Requires: postgresql96-server >= 9.6.2

BuildRequires: flex >= 2.5.37
BuildRequires: bison >= 2.7
BuildRequires: postgresql96-devel >= 9.6.2
BuildRequires: automake, gcc-c++

%description
JsQuery – is a language to query jsonb data type, introduced in PostgreSQL release 9.4.
It's primary goal is to provide an additional functionality to jsonb (currently missing 
in PostgreSQL), such as a simple and effective way to search in nested objects and arrays, 
more comparison operators with indexes support. We hope, that jsquery will be eventually 
a part of PostgreSQL. Jsquery is released as jsquery data type (similar to tsquery) 
and @@ match operator for jsonb.

%prep
%setup -q -n %{name}

%build
PATH=%{_bindir}:$PATH make USE_PGXS=1 %{?_smp_mflags}

%install
rm -rf %{buildroot}

PATH=%{_bindir}:$PATH make USE_PGXS=1 %{?_smp_mflags} install

%{__install} -d %{buildroot}%{_libdir}
%{__install} -d %{buildroot}%{_datadir}
%{__install} -d %{buildroot}%{_incdir}
%{__strip} jsquery.so
%{__install} -m 755 jsquery.so %{buildroot}%{_libdir}/jsquery.so
%{__install} -m 644 jsquery.h %{buildroot}%{_incdir}/jsquery.h
%{__install} -m 644 jsquery.control %{buildroot}%{_datadir}/jsquery.control
%{__install} -m 644 jsquery--1.0.sql %{buildroot}%{_datadir}/jsquery--1.0.sql

%clean
%{__rm} -rf %{buildroot}
%{__rm} -rf %{_libdir}/jsquery.so
%{__rm} -rf %{_incdir}/jsquery.h
%{__rm} -rf %{_datadir}/jsquery.control
%{__rm} -rf %{_datadir}/jsquery--1.0.sql

%files
%attr(755, root, root)%{_libdir}/jsquery.so
%attr(644, root, root)%{_incdir}/jsquery.h
%attr(644, root, root)%{_datadir}/jsquery.control
%attr(644, root, root)%{_datadir}/jsquery--1.0.sql

%changelog
* Thu Mar 2 2017 Alexander Korotkov <aekorotkov@gmail.com>
- Use correct variable for path to server includes
* Mon Feb 20 2017 Alexander Korotkov <aekorotkov@gmail.com>
- Install includes to include/server
- Install jsquery.h
- Fix jqiIndexArray handling in GIN
- Add .deps to .gitignore
