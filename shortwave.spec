%global debug_package %{nil}

%global commit0 c3b47d7fcd5b2f0f1324f6668c58db843cc8e6bb
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global gver .git%{shortcommit0}

Name:       shortwave
Version:    1.0.1
Release:    8%{?gver}
Summary:    Find and listen to internet radio stations

Group:      Applications/Internet
License:    GPLv3
URL:        https://gitlab.gnome.org/World/Shortwave
Source0:    https://gitlab.gnome.org/World/Shortwave/-/archive/%{commit0}/Shortwave-%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz

#BuildRequires:  rustc 
BuildRequires:  meson
BuildRequires:  ninja
BuildRequires:  pkgconfig(gtk+-3.0) >= 3.14
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  pkgconfig(gee-0.8)
BuildRequires:  pkgconfig(json-glib-1.0)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(libsoup-2.4)
BuildRequires:  pkgconfig(libnotify)
BuildRequires:  pkgconfig(gstreamer-pbutils-1.0)
BuildRequires:  pkgconfig(gstreamer-plugins-base-1.0)
BuildRequires:  pkgconfig(gstreamer-plugins-bad-1.0)
BuildRequires:  intltool desktop-file-utils
BuildRequires:	 appstream-glib-dev
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:	 gettext
BuildRequires:	 git
BuildRequires:	 libhandy-devel
BuildRequires:	 libdazzle-devel
BuildRequires:	 desktop-file-utils
BuildRequires:	 openssl-dev
BuildRequires:	 gcc
Requires:       dconf
Requires:       gstreamer1-plugins-base-tools
Requires:       gstreamer1-plugins-base
Requires:       libappstream-glib
Requires:       sqlite-libs
Requires:       gstreamer1-plugins-bad-nonfree
Requires:       gstreamer1-libav

%description
A GTK3 app for finding and listening to internet radio stations.

%prep 
%setup -n Shortwave-%{commit0}

# We need Rust 1.39
mkdir -p rustdir
curl -O https://static.rust-lang.org/dist/rust-nightly-x86_64-unknown-linux-gnu.tar.gz
tar xmzvf rust-nightly-x86_64-unknown-linux-gnu.tar.gz -C $PWD
chmod a+x rust-nightly-x86_64-unknown-linux-gnu/install.sh
rust-nightly-x86_64-unknown-linux-gnu/install.sh --prefix=rustdir --disable-ldconfig --verbose

%build
export PATH=$PATH:$PWD/rustdir/bin:/usr/bin
meson --libdir=lib64 --prefix=/usr --buildtype=plain  builddir
ninja -v -C builddir

%install
DESTDIR=%{buildroot} ninja -C builddir install

%find_lang shortwave

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/de.haeckerfelix.Shortwave.desktop

%post
%{_bindir}/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ]
then
    %{_bindir}/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    %{_bindir}/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
    %{_bindir}/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans
%{_bindir}/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
%{_bindir}/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

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
