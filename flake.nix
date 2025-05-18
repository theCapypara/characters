{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.11";
    riptide.url = "github:theCapypara/riptide-all/nixpkg";
  };

  outputs =
    {
      self,
      nixpkgs,
      riptide,
    }:
    let
      supportedSystems = [
        "x86_64-linux"
        "aarch64-linux"
        "x86_64-darwin"
        "aarch64-darwin"
      ];
      forEachSupportedSystem =
        f:
        nixpkgs.lib.genAttrs supportedSystems (
          system:
          f {
            pkgs = import nixpkgs {
              inherit system;
              overlays = [ riptide.overlays.default ];
            };
          }
        );
    in
    {
      packages = forEachSupportedSystem (
        { pkgs }:
        {
          default =
            with pkgs;
            python312Packages.buildPythonApplication {
              name = "characters";

              src = ./.;

              propagatedBuildInputs = [
                python312Packages.pdfrw
                python312Packages.tornado
                python312Packages.configcrunch
              ];
            };
        }
      );
      devShells = forEachSupportedSystem (
        { pkgs }:
        {
          default = pkgs.mkShell {
            packages = with pkgs; [
              (python312.withPackages (pypkgs: [
                pypkgs.pdfrw
                pypkgs.tornado
                pypkgs.configcrunch
              ]))
              ruff
              ruff-lsp
              poetry
            ];
          };
        }
      );
    };
}
