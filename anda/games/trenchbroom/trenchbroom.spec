%global         appid com.kristianduske.TrenchBroom
%global         appstream_component desktop-application

%global         VERSION_YEAR 2026
%global         VERSION_NUMBER 2

Name:           trenchbroom
Version:        %{VERSION_YEAR}.%{VERSION_NUMBER}
Release:        1
Summary:        Cross-Platform Level Editor

License:        GPL-3.0-or-later and BSD-3-Clause and MIT
URL:            https://github.com/TrenchBroom/TrenchBroom
Source0:        %{url}/archive/refs/tags/v%{version}/%{name}-%{version}.tar.gz

#Patch:          0005-Set-build-info-via-options.patch

BuildRequires:  gcc gcc-c++
BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  assimp-devel
BuildRequires:  freeimage-devel
BuildRequires:  catch-devel
BuildRequires:  fmt-devel
BuildRequires:  miniz-devel
BuildRequires:  tinyxml2-devel
BuildRequires:  freetype-devel
BuildRequires:  glew-devel
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtsvg-devel
BuildRequires:  git
BuildRequires:  pandoc
BuildRequires:  desktop-file-utils
BuildRequires:  terra-appstream-helper
# Needed to run dump-shortcuts and tests due to Qt
BuildRequires:  xorg-x11-server-Xvfb

Requires:       hicolor-icon-theme

%description
TrenchBroom is a modern cross-platform level editor for Quake-engine based games.

%prep
%autosetup -n TrenchBroom-%{version} -p1

# It's easier than patching out vcpkg support
# plus it will be removed next release
mkdir -p vcpkg/scripts/buildsystems
touch vcpkg/scripts/buildsystems/vcpkg.cmake

%conf
%cmake \
    -DBUILD_VERSION_YEAR:STRING="%{VERSION_YEAR}" \
    -DBUILD_VERSION_NUMBER:STRING="%{VERSION_NUMBER}" \
    -DBUILD_PLATFORM_NAME:STRING="Terra" \
    -DCMAKE_PREFIX_PATH="cmake/packages;/app"

%build
%cmake_build

%install
%cmake_install

for size in 8 16 22 24 32 36 42 48 64 72 96 128 192 256 512; do
    install -Dm644 \
        "app/TrenchBroom/resources/linux/icons/icon_${size}.png" \
        "%{buildroot}/%{_hicolordir}/${size}x${size}/apps/trenchbroom.png"
done

%desktop_file_install app/TrenchBroom/resources/linux/trenchbroom.desktop

%check

%desktop_file_validate %{buildroot}%{_appsdir}/trenchbroom.desktop

%terra_appstream

pushd %{__cmake_builddir}/common/test
xvfb-run ./common-regression-test
xvfb-run ./common-test
popd

xvfb-run %{__cmake_builddir}/lib/kdl/test/kdl-test
xvfb-run %{__cmake_builddir}/lib/vm/test/vm-test


%files
%license LICENSE.txt
%doc README.md
%{_bindir}/trenchbroom
%{_datadir}/TrenchBroom
%{_appsdir}/trenchbroom.desktop
%{_hicolordir}/*/apps/vkquake.png
%{_metainfodir}/%{appid}.metainfo.xml
%{_datadir}/mime/packages/trenchbroom.xml

%changelog
* Mon Jun 29 2026 Jan200101 <sentrycraft123@gmail.com>
- Initial package
