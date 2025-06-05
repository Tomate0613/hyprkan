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
      self,
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = import nixpkgs { inherit system; };
      in
      {
        packages.default = pkgs.writeShellApplication {
          name = "hyprkan";

          runtimeInputs = with pkgs; [ socat ];

          text = ''
            ${pkgs.python3}/bin/python ${./hyprkan} "$@"
          '';
        };
      }
    )
    // {
      nixosModules.default =
        {
          config,
          lib,
          pkgs,
          ...
        }:
        with lib;
        {
          options.services.hyprkan = {
            enable = mkEnableOption "Hyprkan Layer Switcher";

            config = mkOption {
              type = types.str;
              default = "";
              description = "Configuration for hyprkan";
            };
          };

          config = mkIf config.services.hyprkan.enable {

            systemd.user.services.hyprkan = {
              description = "Hyprkan Layer Switcher";
              wantedBy = [ "graphical-session.target" ];
              after = [ "graphical-session.target" ];

              serviceConfig =
                let
                  hyprkanConfig = pkgs.writeTextFile {
                    name = "apps.json";
                    text = config.services.hyprkan.config;
                  };
                in
                {
                  ExecStart = ''
                    ${self.packages.${pkgs.system}.default}/bin/hyprkan -c ${hyprkanConfig}
                  '';
                  Restart = "on-failure";
                  RestartSec = 5;
                  Type = "simple";
                };
            };
          };
        };
    };
}
