PACKAGE_MANAGER = uv
CONFIG = config.json

install:
	@printf "\e[34m%s\e[0m\n" "installing program dependencies.."
	@$(PACKAGE_MANAGER) sync

run:
	@$(PACKAGE_MANAGER) run python3 pac-man.py $(CONFIG)

debug:
	@printf "\e[32m%s\e[0m\n" "running program in debug mode.."
	@$(PACKAGE_MANAGER) run python3 -m pdb pac-man.py $(CONFIG)

deploy:
	@printf "\e[34m%s\e[0m\n" "deploying the game for the current platform.."
	@$(PACKAGE_MANAGER) run pyinstaller \
		--onefile \
		--windowed \
		--name Spooks \
		--add-data "assets:assets" \
		pac-man.py
	@printf "\e[34m%s\e[0m\n" "successfully saved the game to ./dist/Pac-man"


clean:
	@printf "\e[32m%s\e[0m\n" "cleaning residual files.."
	@rm -rf  __pycache__ .mypy_cache
	@find . -name __pycache__ -type d -exec rm -rf {} +

lint:
	@printf "\e[33m%s\e[0m\n" "checking flake8.."
	@$(PACKAGE_MANAGER) run flake8 src/ pac-man.py
	@printf "\e[33m%s\e[0m\n" "checking mypy.."
	@$(PACKAGE_MANAGER) run mypy src/ pac-man.py --warn-return-any \
		   --warn-unused-ignores \
		   --ignore-missing-imports \
		   --disallow-untyped-defs \
		   --check-untyped-defs
	@printf "\e[34m%s\e[0m\n" "All files passed linting"

lint-strict:
	@printf "\e[33m%s\e[0m\n" "checking flake8.."
	@$(PACKAGE_MANAGER) run flake8 src/ pac-man.py
	@printf "\e[33m%s\e[0m\n" "checking mypy strict.."
	@$(PACKAGE_MANAGER) run mypy src/ pac-man.py --strict
	@printf "\e[34m%s\e[0m\n" "All files passed linting"
