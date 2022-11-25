Summary:	A statistical, numerical and textual operations tool
Name:		datamash
Version:	1.6
Release:	0.1
License:	GPL v3+
URL:		https://www.gnu.org/software/datamash/
Source0:	http://ftp.gnu.org/gnu/datamash/%{name}-%{version}.tar.gz
BuildRequires:	gcc
BuildRequires:	gettext
BuildRequires:	perl(Digest::MD5)
BuildRequires:	perl(Digest::SHA)
BuildRequires:	perl(Data::Dumper)
BuildRequires:	perl(FileHandle)
BuildRequires:	perl(File::Compare)
BuildRequires:	perl(File::Find)
BuildRequires:	pkgconfig
BuildRequires:	bash-completion
Requires(preun):	info
Requires(post):	info

%description
GNU datamash is a command-line program which performs basic
numeric,textual and statistical operations on input textual data
files.

%prep
%autosetup -p 1
# .UR not defined in el6 an macros
%{?el6:sed -i -e 's/^.UR //g' datamash.1}

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT
%{__rm} -f $RPM_BUILD_ROOT%{_infodir}/dir
%find_lang %{name}
%{__mkdir_p} $RPM_BUILD_ROOT%{compdir}
%{__mv} $RPM_BUILD_ROOT%{_datadir}/datamash/bash-completion.d/datamash $RPM_BUILD_ROOT%{compdir}
# E: non-executable-script %{bash_compdir}/datamash 644 /bin/bash
%{__sed} -i '1d' $RPM_BUILD_ROOT%{compdir}/datamash

%check
%{__make} check

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/install-info %{_infodir}/%{name}.info %{_infodir}/dir || :

%preun
if [ $1 = 0 ];then
/sbin/install-info –delete %{_infodir}/%{name}.info %{_infodir}/dir || :
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README NEWS THANKS TODO AUTHORS ChangeLog
%attr(755,root,root) %{_bindir}/datamash
%{_datadir}/datamash/
%{_infodir}/datamash.info.*
%dir %{compdir}/..
%dir %{compdir}
%{compdir}/datamash
%{_mandir}/man1/datamash.1*
