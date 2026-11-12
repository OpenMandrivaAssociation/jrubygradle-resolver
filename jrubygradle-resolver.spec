Name:		jrubygradle-resolver
Version:	3.0.0
Release:	1
Summary:	JRuby GEM resolver for Gradle
Group:		Development/Java
License:	MPL-2.0
URL:		https://gitlab.com/ysb33rOrg/gradle/simplified-jruby-gradle-plugin
# Tag RELEASE_3_0_0, resolver-plugin only. Compiled with Groovy's
# FileSystemCompiler. The Gradle tool is not invoked.
# Patch0 is the Groovy 4 static type check: RegisteredGemConfiguration
# bounds T by AbstractGemPrepareTask, and ListProperty/MapProperty
# conventions take typed empty collections. Groovy 3 accepted the
# original sources.
Source0:	jrubygradle-resolver-%{version}.tar.gz
Patch0:		jrubygradle-resolver-groovy4-stc.patch

BuildArch:	noarch
BuildRequires:	java-current-devel
BuildRequires:	apache-groovy
BuildRequires:	antlr4
BuildRequires:	objectweb-asm
BuildRequires:	picocli
BuildRequires:	jansi
BuildRequires:	ant-lib
BuildRequires:	slf4j2
BuildRequires:	gradle
BuildRequires:	jruby
BuildRequires:	sysjar
BuildRequires:	javapackages-filesystem
BuildRequires:	mvn(org.ysb33r.gradle:grolifant5-core)
BuildRequires:	mvn(org.ysb33r.gradle:grolifant5-herd)
BuildRequires:	mvn(org.ysb33r.gradle:grolifant5-rawhide)
BuildRequires:	mvn(com.squareup.okhttp3:okhttp)
BuildRequires:	mvn(com.squareup.okio:okio)
BuildRequires:	mvn(io.ratpack:ratpack-base)
BuildRequires:	mvn(io.ratpack:ratpack-exec)
BuildRequires:	mvn(io.ratpack:ratpack-core)
BuildRequires:	mvn(org.slf4j:slf4j-api)
BuildRequires:	mvn(com.google.guava:guava)
BuildRequires:	mvn(org.reactivestreams:reactive-streams)
BuildRequires:	mvn(org.jctools:jctools-core)
BuildRequires:	mvn(javax.inject:javax.inject)
BuildRequires:	mvn(com.google.code.findbugs:jsr305)
BuildRequires:	mvn(com.fasterxml.jackson.core:jackson-annotations)
BuildRequires:	mvn(com.fasterxml.jackson.core:jackson-core)
BuildRequires:	mvn(com.fasterxml.jackson.core:jackson-databind)
BuildRequires:	mvn(com.fasterxml.jackson.dataformat:jackson-dataformat-yaml)
BuildRequires:	mvn(com.fasterxml.jackson.datatype:jackson-datatype-guava)
BuildRequires:	mvn(com.fasterxml.jackson.datatype:jackson-datatype-jdk8)
BuildRequires:	mvn(com.fasterxml.jackson.datatype:jackson-datatype-jsr310)
BuildRequires:	mvn(com.github.ben-manes.caffeine:caffeine)
BuildRequires:	mvn(org.yaml:snakeyaml)
BuildRequires:	mvn(io.netty:netty-buffer)
BuildRequires:	mvn(io.netty:netty-codec)
BuildRequires:	mvn(io.netty:netty-codec-dns)
BuildRequires:	mvn(io.netty:netty-codec-http)
BuildRequires:	mvn(io.netty:netty-codec-socks)
BuildRequires:	mvn(io.netty:netty-common)
BuildRequires:	mvn(io.netty:netty-handler)
BuildRequires:	mvn(io.netty:netty-handler-proxy)
BuildRequires:	mvn(io.netty:netty-resolver)
BuildRequires:	mvn(io.netty:netty-resolver-dns)
BuildRequires:	mvn(io.netty:netty-transport)
BuildRequires:	mvn(io.netty:netty-transport-native-unix-common)
Requires:	apache-groovy
Requires:	gradle

