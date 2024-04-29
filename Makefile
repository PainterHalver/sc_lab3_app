.PHONY: all clean dev-flask dev-react build-client serve help

CLIENT_DIR = client
PYCACHE_DIRS = $(shell find . -type d -name "__pycache__")

all:
	@echo "Please specify a target or use 'make help' for more information."

clean:
	rm -rf $(PYCACHE_DIRS) $(CLIENT_DIR)/build .scannerwork

dev-flask:
	@echo "Starting Flask server..."
	@echo "Server public IP: $$(curl -fsSL ifconfig.me)"
	python -m flask run --host 0.0.0.0 --port 9000 --debug

dev-react:
	@echo "Starting React server..."
	cd $(CLIENT_DIR) && npm start

build-client:
	cd $(CLIENT_DIR) && npm run build

help:
	@echo "Available targets:"
	@echo "  all         : Display this help message"
	@echo "  clean       : Remove Python cache files and client build files"
	@echo "  dev-flask   : Start the Flask server in development mode"
	@echo "  dev-react   : Start the React server in development mode"
	@echo "  build-client: Build the React client"