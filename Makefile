run-monitor:
	docker run --rm -d --name monitor -p 8080:8080/tcp ghcr.io/tanmoysg/logsmith-monitor:v0.0.6

show-monitor:
	docker logs --tail 1000 -f monitor