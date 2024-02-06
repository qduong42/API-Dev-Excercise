py = $(shell if [ -d $(PWD)/'.venv' ]; then echo $(PWD)/".venv/bin/python3"; else echo "python3"; fi)
pip = $(py) -m pip

all: build

build:
	@echo "Building configuration docker-compose up in detached mode...\n"
	@docker-compose up -d
	@echo "Installling python packages using pip install...\n"
	${pip} install pymongo requests fastapi uvicorn python-dotenv pandas wheel
	@echo "executing dataReceiveStoreEnv.py\n"
	${py} dataReceiveStoreEnv.py
	@echo "executing mainEnv.py\n"
	${py} mainEnv.py

install:
	${pip} install pymongo requests fastapi uvicorn python-dotenv pandas wheel

up:
	@docker-compose up -d

down:
	@docker-compose down

stop-remove-containers:
	@CONTAINERS=$$(docker ps -qa); \
	if [ -n "$$CONTAINERS" ]; then \
		docker stop $$CONTAINERS; \
		docker rm $$CONTAINERS; \
	else \
		echo "No running containers to stop/rm."; \
	fi

remove-volume:
	@DOCKERVOLUME=$$(docker volume ls -q); \
	if [ -n "$$DOCKERVOLUME" ]; then \
		docker volume rm  $$DOCKERVOLUME; \
	else \
		echo "No volumes to rm."; \
	fi

fclean: stop-remove-containers  remove-volume
	@echo "Total clean of all configurations docker\n"
	@docker system prune -a
	@for image in $$(docker images -qa); do \
		if docker image inspect -f '{{.Id}} {{.Parent}}' $$image | grep -q -E '^$(image)'; then \
			docker rmi -f $$image; \
		else \
			echo "no images to remove"; \
		fi; \
	done

.PHONY	: all build down re clean fclean

re: fclean
	all