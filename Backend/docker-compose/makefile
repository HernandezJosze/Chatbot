make: ## Print all commands available with make:
	@echo "To execute the next commands you must do:\nmake [command]"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

instructions: ## Give instructions about the requirements to run the project.
	@echo \
"\n\nIn order to run the project you need to make sure you have docker, docker-compose and python installed and running.\n\
Please install docker from the next URL: https://docs.docker.com/desktop/,\n\
Please install docker-compose from the next URL: https://docs.docker.com/compose/install/\n\
Please install python from the next URL https://www.python.org/downloads/\n\
\n\
Make sure you select the correct version for your Operative System.\n\
Once you have this install Execute 'make install' and you are ready to run and test!\n\n"

run: ## Build and run docker images in the docker-compose file.
	docker-compose up -d

down: ## Stop the containers.
	docker-compose down

clean: ## Stop and remove docker images.
	make down
	docker rmi docker-compose-web
	docker rmi ollama/ollama
	docker rmi mariadb

install: #Install the python libraries necessaries to run the tests.
	pip3 install ollama && pip3 install load-dotenv

test: #Run a ollama test.
	@echo "Make sure you have the backend up and running\n"
	python3 ../webserver/tests/test1.py
