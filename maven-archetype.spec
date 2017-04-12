%{?scl:%scl_package maven-archetype}
%{!?scl:%global pkg_name %{name}}
%{?java_common_find_provides_and_requires}

%global baserelease 3

Name:           %{?scl_prefix}maven-archetype
Version:        2.4
Release:        3.%{baserelease}%{?dist}
Summary:        Maven project templating toolkit

License:        ASL 2.0
URL:            https://maven.apache.org/archetype/
Source0:        http://repo.maven.apache.org/maven2/org/apache/maven/archetype/%{pkg_name}/%{version}/%{pkg_name}-%{version}-source-release.zip

Patch1:         0001-Add-Maven-3-compatibility.patch
Patch2:         0002-Fix-jetty-namespace.patch
Patch3:         0003-Port-to-current-plexus-utils.patch

BuildArch:      noarch

BuildRequires:  %{?scl_prefix}maven-local
BuildRequires:  %{?scl_prefix_java_common}mvn(commons-collections:commons-collections)
BuildRequires:  %{?scl_prefix_java_common}mvn(commons-io:commons-io)
BuildRequires:  %{?scl_prefix_java_common}mvn(dom4j:dom4j)
BuildRequires:  %{?scl_prefix_java_common}mvn(jdom:jdom)
BuildRequires:  %{?scl_prefix_java_common}mvn(junit:junit)
BuildRequires:  %{?scl_prefix}mvn(net.sourceforge.jchardet:jchardet)
BuildRequires:  %{?scl_prefix}mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven:maven-compat)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven:maven-core)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven:maven-model)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven:maven-parent:pom:)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven:maven-plugin-api)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven:maven-project)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven.plugins:maven-dependency-plugin)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven.plugins:maven-plugin-plugin)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven.shared:maven-invoker)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven.shared:maven-plugin-testing-harness)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven.shared:maven-script-interpreter)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven.wagon:wagon-file)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven.wagon:wagon-http)
BuildRequires:  %{?scl_prefix}mvn(org.apache.rat:apache-rat-plugin)
BuildRequires:  %{?scl_prefix}mvn(org.apache.velocity:velocity)
BuildRequires:  %{?scl_prefix}mvn(org.beanshell:bsh)
BuildRequires:  %{?scl_prefix}mvn(org.codehaus.modello:modello-maven-plugin)
BuildRequires:  %{?scl_prefix}mvn(org.codehaus.plexus:plexus-component-annotations)
BuildRequires:  %{?scl_prefix}mvn(org.codehaus.plexus:plexus-component-metadata)
BuildRequires:  %{?scl_prefix}mvn(org.codehaus.plexus:plexus-container-default)
BuildRequires:  %{?scl_prefix}mvn(org.codehaus.plexus:plexus-interactivity-api)
BuildRequires:  %{?scl_prefix}mvn(org.codehaus.plexus:plexus-utils)
BuildRequires:  %{?scl_prefix}mvn(org.codehaus.plexus:plexus-velocity)

%description
Archetype is a Maven project templating toolkit. An archetype is
defined as an original pattern or model from which all other things of
the same kind are made. The names fits as we are trying to provide a
system that provides a consistent means of generating Maven
projects. Archetype will help authors create Maven project templates
for users, and provides users with the means to generate parameterized
versions of those project templates.

Using archetypes provides a great way to enable developers quickly in
a way consistent with best practices employed by your project or
organization. Within the Maven project we use archetypes to try and
get our users up and running as quickly as possible by providing a
sample project that demonstrates many of the features of Maven while
introducing new users to the best practices employed by Maven. In a
matter of seconds a new user can have a working Maven project to use
as a jumping board for investigating more of the features in Maven. We
have also tried to make the Archetype mechanism additive and by that
we mean allowing portions of a project to be captured in an archetype
so that pieces or aspects of a project can be added to existing
projects. A good example of this is the Maven site archetype. If, for
example, you have used the quick start archetype to generate a working
project you can then quickly create a site for that project by using
the site archetype within that existing project. You can do anything
like this with archetypes.

You may want to standardize J2EE development within your organization
so you may want to provide archetypes for EJBs, or WARs, or for your
web services. Once these archetypes are created and deployed in your
organization's repository they are available for use by all developers
within your organization.

%package javadoc
Summary:        API documentation for %{pkg_name}

%description    javadoc
%{summary}.

%package catalog
Summary:        Maven Archetype Catalog model

%description catalog
%{summary}.

%package descriptor
Summary:        Maven Archetype Descriptor model

%description descriptor
%{summary}.

%package registry
Summary:        Maven Archetype Registry model

%description registry
%{summary}.

%package common
Summary:        Maven Archetype common classes

%description common
%{summary}.

%package packaging
Summary:        Maven Archetype packaging configuration for archetypes

%description packaging
%{summary}.

%package -n %{?scl_prefix}%{pkg_name}-plugin
Summary:        Maven Plugin for using archetypes

%description -n %{?scl_prefix}%{pkg_name}-plugin
%{summary}.

%prep
%{?scl:scl enable %{scl} %{scl} - << "EOF"}
set -e -x
%setup -n %{pkg_name}-%{version} -q

