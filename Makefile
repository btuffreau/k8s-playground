APPLICATION_NAME = "awesome_app"
APPLICATION_VERSION = "latest"
INCLUSTER_REGISTRY_NAME = "kind-registry"
INCLUSTER_REGISTRY_PORT = 5000
LOCAL_REGISTRY = "localhost:5001"
LOCAL_KUBE_CONTEXT = "kind-aetion"

.PHONY: env deploy py build clean

env: py
	@echo "Deploying kubernetes cluster and container registry..."
	@bash -c "./setup/setup.sh $(INCLUSTER_REGISTRY_NAME) $(INCLUSTER_REGISTRY_PORT)"
	@echo "'$(LOCAL_KUBE_CONTEXT)' context created, local registry $(LOCAL_REGISTRY) (inbound $(INCLUSTER_REGISTRY_NAME):$(INCLUSTER_REGISTRY_PORT))"

py:
	@pip3.11 install -e ./frontend

build:
	@docker build --tag $(LOCAL_REGISTRY)/$(APPLICATION_NAME):$(APPLICATION_VERSION) ./frontend

push: env build
	@docker push  $(LOCAL_REGISTRY)/$(APPLICATION_NAME):$(APPLICATION_VERSION)
	@echo "New image available at \
	${INCLUSTER_REGISTRY_NAME}:${INCLUSTER_REGISTRY_PORT}/${APPLICATION_NAME}:${APPLICATION_VERSION}"

deploy:
	@kubectl apply --context $(LOCAL_KUBE_CONTEXT) -f ./deploy/

release: push deploy
	@kubectl rollout restart --context $(LOCAL_KUBE_CONTEXT) -n aetion deployment/frontend

clean:
	@kubectl delete --context $(LOCAL_KUBE_CONTEXT) -f ./deploy/
