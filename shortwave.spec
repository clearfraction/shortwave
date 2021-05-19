%global commit0 9bfc5ee2d857035cf0d3c72e211b3d76b85d7414
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global gver .git%{shortcommit0}

Name:       shortwave
Version:    2.0.1
Release:    2
Summary:    Find and listen to internet radio stations
Group:      Applications/Internet
License:    GPLv3
URL:        https://gitlab.gnome.org/World/Shortwave
Source0:    https://gitlab.gnome.org/World/Shortwave/-/archive/%{commit0}/Shortwave-%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
BuildRequires:  rustc 
BuildRequires:  meson
BuildRequires:  ninja
BuildRequires:  libadwaita-dev
BuildRequires:  gtk4-dev
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gee-0.8)
BuildRequires:  pkgconfig(json-glib-1.0)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(libsoup-2.4)
BuildRequires:  pkgconfig(libnotify)
BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  pkgconfig(gstreamer-pbutils-1.0)
BuildRequires:  pkgconfig(gstreamer-plugins-base-1.0)
BuildRequires:  pkgconfig(gstreamer-plugins-bad-1.0)
BuildRequires:  intltool desktop-file-utils
BuildRequires:  appstream-glib-dev
BuildRequires:  pkgconfig(x11)
BuildRequires:  gettext
BuildRequires:  git
BuildRequires:  libdazzle-dev
BuildRequires:  desktop-file-utils
BuildRequires:  openssl-dev
BuildRequires:  sqlite-autoconf-dev
Requires:       dconf
Requires:       gstreamer1-plugins-base-tools
Requires:       gstreamer1-plugins-base
Requires:       libappstream-glib
Requires:       sqlite-libs
Requires:       gstreamer1-plugins-bad-nonfree
Requires:       gstreamer1-libav

%description
Finding and listening to internet radio stations.

%prep 
%setup -n Shortwave-%{commit0}

# fix pkgdatadir
sed -i  "s|pkgdatadir = join_paths(get_option('prefix'), datadir, meson.project_name())|pkgdatadir = '/opt/3rd-party/bundles/clearfraction/usr/share/shortwave'|" meson.build

%build
#export PATH=$PATH:$PWD/rustdir/bin:/usr/bin
unset http_proxy
unset no_proxy 
unset https_proxy
meson --libdir=lib64 --prefix=/usr  builddir
ninja -v -C builddir

%install
DESTDIR=%{buildroot} ninja -C builddir install

%find_lang shortwave

%files -f %{name}.lang
%license COPYING.md
%{_bindir}/%{name}
%{_datadir}/shortwave/
%{_datadir}/glib-2.0/schemas/*
%{_datadir}/applications/de.haeckerfelix.Shortwave.desktop
%{_datadir}/icons/hicolor/*/apps/de.haeckerfelix.*
%{_datadir}/metainfo/*.xml
%{_datadir}/dbus-1/services/*.service


%changelog
# based on https://github.com/UnitedRPMs/shortwave