%patch1 -p1
%patch2 -p1
%patch3 -p1

# Add OSGI info to catalog and descriptor jars
pushd archetype-models/archetype-catalog
    %pom_xpath_remove "pom:project/pom:packaging"
    %pom_xpath_inject "pom:project" "<packaging>bundle</packaging>"
    %pom_xpath_inject "pom:build/pom:plugins" "
      <plugin>
        <groupId>org.apache.felix</groupId>
        <artifactId>maven-bundle-plugin</artifactId>
        <extensions>true</extensions>
        <configuration>
          <instructions>
            <_nouses>true</_nouses>
            <Export-Package>org.apache.maven.archetype.catalog.*</Export-Package>
          </instructions>
        </configuration>
      </plugin>"
popd
pushd archetype-models/archetype-descriptor
    %pom_xpath_remove "pom:project/pom:packaging"
    %pom_xpath_inject "pom:project" "<packaging>bundle</packaging>"
    %pom_xpath_inject "pom:build/pom:plugins" "
      <plugin>
        <groupId>org.apache.felix</groupId>
        <artifactId>maven-bundle-plugin</artifactId>
        <extensions>true</extensions>
        <configuration>
          <instructions>
            <_nouses>true</_nouses>
            <Export-Package>org.apache.maven.archetype.metadata.*</Export-Package>
          </instructions>
        </configuration>
      </plugin>"
popd


# groovy is not really needed
%pom_remove_dep org.codehaus.groovy:groovy maven-archetype-plugin/pom.xml

%pom_disable_module archetype-testing
%pom_remove_plugin org.apache.maven.plugins:maven-antrun-plugin archetype-common/pom.xml
%{?scl:EOF}


%build
%{?scl:scl enable %{scl} %{scl} - << "EOF"}
set -e -x
%mvn_package :archetype-models maven-archetype
# we don't have cargo so skip tests for now
%mvn_build -s -f
%{?scl:EOF}


%install
%{?scl:scl enable %{scl} %{scl} - << "EOF"}
set -e -x
%mvn_install
%{?scl:EOF}


%files -f .mfiles-maven-archetype
%doc LICENSE NOTICE
%dir %{_mavenpomdir}/%{pkg_name}

%files catalog -f .mfiles-archetype-catalog
%dir %{_javadir}/%{pkg_name}
%dir %{_mavenpomdir}/%{pkg_name}

%files descriptor -f .mfiles-archetype-descriptor
%dir %{_javadir}/%{pkg_name}
%dir %{_mavenpomdir}/%{pkg_name}

%files registry -f .mfiles-archetype-registry
%dir %{_javadir}/%{pkg_name}
%dir %{_mavenpomdir}/%{pkg_name}

%files common -f .mfiles-archetype-common
%dir %{_javadir}/%{pkg_name}
%dir %{_mavenpomdir}/%{pkg_name}

%files packaging -f .mfiles-archetype-packaging
%dir %{_javadir}/%{pkg_name}
%dir %{_mavenpomdir}/%{pkg_name}

%files -n %{?scl_prefix}%{pkg_name}-plugin -f .mfiles-maven-archetype-plugin
%dir %{_javadir}/%{pkg_name}
%dir %{_mavenpomdir}/%{pkg_name}

%files javadoc -f .mfiles-javadoc
%doc LICENSE

%changelog
* Tue Feb 07 2017 Michael Simacek <msimacek@redhat.com> - 2.4-3.3
- Fix directory ownership
- Resolves rhbz#1418384

* Fri Jan 20 2017 Michael Simacek <msimacek@redhat.com> - 2.4-3.2
- Build for rh-maven33

* Fri Jan 20 2017 Mat Booth <mat.booth@redhat.com> - 2.4-3.1
- Auto SCL-ise package for rh-eclipse46 collection

* Thu Jun 02 2016 Michael Simacek <msimacek@redhat.com> - 2.4-3
- Port to current plexus-utils

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 24 2015 Michael Simacek <msimacek@redhat.com> - 2.4-1
- Update to upstream version 2.4
- Remove Group tags

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Mar 13 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3-1
- Update to upstream version 2.3

* Mon Jun  9 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2-5
- Regenerate build-requires
- Resolves: rhbz#1106161

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2-4
- Use Requires: java-headless rebuild (#1067528)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 2.2-2
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Fri Feb 01 2013 Michal Srb <msrb@redhat.com> - 2.2-1
- Update to upstream version 2.2
- Build with xmvn
- Remove unnecessary depmap and patch

* Thu Aug 09 2012 Gerard Ryan <galileo@fedoraproject.org> - 2.1-7
- Add OSGI info to descriptor.jar

* Tue Aug  7 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.1-6
- Export only proper OSGI packages
- Do not generate "uses" OSGI clauses

* Mon Aug 06 2012 Gerard Ryan <galileo@fedoraproject.org> - 2.1-5
- Fix jetty namespace
- Add OSGI info to catalog.jar

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Sep 20 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.1-2
- Add depmap explanation
- Omit javadoc.sh from javadocs
- Add explicit maven NVR that is needed

* Wed Sep 14 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.1-1
- Initial version of the package
