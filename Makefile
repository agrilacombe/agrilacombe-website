# Makefile for Agri Lacombe Astro Website

# Variables
NPM = npm
NODE_MODULES = node_modules
DIST_DIR = dist
ASTRO_CACHE_DIR = .astro # Astro's cache and build artifacts directory
SCRIPTS_DIR = scripts

.PHONY: all install dev build preview clean deep-clean lint format help

# Default target: Install dependencies (if needed) and start dev server
all: dev

# Install dependencies
# This uses a common pattern to only run install if node_modules doesn't exist or package.json is newer
$(NODE_MODULES): package.json
	$(NPM) install
	@touch $(NODE_MODULES) # Touch node_modules only if npm install runs

install: $(NODE_MODULES)
	@echo "Dependencies are up to date."

# Start development server
dev: install
	$(NPM) run dev

# Build for production
build: install
	$(NPM) run build

# Preview production build
preview: build
	$(NPM) run preview

# Clean project: remove build artifacts
clean:
	@echo "Cleaning project (build artifacts)..."
	rm -rf $(DIST_DIR)
	rm -rf $(ASTRO_CACHE_DIR)/dist
	rm -rf $(ASTRO_CACHE_DIR)/build
	@echo "Build artifacts cleaned."

# Deep clean project: remove build artifacts, node_modules, package-lock.json, and Astro cache
deep-clean:
	@echo "Performing deep clean..."
	# Ensure the script has execute permissions before running
	chmod +x $(SCRIPTS_DIR)/deep-clean.sh
	sh $(SCRIPTS_DIR)/deep-clean.sh
	@echo "Deep clean complete. Run 'make install' or 'npm install' next."

# Lint project files (using Prettier)
lint: install
	$(NPM) run format -- --check . # Uses the format script from package.json with --check flag

# Format project files (using Prettier)
format: install
	$(NPM) run format . # Uses the format script from package.json

# Help: Display available targets
help:
	@echo "Available targets:"
	@echo "  all         - Install dependencies (if needed) and start dev server (default)"
	@echo "  install     - Install project dependencies"
	@echo "  dev         - Start the Astro development server"
	@echo "  build       - Build the project for production"
	@echo "  preview     - Serve the production build locally"
	@echo "  clean       - Remove build artifacts (dist/, .astro/dist/, .astro/build/)"
	@echo "  deep-clean  - Remove build artifacts, node_modules, package-lock.json, and .astro/ directory"
	@echo "  lint        - Check code formatting using Prettier"
	@echo "  format      - Format code using Prettier"
	@echo "  help        - Show this help message"
