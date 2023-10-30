dev_build_up:
	docker compose -f development/docker-compose-dev.yml up -d --build
dev_down:
	docker compose -f development/docker-compose-dev.yml down
dev_up:
	docker compose -f development/docker-compose-dev.yml up -d

prod_build_up:
	docker compose -f production/docker-compose-prod.yml up -d --build
prod_down:
	docker compose -f production/docker-compose-prod.yml down
prod_up:
	docker compose -f production/docker-compose-prod.yml up -d
