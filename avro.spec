%define HADOOP_VERSION 3.2.1

Name:             avro
Version:          1.10.2
Release:          2
Summary:          Data serialization system
License:          Apache-2.0
URL:              http://avro.apache.org

Source0:          https://github.com/apache/avro/archive/refs/tags/release-1.10.2.tar.gz
# file xmvn-reactor required by mvn_install to specify which jar package should be put in rpm
Source1:          xmvn-reactor
# Maven dependencies we use to speedup build on OBS.
Source2:          groovy.tar.gz
Source3:          org.eclipse.jdt.core.tar.gz
Source4:          Saxon-HE.tar.gz
Source5:          zstd-jni.tar.gz
Source6:          biz.aQute.bndlib.tar.gz
Source7:          icu4j.tar.gz
Source8:          hadoop-hdfs-client.tar.gz
Source9:          hadoop-hdfs.tar.gz

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

mkdir -p /home/abuild/.m2/repository/
tar -zxvf %{SOURCE2} -C /home/abuild/.m2/repository/
tar -zxvf %{SOURCE3} -C /home/abuild/.m2/repository/
tar -zxvf %{SOURCE4} -C /home/abuild/.m2/repository/
tar -zxvf %{SOURCE5} -C /home/abuild/.m2/repository/
tar -zxvf %{SOURCE6} -C /home/abuild/.m2/repository/
tar -zxvf %{SOURCE7} -C /home/abuild/.m2/repository/
tar -zxvf %{SOURCE8} -C /home/abuild/.m2/repository/
tar -zxvf %{SOURCE9} -C /home/abuild/.m2/repository/

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
* Thu Nov 24 2022 misaka00251 <liuxin@iscas.ac.cn> - 1.10.2-2
- Fix build on OBS

* Tue Jun 29 2021 Ge Wang <wangge20@huawei.com> - 1.10.2-1
- Init package

