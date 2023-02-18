let pkgs = import <nixpkgs> { };
in
let
  mesh-announce-python = pkgs.python3;
  python-with-mesh-announce-packages = mesh-announce-python.withPackages (p: with p; [
    psutil
  ]);
in
pkgs.mkShell {
  nativeBuildInputs = [
    python-with-mesh-announce-packages
    pkgs.git
    pkgs.lsb-release
    pkgs.ethtool
    pkgs.batctl
  ];
}
