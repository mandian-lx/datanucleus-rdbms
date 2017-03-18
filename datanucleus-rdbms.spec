%{?_javapackages_macros:%_javapackages_macros}

%global commit 9bd33de81ccdce1c1c448cdd3c0aa8d9480eff9a
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:          datanucleus-rdbms
Version:       3.2.13
Release:       5
Summary:       DataNucleus RDBMS
License:       ASL 2.0
URL:           http://www.datanucleus.org/%{name}
Source:        https://github.com/datanucleus/%{name}/archive/%{commit}/%{name}-%{commit}.tar.gz

BuildRequires: java-devel
BuildRequires: mvn(com.mchange:c3p0)
BuildRequires: mvn(commons-collections:commons-collections)
BuildRequires: mvn(commons-dbcp:commons-dbcp)
BuildRequires: mvn(commons-pool:commons-pool)
BuildRequires: mvn(javax.time:time-api)
BuildRequires: mvn(javax.transaction:jta)
BuildRequires: mvn(org.datanucleus:datanucleus-core)
BuildRequires: mvn(proxool:proxool)
BuildRequires: mvn(org.apache.tomcat:tomcat-jdbc)
# Test deps
BuildRequires: mvn(junit:junit)
BuildRequires: mvn(log4j:log4j)

BuildRequires: maven-local
BuildRequires: maven-install-plugin
BuildRequires: datanucleus-maven-parent

# fix for broken proxool metadata
BuildRequires: mvn(net.sf.cglib:cglib)

BuildArch:     noarch

%description
Plugin for DataNucleus providing persistence to RDBMS data-stores.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n %{name}-%{commit}

# Fix c3p0 gId
%pom_xpath_set "pom:project/pom:dependencies/pom:dependency[pom:artifactId = 'c3p0' ]/pom:groupId" com.mchange

# Non free
%pom_remove_dep oracle:ojdbc14_g
%pom_remove_dep oracle:xdb
%pom_remove_dep oracle:xmlparser
rm -r src/java/org/datanucleus/store/rdbms/mapping/oracle/Oracle*.java \
 src/java/org/datanucleus/store/rdbms/mapping/oracle/XMLTypeRDBMSMapping.java \
 src/java/org/datanucleus/store/rdbms/adapter/OracleAdapter.java

# Unavailable dep
%pom_remove_dep com.jolbox:bonecp
rm -r src/java/org/datanucleus/store/rdbms/connectionpool/BoneCP*.java
# Required by bonecp
%pom_remove_dep org.slf4j:slf4j-api
%pom_remove_dep org.slf4j:slf4j-log4j12

%pom_xpath_inject "pom:project/pom:build/pom:plugins/pom:plugin[pom:artifactId = 'maven-bundle-plugin' ]/pom:configuration/pom:instructions" '
<Require-Bundle>org.datanucleus;bundle-version="${project.version}"</Require-Bundle>
<Bundle-Name>${project.name}</Bundle-Name>
<Bundle-Vendor>DataNucleus</Bundle-Vendor>'
%pom_xpath_inject "pom:project/pom:build/pom:plugins/pom:plugin[pom:artifactId = 'maven-bundle-plugin' ]" "
<executions>
  <execution>
    <id>bundle-manifest</id>
    <phase>process-classes</phase>
    <goals>
      <goal>manifest</goal>
    </goals>
  </execution>
</executions>"

sed -i 's/\r//' META-INF/LICENSE.txt META-INF/NOTICE.txt META-INF/README.txt
cp -p META-INF/LICENSE.txt .
cp -p META-INF/NOTICE.txt .
cp -p META-INF/README.txt .

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc LICENSE.txt NOTICE.txt README.txt

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt NOTICE.txt

%changelog
* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.13-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jul 06 2015 Peter MacKinnon <pmackinn@redhat.com> 3.2.13-3
- workaround broken proxool metadata

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 19 2014 Peter MacKinnon <pmackinn@redhat.com> 3.2.13-1
- updated to 3.2.13
- updated to xmvn 2.0
- remove tomcat-jdbc system scope dep
- remove oss-parent

* Mon Jun 09 2014 Peter MacKinnon <pmackinn@redhat.com> 3.2.9-3
- removed wagon-ssh-external dependency

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Dec 10 2013 Peter MacKinnon <pmackinn@redhat.com> 3.2.9-1
- updated to version 3.2.9
- switched to manual xmvn build and install

* Fri Sep 20 2013 gil cattaneo <puntogil@libero.it> 3.2.6-1
- initial rpm
