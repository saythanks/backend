API=backend_api_1

db/downgrade:
	docker exec $(API) pipenv run flask db downgrade

db/upgrade:
	docker exec $(API) pipenv run flask db upgrade
