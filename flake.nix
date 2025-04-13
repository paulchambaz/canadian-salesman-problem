{
  description = "Mogpl dev environment";
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };
  outputs = {
    self,
    nixpkgs,
    flake-utils,
  }:
    flake-utils.lib.eachDefaultSystem (
      system: let
        pkgs = import nixpkgs {
          inherit system;
          config = {
            allowUnfree = true;
          };
        };
        python = pkgs.python311;
        pythonPackages = python.pkgs;
        devPkgs = with pkgs; [
          just
          python
          (texlive.combine {
            inherit
              (texlive)
              scheme-full
              adjustbox
              collectbox
              tcolorbox
              pgf
              xetex
              ;
          })
        ];
        pythonPkgs = with pythonPackages; [
          numpy
          matplotlib
          networkx
          tqdm
          scipy
        ];
      in {
        devShells.default = pkgs.mkShell {
          buildInputs = devPkgs ++ pythonPkgs;
        };
      }
    );
}