%description
org.ysb33r.gradle.jruby:jrubygradle-resolver %{version}, the
org.ysb33r.jruby.resolver Gradle plugin. GemVersion translates the
Ruby pessimistic requirement "~> 1.2.3" into the Ivy range
[1.2.3,1.3.0[ and PluginMetadata.version() reports %{version}.
The sources are compiled with FileSystemCompiler at bytecode 8.
The Gradle tool is not invoked.

%prep
%autosetup -n jrubygradle-resolver-%{version} -p1
find . -type f \( -name '*.jar' -o -name '*.class' -o -name '*.so' -o -name '*.node' -o -name '*.wasm' \) -print > binaries.list
find . -type d -name '*.jar' -print >> binaries.list
if [ -s binaries.list ]; then
	cat binaries.list
	exit 1
fi
props=resolver-plugin/src/main/resources/META-INF/org.ysb33r.gradle.jruby.version.properties
sed -i \
	-e 's/${VERSION}/%{version}/' \
	-e 's/${MIN_GRADLE}/7.3.3/' \
	-e 's/${JRUBY_VERSION}/9.4.15.0/' \
	"$props"
grep -F -q 'version=%{version}' "$props"
grep -F -q 'mingradle=7.3.3' "$props"
grep -F -q 'jrubyversion=9.4.15.0' "$props"
if grep -F '${VERSION}' "$props"; then
	exit 1
fi
find resolver-plugin/src/main -type f \( -name '*.groovy' -o -name '*.java' \) | sort > sources.list
test "$(wc -l < sources.list)" -eq 58
test "$(grep -c '\.java$' sources.list)" -eq 15
test "$(grep -c '\.groovy$' sources.list)" -eq 43
grep -F -q 'T extends AbstractGemPrepareTask' resolver-plugin/src/main/groovy/org/ysb33r/gradle/jruby/api/gems/GemConfigurations.groovy
grep -F -q 'Collections.<String>emptyList()' resolver-plugin/src/main/groovy/org/ysb33r/gradle/jruby/api/core/JRubyExecSpec.groovy

%build
set -eo pipefail
export JAVA_HOME=%{_jvmdir}/java-openjdk
export PATH="$JAVA_HOME/bin:/usr/bin:/bin"
tool_cp=%{_javadir}/apache-groovy.jar
for extra in \
	%{_javadir}/apache-groovy-xml.jar \
	%{_javadir}/apache-groovy-json.jar \
	%{_javadir}/apache-groovy-templates.jar \
	%{_javadir}/antlr4-runtime.jar \
	%{_javadir}/asm.jar \
	%{_javadir}/asm-commons.jar \
	%{_javadir}/asm-tree.jar \
	%{_javadir}/asm-util.jar \
	%{_javadir}/asm-analysis.jar \
	%{_javadir}/picocli.jar \
	/usr/lib/java/jansi/jansi.jar \
	%{_javadir}/ant.jar
do
	test -s "$extra"
	tool_cp=$tool_cp:$extra
done
src_cp=%{_javadir}/jruby.jar
for extra in \
	%{_javadir}/grolifant5-core.jar \
	%{_javadir}/grolifant5-herd.jar \
	%{_javadir}/grolifant5-rawhide.jar \
	%{_javadir}/ratpack-base.jar \
	%{_javadir}/ratpack-exec.jar \
	%{_javadir}/ratpack-core.jar \
	%{_javadir}/okhttp.jar \
	%{_javadir}/okio.jar \
	%{_javadir}/slf4j-api.jar \
	%{_javadir}/guava.jar \
	%{_javadir}/reactive-streams.jar \
	%{_javadir}/jctools-core.jar \
	%{_javadir}/atinject.jar \
	%{_javadir}/javax.annotation.jar \
	%{_javadir}/apache-groovy.jar \
	%{_javadir}/apache-groovy-xml.jar \
	%{_javadir}/apache-groovy-json.jar \
	%{_javadir}/jackson-databind.jar \
	%{_javadir}/jackson-core.jar \
	%{_javadir}/jackson-annotations.jar \
	%{_javadir}/jackson-datatype-guava.jar \
	%{_javadir}/jackson-datatype-jdk8.jar \
	%{_javadir}/jackson-datatype-jsr310.jar \
	%{_javadir}/jackson-dataformat-yaml.jar \
	%{_javadir}/snakeyaml.jar \
	%{_javadir}/caffeine.jar
do
	test -s "$extra"
	src_cp=$src_cp:$extra
done
for j in %{_javadir}/netty-*.jar %{_datadir}/gradle/lib/*.jar %{_datadir}/gradle/lib/plugins/*.jar %{_datadir}/gradle/lib/agents/*.jar; do
	test -s "$j"
	src_cp=$src_cp:$j
done
mkdir -p classes
java -Dgroovy.target.bytecode=1.8 -cp "$tool_cp" org.codehaus.groovy.tools.FileSystemCompiler \
	--classpath "$src_cp" -j '-J-release=8' -d classes @sources.list
/bin/cp -a resolver-plugin/src/main/resources/. classes/
mkdir -p classes/META-INF/gradle-plugins
printf '%s\n' 'implementation-class=org.ysb33r.gradle.jruby.api.plugins.JRubyResolverPlugin' \
	> classes/META-INF/gradle-plugins/org.ysb33r.jruby.resolver.properties
test "$(find classes -name '*.class' | wc -l)" -eq 191
javap -v -classpath classes org.ysb33r.gradle.jruby.api.gems.GemVersion | grep -F -q 'major version: 52'
javap -v -classpath classes org.ysb33r.gradle.jruby.api.gems.RegisteredGemConfiguration | grep -F -q 'major version: 52'
javap -v -classpath classes org.ysb33r.gradle.jruby.internal.core.PluginMetadata | grep -F -q 'major version: 52'
grep -F -q 'version=%{version}' classes/META-INF/org.ysb33r.gradle.jruby.version.properties
printf '%s\n' 'Manifest-Version: 1.0' 'Automatic-Module-Name: org.ysb33r.gradle.jruby' > resolver.mf
jar cfm jrubygradle-resolver.jar resolver.mf -C classes .
jar i jrubygradle-resolver.jar
jar tf jrubygradle-resolver.jar | grep -F -q 'org/ysb33r/gradle/jruby/api/gems/GemVersion.class'
jar tf jrubygradle-resolver.jar | grep -F -q 'META-INF/gradle-plugins/org.ysb33r.jruby.resolver.properties'
jar tf jrubygradle-resolver.jar | grep -F -q 'META-INF/org.ysb33r.gradle.jruby.version.properties'
desc=$(jar --describe-module --file jrubygradle-resolver.jar)
printf '%s\n' "$desc" | grep -F -qx 'org.ysb33r.gradle.jruby automatic'
if printf '%s\n' "$desc" | grep -F -q 'Unable'; then
	printf '%s\n' "$desc"
	exit 1
fi

cat > jrubygradle-resolver.pom << 'END'
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>
  <groupId>org.ysb33r.gradle.jruby</groupId>
  <artifactId>jrubygradle-resolver</artifactId>
  <version>%{version}</version>
  <name>jrubygradle-resolver</name>
  <description>Resolve RubyGems for the JRuby Gradle plugin.</description>
  <url>https://gitlab.com/ysb33rOrg/gradle/simplified-jruby-gradle-plugin</url>
  <licenses>
    <license>
      <name>MPL-2.0</name>
      <url>https://www.mozilla.org/MPL/2.0/</url>
    </license>
  </licenses>
  <dependencies>
    <dependency>
      <groupId>org.ysb33r.gradle</groupId>
      <artifactId>grolifant5-core</artifactId>
      <version>5.12.7</version>
    </dependency>
    <dependency>
      <groupId>org.ysb33r.gradle</groupId>
      <artifactId>grolifant5-herd</artifactId>
      <version>5.12.7</version>
    </dependency>
    <dependency>
      <groupId>org.ysb33r.gradle</groupId>
      <artifactId>grolifant5-rawhide</artifactId>
      <version>5.12.7</version>
    </dependency>
    <dependency>
      <groupId>com.squareup.okhttp3</groupId>
      <artifactId>okhttp</artifactId>
      <version>4.12.0</version>
    </dependency>
    <dependency>
      <groupId>io.ratpack</groupId>
      <artifactId>ratpack-core</artifactId>
      <version>1.9.0</version>
    </dependency>
    <dependency>
      <groupId>io.github.rburgst</groupId>
      <artifactId>okhttp-digest</artifactId>
      <version>3.1.1</version>
    </dependency>
  </dependencies>
</project>
END

cat > jruby-resolver-gradle-plugin.pom << 'END'
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>
  <groupId>org.ysb33r.jruby.resolver</groupId>
  <artifactId>org.ysb33r.jruby.resolver.gradle.plugin</artifactId>
  <version>%{version}</version>
  <packaging>pom</packaging>
  <name>org.ysb33r.jruby.resolver.gradle.plugin</name>
  <description>Gradle plugin marker for org.ysb33r.jruby.resolver.</description>
  <url>https://gitlab.com/ysb33rOrg/gradle/simplified-jruby-gradle-plugin</url>
  <licenses>
    <license>
      <name>MPL-2.0</name>
      <url>https://www.mozilla.org/MPL/2.0/</url>
    </license>
  </licenses>
  <dependencies>
    <dependency>
      <groupId>org.ysb33r.gradle.jruby</groupId>
      <artifactId>jrubygradle-resolver</artifactId>
      <version>%{version}</version>
    </dependency>
  </dependencies>
</project>
END

%install
set -eo pipefail
sysjar install --buildroot %{buildroot} \
	--artifact jrubygradle-resolver.pom:jrubygradle-resolver.jar \
	--file-name jrubygradle-resolver \
	--filelist .mfiles-resolver
sysjar install --buildroot %{buildroot} \
	--artifact jruby-resolver-gradle-plugin.pom \
	--file-name org.ysb33r.jruby.resolver.gradle.plugin \
	--filelist .mfiles-marker
awk '!seen[$0]++' .mfiles-resolver .mfiles-marker > .mfiles
idx="%{buildroot}/usr/share/sysjar/index/org.ysb33r.gradle.jruby/jrubygradle-resolver.sysjar"
test -s "$idx"
grep -F -q '"version": "%{version}"' "$idx"
grep -F -q '"artifactId": "jrubygradle-resolver"' "$idx"
marker="%{buildroot}/usr/share/sysjar/index/org.ysb33r.jruby.resolver/org.ysb33r.jruby.resolver.gradle.plugin@pom.sysjar"
test -s "$marker"
grep -F -q '"version": "%{version}"' "$marker"
grep -F -q '"artifactId": "org.ysb33r.jruby.resolver.gradle.plugin"' "$marker"
test -s %{buildroot}%{_javadir}/jrubygradle-resolver.jar

%check
set -eo pipefail
export JAVA_HOME=%{_jvmdir}/java-openjdk
export PATH="$JAVA_HOME/bin:/usr/bin:/bin"
JAR=%{buildroot}%{_javadir}/jrubygradle-resolver.jar
test -s "$JAR"
mkdir -p check
cat > check/JRubyResolverCheck.java << 'END'
import org.ysb33r.gradle.jruby.api.gems.GemVersion;
import org.ysb33r.gradle.jruby.internal.core.PluginMetadata;

public class JRubyResolverCheck {
    public static void main(String[] args) {
        GemVersion pessimistic = GemVersion.gemVersionFromGemRequirement("~> 1.2.3");
        String ivy = pessimistic.toString();
        if (!"[1.2.3,1.3.0[".equals(ivy)) {
            throw new AssertionError(ivy);
        }
        String version = PluginMetadata.version();
        if (!"%{version}".equals(version)) {
            throw new AssertionError(version);
        }
        System.out.println("jrubygradle_resolver_ok " + version + " " + ivy);
    }
}
END
CP="$JAR:%{_javadir}/apache-groovy.jar:%{_javadir}/slf4j-api.jar:%{_javadir}/asm.jar:%{_javadir}/asm-commons.jar:%{_javadir}/asm-tree.jar:%{_javadir}/asm-util.jar:%{_javadir}/asm-analysis.jar"
javac --release 8 -encoding UTF-8 -Xlint:-options -cp "$CP" -d check check/JRubyResolverCheck.java
java -cp "check:$CP" JRubyResolverCheck > check/out.txt
cat check/out.txt
grep -F -qx 'jrubygradle_resolver_ok %{version} [1.2.3,1.3.0[' check/out.txt

%files -f .mfiles
%license LICENSE
%doc README.adoc CHANGELOG.adoc
