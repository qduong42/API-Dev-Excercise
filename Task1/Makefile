ifeq ($(OS),Windows_NT)
	OOS := Windows
else
	OOS := other
endif

all: build

build: venv
	@echo "Building configuration docker-compose up in detached mode...\n"
	@docker-compose up -d
	@echo "executing dataReceiveStoreEnv.py\n"
ifeq ($(OOS),Windows)
	@echo "executing dataReceiveStoreEnv.py\n"
	@if [ -f venv/Scripts/activate ]; then venv/Scripts/python dataReceiveStoreEnv.py; else python dataReceiveStoreEnv.py; fi
	@echo "executing mainEnv.py\n"
	@if [ -f venv/Scripts/activate ]; then venv/Scripts/python mainEnv.py; else python mainEnv.py; fi
else
	@echo "executing dataReceiveStoreEnv.py\n"
	@if [ -f venv/bin/activate ]; then venv/bin/python3 dataReceiveStoreEnv.py; else python3 dataReceiveStoreEnv.py; fi
	@echo "executing mainEnv.py\n"
	@if [ -f venv/bin/activate ]; then venv/bin/python3 mainEnv.py; else python3 mainEnv.py; fi
endif

venv:
ifeq ($(OOS),Windows)
	-python -m venv venv; VENV_EXIT_CODE=$$?; \
	if [ $$VENV_EXIT_CODE -eq 0 ]; then . venv/Scripts/activate; venv/Scripts/pip install pymongo requests fastapi uvicorn python-dotenv pandas wheel termcolor;  else echo "Failed to create virtual environment"; exit 1; fi
else
	-python3 -m venv venv; VENV_EXIT_CODE=$$?; \
	if [ $$VENV_EXIT_CODE -eq 0 ]; then . venv/bin/activate; venv/bin/pip install pymongo requests fastapi uvicorn python-dotenv pandas wheel termcolor; else echo "Failed to create virtual environment"; exit 1; fi
endif
	@echo "Virtual environment detection passed successfully."

up:
	@docker-compose up -d

down:
	@docker-compose down

stop-remove-containers:
	@echo "Stopping and removing containers\n"
	@CONTAINERS=$$(docker ps -qa); \
	if [ -n "$$CONTAINERS" ]; then \
	docker stop $$CONTAINERS; \
	docker rm $$CONTAINERS; \
	else \
	echo "No running containers to stop/rm."; \
	fi

remove-volume:
	@echo "Cleaning all volumes"
	@DOCKERVOLUME=$$(docker volume ls -q); \
	if [ -n "$$DOCKERVOLUME" ]; then \
	docker volume rm  $$DOCKERVOLUME; \
	else \
	echo "No volumes to rm."; \
	fi

remove_image:
	@echo "Removing all images"
	@for image in $$(docker images -qa); do \
	if docker image inspect -f '{{.Id}} {{.Parent}}' $$image | grep -q -E '^$(image)'; then \
	docker rmi -f $$image; \
	else \
	echo "no images to remove"; \
	fi; \
	done

fclean: stop-remove-containers  remove-volume remove_image
	@docker system prune -a
	@echo "All docker configuration cleaned!\n"


.PHONY	: all build down re clean fclean venv install up stop-remove-containers remove-volume

re: fclean
	$(MAKE) all