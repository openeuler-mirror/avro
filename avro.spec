%define HADOOP_VERSION 3.2.1

Name:             avro
Version:          1.10.2
Release:          1
Summary:          Data serialization system
License:          Apache-2.0
URL:              http://avro.apache.org

Source0:          https://github.com/apache/avro/archive/refs/tags/release-1.10.2.tar.gz
# file xmvn-reactor required by mvn_install to specify which jar package should be put in rpm
Source1:          xmvn-reactor

BuildArch:        noarch

BuildRequires:    maven maven-local java-1.8.0-openjdk-devel
Requires:         java-1.8.0-openjdk

%description
Apache Avro is a data serialization system.

Avro provides:

* Rich data structures.
* A compact, fast, binary data format.
* A container file, to store persistent data.
* Remote procedure call (RPC).
* Simple integration with dynamic languages. Code generation is not required
  to read or write data files nor to use or implement RPC protocols. Code
  generation as an optional optimization, only worth implementing for
  statically typed languages.

%prep
%setup -q -n avro-release-1.10.2
cp %{SOURCE1} ./.xmvn-reactor
echo `pwd` > absolute_prefix.log
sed -i 's/\//\\\//g' absolute_prefix.log
absolute_prefix=`head -n 1 absolute_prefix.log`
sed -i 's/absolute-prefix/'"$absolute_prefix"'/g' .xmvn-reactor

%build
for module in avro compiler maven-plugin ipc ipc-jetty ipc-netty tools mapred protobuf thrift archetypes grpc integration-test perf;do
    pushd lang/java/${module}
      mvn package -Dcheckstyle.skip=true -Dmaven.test.skip=true -Dhadoop.version=%{HADOOP_VERSION} -P hadoop2
    popd
done 

pushd lang/java/trevni/avro
    mvn package -Dcheckstyle.skip=true -Dmaven.test.skip=true -Dhadoop.version=%{HADOOP_VERSION} -P hadoop2
popd

pushd lang/java/trevni
    mvn package -Dcheckstyle.skip=true -Dmaven.test.skip=true -Dhadoop.versio=%{HADOOP_VERSION} -P hadoop2
popd

%install
%mvn_install
install -d -m 0755 %{buildroot}%{_datadir}/java/%{name}
install -m 0755 lang/java/tools/target/avro-tools-1.10.2-nodeps.jar %{buildroot}%{_datadir}/java/%{name}/avro-tools-nodeps.jar

%files -f .mfiles
%doc README.md
%license LICENSE.txt NOTICE.txt
%{_datadir}/java/avro/avro-tools-nodeps.jar

%changelog
* Tue Jun 29 2021 Ge Wang <wangge20@huawei.com> - 1.10.2-1
- Init package

