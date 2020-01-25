#
# Conditional build:
%bcond_without	javadoc		# don't build javadoc
%bcond_without	tests		# don't build and run tests

%define		srcname		uddi4j
Summary:	API to interact with a UDDI registry
Name:		java-%{srcname}
Version:	2.0.5
Release:	0.1
License:	IBM Public License
Group:		Libraries/Java
Source0:	http://downloads.sourceforge.net/uddi4j/%{srcname}-src-%{version}.zip
# Source0-md5:	cd358e19acb9b3a4197fce7481c0cce1
URL:		http://uddi4j.sourceforge.net/
%if %(locale -a | grep -q '^en_US$'; echo $?)
BuildRequires:	glibc-localedb-all
%endif
BuildRequires:	java-axis
BuildRequires:	java-xerces
BuildRequires:	jdk
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
BuildRequires:	unzip
Requires:	java-axis
Requires:	java-xerces
Requires:	jpackage-utils
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
UDDI4J is a Java class library that provides an API to interact with a
UDDI (Universal Description, Discovery and Integration) registry. The
UDDI Project is a comprehensive, open industry initiative enabling
businesses to (I) discover each other, and (II) define how they
interact over the internet and share information in a global registry
architecture. UDDI is the building block which will enable businesses
to quickly, easily and dynamically find and transact with one another
via their preferred applications.

%package javadoc
Summary:	Online manual for %{name}
Summary(pl.UTF-8):	Dokumentacja online do %{name}
Group:		Documentation
Requires:	jpackage-utils

%description javadoc
Documentation for %{name}.

%description javadoc -l pl.UTF-8
Dokumentacja do %{name}.

%description javadoc -l fr.UTF-8
Javadoc pour %{name}.

%prep
%setup -q -n %{srcname}
%{__sed} -i -e 's,\r$,,' build.xml README

%build
export LC_ALL=en_US # source code not US-ASCII
%ant %{?with_javadoc:javadocs} \
	-Djavac.executable=%javac \
	-Dapache.axis.location=$(find-jar axis) \
	-Dw3cdom.location=$(find-jar xercesImpl)

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javadir}

# jars
cp -a build/lib/%{srcname}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-%{version}.jar
ln -s %{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}.jar

# javadoc
%if %{with javadoc}
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
cp -a build/javadocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
ln -s %{srcname}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{srcname} # ghost symlink
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{srcname}-%{version} %{_javadocdir}/%{srcname}

%files
%defattr(644,root,root,755)
%{_javadir}/*.jar

%if %{with javadoc}
%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{srcname}-%{version}
%ghost %{_javadocdir}/%{srcname}
%endif
