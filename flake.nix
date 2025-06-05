{
  description = "Kanata Layer Switcher for Hyprland";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs =
    {
      nixpkgs,
      flake-utils,
      ...
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = import nixpkgs { inherit system; };
      in
      {
        packages.default = pkgs.writeShellApplication {
          name = "my-script";

          runtimeInputs = with pkgs; [ socat ];

          text = ''
            ${pkgs.python3}/bin/python ${./hyprkan} "$@"
          '';
        };
      }
    );
}
