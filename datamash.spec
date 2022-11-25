#
# Conditional build:
%bcond_without	tests	# don't run tests

Summary:	A statistical, numerical and textual operations tool
Name:		datamash
Version:	1.8
Release:	1
License:	GPL v3+
Group:		Applications
Source0:	http://ftp.gnu.org/gnu/datamash/%{name}-%{version}.tar.gz
# Source0-md5:	b5f2dcfcefb2d41f88c54619b08727e3
URL:		https://www.gnu.org/software/datamash/
BuildRequires:	gettext-tools
BuildRequires:	pkgconfig
%if %{with tests}
BuildRequires:	perl-base
BuildRequires:	perl-modules
BuildRequires:	rpm-build >= 4.6
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GNU datamash is a command-line program which performs basic numeric,
textual and statistical operations on input textual data files.

%package -n bash-completion-datamash
Summary:	Bash completion for datamash command line
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	bash-completion >= 1:2.0
BuildArch:	noarch

%description -n bash-completion-datamash
Bash completion for datamash command line.

%prep
%setup -q

%build
%configure \
	--with-bash-completion-dir="%{bash_compdir}"

%{__make}

%{?with_tests:%{__make} check}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{bash_compdir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -f $RPM_BUILD_ROOT%{_infodir}/dir

%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/%{name}/examples

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun	-p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README THANKS examples
%attr(755,root,root) %{_bindir}/datamash
%attr(755,root,root) %{_bindir}/decorate
%{_infodir}/datamash.info*
%{_mandir}/man1/datamash.1*
%{_mandir}/man1/decorate.1*

%files -n bash-completion-datamash
%defattr(644,root,root,755)
%{bash_compdir}/datamash
