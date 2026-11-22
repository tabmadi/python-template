# The toolchain, the git hooks, and the checks, per ADR-0100 and ADR-0110. The tabkit module holds every shared
# part, and this file adds the Python parts.
{
  description = "A Python application with uv, ruff with every rule, pyrefly, and pytest";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-parts = {
      url = "github:hercules-ci/flake-parts";
      inputs.nixpkgs-lib.follows = "nixpkgs";
    };
    # A new version is a new tag here.
    tabkit = {
      url = "github:tabmadi/tabkit/v0.19.0";
      inputs.nixpkgs.follows = "nixpkgs";
      inputs.flake-parts.follows = "flake-parts";
    };
    # uv2nix builds the environment of uv.lock, so a check installs it without network.
    pyproject-nix = {
      url = "github:pyproject-nix/pyproject.nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    uv2nix = {
      url = "github:pyproject-nix/uv2nix";
      inputs.pyproject-nix.follows = "pyproject-nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    pyproject-build-systems = {
      url = "github:pyproject-nix/build-system-pkgs";
      inputs.pyproject-nix.follows = "pyproject-nix";
      inputs.uv2nix.follows = "uv2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs =
    inputs@{ flake-parts, tabkit, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      # The template scope adds its own checks and outputs. A copy has no template/ folder, so it adds nothing.
      imports = [
        tabkit.flakeModules.default
      ]
      ++ inputs.nixpkgs.lib.optional (builtins.pathExists ./template/scope.nix) ./template/scope.nix;

      perSystem =
        { pkgs, lib, ... }:
        let
          # The Python line of the repo. `requires-python` in pyproject.toml names the same line.
          python = pkgs.python315;
          ruff = "--config .config/ruff.toml";

          # The locked environment of uv.lock with the dev group, built from wheels.
          workspace = inputs.uv2nix.lib.workspace.loadWorkspace { workspaceRoot = ./.; };
          pythonSet =
            (pkgs.callPackage inputs.pyproject-nix.build.packages { inherit python; }).overrideScope
              (
                lib.composeManyExtensions [
                  inputs.pyproject-build-systems.overlays.default
                  (workspace.mkPyprojectOverlay { sourcePreference = "wheel"; })
                ]
              );
          venv = pythonSet.mkVirtualEnv "python-template-env" workspace.deps.all;

          # A check runs on the tracked files with the locked environment.
          pyCheck =
            name: command:
            pkgs.runCommand name
              {
                nativeBuildInputs = [
                  venv
                  pkgs.ruff
                  pkgs.pyrefly
                ];
              }
              ''
                cp -r ${./.} source
                chmod -R u+w source
                cd source
                export HOME=$TMPDIR
                ${command}
                touch $out
              '';
        in
        {
          tabkit.packages = [
            python
            pkgs.uv
            pkgs.ruff
            pkgs.pyrefly
          ];

          # uv uses the Python of the dev shell and never downloads one. A wheel with native code
          # finds the C++ runtime and zlib, which a Nix Python does not give it.
          tabkit.env = {
            UV_PYTHON = "${python}/bin/python3";
            UV_PYTHON_DOWNLOADS = "never";
            LD_LIBRARY_PATH = lib.makeLibraryPath [
              pkgs.stdenv.cc.cc.lib
              pkgs.zlib
            ];
          };

          # A fix stops the commit, so the engineer reviews the change and stages it.
          tabkit.hooks.ruff = {
            name = "ruff";
            entry = "${pkgs.writeShellScript "ruff-fix" ''
              ${pkgs.ruff}/bin/ruff check ${ruff} --fix "$@"
              ${pkgs.ruff}/bin/ruff format ${ruff} "$@"
            ''}";
            files = "\\.py$";
          };

          checks.lint-py = pyCheck "lint-py" ''
            ruff check ${ruff} .
            ruff format ${ruff} --check .
            pyrefly check --python-interpreter-path ${venv}/bin/python
          '';
          checks.test = pyCheck "test" "python -m pytest -p no:cacheprovider";
        };
    };
}
