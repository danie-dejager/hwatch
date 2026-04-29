Name:           hwatch
Version:        0.4.2
Release:        1%{?dist}
Summary:        A modern alternative to the 'watch' command, it records differences in execution results and allows for examination of these differences afterward.
URL:            https://github.com/blacknon/hwatch/
License:        MIT
Source0:        https://github.com/blacknon/hwatch/archive/refs/tags/%{version}.tar.gz

BuildRequires:  git
BuildRequires:  python3
BuildRequires:  curl
BuildRequires:  gcc

%define debug_package %{nil}
%if 0%{?amzn2023}
%undefine _package_note
%undefine _rpm_package_note
%undefine _hardening_ldflags
%global _build_ldflags %{nil}
%endif

%description
hwatch is a alternative watch command. Records the results of command execution that can display its history and differences.

Features:
* Can keep the history when the difference, occurs and check it later.
* Can check the difference in the history. The display method can be changed in real time.
* Can output the execution result as log (json format).
* Custom keymaps are available.
* Support ANSI color code.
* Execution result can be scroll.
* Not only as a TUI application, but also to have the differences output as standard output.
* If a difference occurs, you can have the specified command additionally executed.

%prep
%setup -q

%build
export RUSTFLAGS="-C link-arg=-fuse-ld=bfd"
# Install Rust using curl
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
export PATH="$PATH:$HOME/.cargo/bin"
%if 0%{?amzn2023}
unset LDFLAGS
export RUSTFLAGS="-C link-arg=-fuse-ld=bfd"
%endif
$HOME/.cargo/bin/cargo build --release --locked --all-features
strip target/release/%{name}

%install
install -D -m 644 completion/bash/%{name}-completion.bash %{buildroot}/etc/bash_completion.d/%{name}.bash
install -D -m 755 target/release/%{name} %{buildroot}/usr/bin/%{name}
install -D -m 644 LICENSE %{buildroot}/usr/share/licenses/%{name}/LICENSE
install -D -m 644 README.md %{buildroot}/usr/share/doc/%{name}/README.md

%check
%if 0%{?amzn2023}
unset LDFLAGS
export RUSTFLAGS="-C link-arg=-fuse-ld=bfd"
%endif

$HOME/.cargo/bin/cargo test --release --locked --all-features -- \
  --skip test_exec_command_with_force_color_stdout_is_tty \
  --skip test_exec_command_with_force_color_stdin_is_tty

%files
%license LICENSE
%doc README.md
/usr/bin/%{name}
/etc/bash_completion.d/%{name}.bash
