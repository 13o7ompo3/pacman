SRC_DIR = src
SRC = $(shell find $(SRC_DIR) -path '*/__pycache__' -prune -o -type f -name '*.py' -print)
PACKAGE_MANAGER = uv
CONFIG = config.json

install:
	echo $(SRC)
	@printf "\e[34m%s\e[0m\n" "installing program dependencies.."
	@$(PACKAGE_MANAGER) sync

run:
	@$(PACKAGE_MANAGER) run python3 pac-man.py $(CONFIG)

debug:
	@printf "\e[32m%s\e[0m\n" "running program in debug mode.."
	@$(PACKAGE_MANAGER) run python3 -m pdb pac-man.py $(CONFIG)

clean:
	@printf "\e[32m%s\e[0m\n" "cleaning residual files.."
	@rm -rf  __pycache__ .mypy_cache

lint:
	@printf "\e[33m%s\e[0m\n" "checking flake8.."
	$(PACKAGE_MANAGER) run flake8 $(SRC)
	@printf "\e[33m%s\e[0m\n" "checking mypy.."
	$(PACKAGE_MANAGER) run mypy $(SRC) --warn-return-any \
		   --warn-unused-ignores \
		   --ignore-missing-imports \
		   --disallow-untyped-defs \
		   --check-untyped-defs

lint-strict:
	@printf "\e[33m%s\e[0m\n" "checking flake8.."
	$(PACKAGE_MANAGER) run flake8 $(SRC)
	@printf "\e[33m%s\e[0m\n" "checking mypy strict.."
	$(PACKAGE_MANAGER) run mypy $(SRC) --strict
