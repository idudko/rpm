%define _name   postgresql96-pg_pathman
%define _pgdir   /usr/pgsql-9.6
%define _bindir  %{_pgdir}/bin
%define _libdir  %{_pgdir}/lib
%define _datadir %{_pgdir}/share/extension
%define _build_timestamp %(date +"%Y%m%d")
%define _config_file /var/lib/pgsql/9.6/data/postgresql.conf
%define debug_package %{nil}

Summary: Module provides optimized partitioning mechanism and functions to manage partitions for PostgreSQL
Name: %{_name}
Version: %{_build_timestamp}
Release: 1%{?dist}
Group: Applications/Databases
License: PostgreSQL
URL: https://github.com/postgrespro/pg_pathman
Source0: %{_name}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: x86_64

Requires: postgresql96-server >= 9.6.2

BuildRequires: flex >= 2.5.37
BuildRequires: bison >= 2.7
BuildRequires: postgresql96-devel >= 9.6.2
BuildRequires: automake, gcc-c++

%description
The pg_pathman module provides optimized partitioning mechanism and functions to manage partitions.
The extension is compatible with PostgreSQL 9.5+.

%prep
%setup -q -n %{name}

%build
PATH=%{_bindir}:$PATH make USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

PATH=%{_bindir}:$PATH make USE_PGXS=1 %{?_smp_mflags} install

%{__install} -d %{buildroot}%{_libdir}
%{__install} -d %{buildroot}%{_datadir}
%{__strip} pg_pathman.so
%{__install} -m 755 pg_pathman.so %{buildroot}%{_libdir}/pg_pathman.so
%{__install} -m 644 pg_pathman.control %{buildroot}%{_datadir}/pg_pathman.control
%{__install} -m 644 pg_pathman--1.0--1.1.sql %{buildroot}%{_datadir}/pg_pathman--1.0--1.1.sql
%{__install} -m 644 pg_pathman--1.1--1.2.sql %{buildroot}%{_datadir}/pg_pathman--1.1--1.2.sql
%{__install} -m 644 pg_pathman--1.2--1.3.sql %{buildroot}%{_datadir}/pg_pathman--1.2--1.3.sql
%{__install} -m 644 pg_pathman--1.3.sql %{buildroot}%{_datadir}/pg_pathman--1.3.sql

%clean
%{__rm} -rf %{buildroot}
%{__rm} -rf %{_libdir}/pg_pathman.so
%{__rm} -rf %{_datadir}/pg_pathman.control
%{__rm} -rf %{_datadir}/pg_pathman--1.0--1.1.sql
%{__rm} -rf %{_datadir}/pg_pathman--1.1--1.2.sql
%{__rm} -rf %{_datadir}/pg_pathman--1.2--1.3.sql
%{__rm} -rf %{_datadir}/pg_pathman--1.3.sql

%post
if [ -f "%{_config_file}" ]
then
    sed -i -e 's/^#shared_preload_libraries = '\'''\''/shared_preload_libraries = '\''pg_pathman'\''/' %{_config_file}
fi

%postun
if [ -f "%{_config_file}" ]
then
    sed -i -e 's/^shared_preload_libraries = '\''pg_pathman'\''/#shared_preload_libraries = '\'''\''/' %{_config_file}
fi

%files
%attr(755, root, root)%{_libdir}/pg_pathman.so
%attr(644, root, root)%{_datadir}/pg_pathman.control
%attr(644, root, root)%{_datadir}/pg_pathman--1.0--1.1.sql
%attr(644, root, root)%{_datadir}/pg_pathman--1.1--1.2.sql
%attr(644, root, root)%{_datadir}/pg_pathman--1.2--1.3.sql
%attr(644, root, root)%{_datadir}/pg_pathman--1.3.sql

%changelog
* Tue Apr 4 2017 Maksim Milyutin <milyutinma@gmail.com>
- Add first regression test on join clause
* Tue Apr 4 2017 Dmitry Ivanov <funbringer@gmail.com>
- bugfix: copy parent's joininfo to child RelOptInfo
